from typing import Union

from pandas import DataFrame  # type: ignore[import]

from datatosk import types
from datatosk.sources.source import SourceRead


class SQLRead(SourceRead):
    """Base class to be inherited by all SQL database based SourceRead classes."""

    def __call__(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> DataFrame:
        """Default all SQLRead() children .read() implementation."""
        return self.to_pandas(query=query, params=params, **kwargs)

    def to_dict(self) -> Union[types.DictType, types.JSONType]:
        raise NotImplementedError

    def to_list(self) -> types.ListType:
        raise NotImplementedError

    def to_pandas(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> DataFrame:
        raise NotImplementedError
