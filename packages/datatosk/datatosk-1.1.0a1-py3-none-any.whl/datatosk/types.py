from datetime import datetime, date
from typing import Any, Iterable, List, Mapping, Optional, Tuple, Union

KwargsType = Union[
    Mapping[
        Union[str, bytes, int, float],
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    str,
    bytes,
    None,
    Tuple[
        Union[str, bytes, int, float],
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        str,
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        bytes,
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        int,
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        float,
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
]

JSONType = Union[str, int, float, bool, None, Mapping[str, Any], List[Any]]

ListType = List[Union[str, int, float, bool, List[Union[str, int, float, bool]]]]

DictType = Union[List[Mapping[str, Union[str, int, float, bool]]], JSONType]

_ParamTypes = Union[str, int, float, bool, datetime, date]

ParamsType = Optional[
    Mapping[
        str,
        Union[_ParamTypes, Iterable[_ParamTypes]],
    ]
]
