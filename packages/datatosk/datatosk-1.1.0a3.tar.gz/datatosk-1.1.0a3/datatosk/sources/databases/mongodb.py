from typing import List, Optional, Union

import pandas as pd  # type: ignore[import]
from pymongo import MongoClient  # type: ignore[import]
from pymongo.collection import Collection  # type: ignore[import]
from pymongo.cursor import Cursor  # type: ignore[import]
from pymongo.database import Database  # type: ignore[import]
from pymongo.results import InsertManyResult  # type: ignore[import]

from datatosk import types
from datatosk.sources.source import Source, SourceParam, SourceRead, SourceWrite


# pylint: disable = abstract-method
class MongoRead(SourceRead):
    """
    Interface class for reading data from MongoDB.

    Attributes:
        database: A MongoDB database name
    """

    def __init__(self, database: Database) -> None:
        self.database = database

    def __call__(
        self,
        collection: str = "",
        query_filter: types.DictType = None,
        projection: types.DictType = None,
    ) -> Cursor:
        collection_instance: Collection = self.database[collection]
        return collection_instance.find(filter=query_filter, projection=projection)

    def to_list(
        self,
        collection: str = "",
        query_filter: types.DictType = None,
        projection: types.DictType = None,
    ) -> types.ListType:
        collection_instance: Collection = self.database[collection]
        return list(
            collection_instance.find(filter=query_filter, projection=projection)
        )

    def to_pandas(
        self,
        collection: str = "",
        query_filter: types.DictType = None,
        projection: types.DictType = None,
    ) -> pd.DataFrame:
        return pd.DataFrame(
            self.to_list(
                collection=collection, query_filter=query_filter, projection=projection,
            ),
        )

    def to_dict(self) -> Union[types.DictType, types.JSONType]:
        raise NotImplementedError


class MongoWrite(SourceWrite):
    """
    Interface class for writing data to MongoDB.

    Attributes:
        database: A MongoDB database name
    """

    def __init__(self, database: Database) -> None:
        self.database = database

    def __call__(
        self,
        collection: str,
        data: Union[pd.DataFrame, types.DictType, types.ListType],
    ) -> InsertManyResult:
        collection = self.database[collection]
        if isinstance(data, pd.DataFrame):
            return self.from_pandas(df=data, collection=collection)

        raise NotImplementedError(f"Unsupported data type: {type(data)}")

    def from_pandas(
        self,
        df: Optional[pd.DataFrame] = None,
        collection: Optional[Collection] = None,
    ) -> InsertManyResult:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df argument must be a pandas dataframe")

        data = df.to_dict(orient="records")
        return self._execute_write(collection=collection, data=data)

    def from_dict(self, data: types.DictType) -> None:
        raise NotImplementedError

    def from_list(self, data: types.DictType) -> None:
        raise NotImplementedError

    @staticmethod
    def _execute_write(
        collection: Collection, data: Union[types.ListType, types.DictType],
    ) -> InsertManyResult:
        if isinstance(data, list):
            return collection.insert_many(documents=data)
        if isinstance(data, dict):
            return collection.insert_one(document=data)

        raise NotImplementedError("Unsupported data type")


class MongoSource(Source):
    """
    MongoDB database interface.

    Attributes:
        source_name: source identifier.
            Environment variables that should be defined:
            - `MONGO_HOST_[SOURCE_NAME]`
            - `MONGO_PORT_[SOURCE_NAME]`
            - `MONGO_DATABASE_[SOURCE_NAME]`
            - `MONGO_USER_[SOURCE_NAME]`
            - `MONGO_PASSWORD_[SOURCE_NAME]`

    Examples:

    Reading from MongoDB Source
    ===========================

    >>> import datatosk
    >>> mongo_source = datatosk.mongodb("source_name")
    >>> mongo_source.read.to_list(
        collection="vintage_guitars", command="find", query={"model": "stratocaster"},
    )
    [
      {
        '_id': ObjectId('5f4cc56f45f571f6532b57de'),
        'name': "Fender Standard Stratocaster Olympic White",
        'year_of_production': "1974",
        'price': 1340000
      }
    ]

    Writing to MongoDB Source
    ====================

    >>> import datatosk
    >>> mongo_source = datatosk.mongodb("source_name")
    >>> mongo_source.write(
        collection="vintage_guitars", command="insert_many", data=DataFrame()
    )

    The library will attepmt to automatically handle passed data type,
    but there's also a possibiliti to force a particular type:
    >>> mongo_source.write.from_dict(
        collection="vintage_guitars", command="insert_many", data={}
    )
    """

    def __init__(self, source_name: str) -> None:
        super().__init__(source_name)
        self.client = MongoClient(
            host=self.init_params["MONGO_HOST"],
            port=int(self.init_params["MONGO_PORT"]),
            username=self.init_params["MONGO_USER"],
            password=self.init_params["MONGO_PASSWORD"],
        )
        self.database = self.client[self.init_params["MONGO_DATABASE"]]

    @property
    def params(self) -> List[SourceParam]:
        return [
            SourceParam(env_name="MONGO_HOST"),
            SourceParam(env_name="MONGO_PORT"),
            SourceParam(env_name="MONGO_DATABASE"),
            SourceParam(env_name="MONGO_USER"),
            SourceParam(env_name="MONGO_PASSWORD"),
        ]

    @property
    def read(self) -> MongoRead:
        return MongoRead(database=self.database)

    @property
    def write(self) -> MongoWrite:
        return MongoWrite(database=self.database)
