from typing import List, Union, Final, Optional, Any
from datetime import datetime, date

from google.cloud.bigquery import Client, ScalarQueryParameter, ArrayQueryParameter, QueryJobConfig  # type: ignore[import]
import pandas as pd  # type: ignore[import]

from datatosk import types
from datatosk.sources.databases.sql.sql_source import SQLRead
from datatosk.sources.source import Source, SourceParam, SourceWrite


class BigqueryTypes:  # pylint: disable=too-few-public-methods
    """GBQ data types."""

    BOOL: Final[str] = "BOOL"
    INT64: Final[str] = "INT64"
    FLOAT64: Final[str] = "FLOAT64"
    DATE: Final[str] = "DATE"
    TIMESTAMP: Final[str] = "TIMESTAMP"
    STRING: Final[str] = "STRING"


class GBQRead(SQLRead):
    """Interface element for retrieving data from GBQ dataset.

    Attributes:
        client: bigquery.Client object
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    def to_list(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> types.ListType:

        return list(self._query(query=query, params=params, **kwargs))

    def to_dict(self) -> types.DictType:
        raise NotImplementedError

    def to_pandas(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> pd.DataFrame:

        return self._query(query=query, params=params, **kwargs).to_dataframe()

    def _query(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> Any:
        return self.client.query(
            query=query,
            job_config=self._configure_job(params=params),
            **kwargs,
        )

    def _configure_job(
        self, params: types.ParamsType = None
    ) -> Optional[QueryJobConfig]:

        if params is None:
            return None

        query_parameters = []
        for param_name, param_value in params.items():

            if isinstance(param_value, (list, tuple)):

                assert all(
                    isinstance(item, type(param_value[0])) for item in param_value
                ), f"Items in `{param_name}` are inconsistent"

                param_val = param_value[0]
                param_type = ArrayQueryParameter
            else:
                param_val = param_value
                param_type = ScalarQueryParameter

            query_parameters.append(
                param_type(
                    param_name, self._recognize_param_type(param_val), param_value
                )
            )

        return QueryJobConfig(query_parameters=query_parameters)

    @staticmethod
    def _recognize_param_type(  # pylint: disable=too-many-return-statements
        param_value: Union[bool, float, int, datetime, date, str]
    ) -> str:

        if isinstance(param_value, bool):
            return BigqueryTypes.BOOL

        if isinstance(param_value, int):
            return BigqueryTypes.INT64

        if isinstance(param_value, float):
            return BigqueryTypes.FLOAT64

        if isinstance(param_value, datetime):
            return BigqueryTypes.TIMESTAMP

        if isinstance(param_value, date):
            return BigqueryTypes.DATE

        if isinstance(param_value, str):
            try:
                datetime.fromisoformat(param_value)
            except ValueError:
                return BigqueryTypes.STRING
            else:
                return BigqueryTypes.TIMESTAMP

        raise ValueError(f"Parameter type {type(param_value)} is not supported.")


class GBQSource(Source):
    """GBQ database interface, it enables retrieving data from it.

    Attributes:
        source_name: source identifier.
            Envioronment variables that should be defined:
            - `GBQ_PROJECT_ID_[SOURCE_NAME]`
        client: google.cloud.bigquery.Client object

    Examples:

    Reading GoogleBigQuery Source
    ====================

    >>> import datatosk
    >>> source = datatosk.gbq(source_name="epic_source")
    >>> source.read("SELECT * FROM epic_table")
        superheros        real_name
    0      Ironman       Tony Stark
    1       Batman      Bruce Wayne
    2     Catwoman      Selina Kyle

    Use of params
    -------------

    >>> source = datatosk.gbq(source_name="epic_source")
    >>> source.read(
    ...     "SELECT superheros, real_name"
    ...     "FROM epic_table"
    ...     "WHERE superheroes = @superhero",
    ...     params={"superhero": "Catwoman"}
    ...)
        superheros        real_name
    0     Catwoman      Selina Kyle
    """

    def __init__(self, source_name: str) -> None:
        super().__init__(source_name)
        self.client = Client(project=self.init_params["GBQ_PROJECT_ID"])

    @property
    def params(self) -> List[SourceParam]:
        return [SourceParam(env_name="GBQ_PROJECT_ID")]

    @property
    def read(self) -> GBQRead:
        """Interface element for retrieving data from GBQ dataset.

        Returns:
            Method-like class which can be used to retrieve data in various types.
        """
        return GBQRead(client=self.client)

    @property
    def write(self) -> SourceWrite:
        """Not implemented yet"""
        raise NotImplementedError
