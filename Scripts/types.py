from typing import (
    Generic,
    Literal,
    NotRequired,
    Required,
    TypeAlias,
    TypedDict,
    TypeVar,
)


class _APIName(TypedDict):
    """
    Represents the name of an API entity.
    """

    name: Required[str]


class _APIDocstring(TypedDict):
    """
    Represents the docstring of an API entity.
    """

    docstring: NotRequired[str]


_T = TypeVar("_T", bound=str)


class _APIType(_APIName, _APIDocstring, Generic[_T]):
    """
    Represents a generic API type.
    """

    kind: Required[_T]


class APISimpleType(_APIType[Literal["simple"]]):
    """
    Represents a simple API type.
    """


class APIEnumerationItemType(_APIName, _APIDocstring):
    """
    Represents an item in an enumeration type.
    """

    value: Required[int]


class APIEnumerationType(_APIType[Literal["enumeration"]]):
    """
    Represents an enumeration API type.
    """

    items: Required[list[APIEnumerationItemType]]


class APIParameterType(_APIName, _APIDocstring):
    """
    Represents a parameter in an API.
    """

    type_name: Required[str]
    nilable: Required[bool]
    table: NotRequired[bool]
    stride: NotRequired[int]
    default: NotRequired[str]


class APIStructureType(_APIType[Literal["structure"]]):
    """
    Represents a structure API type.
    """

    fields: Required[list[APIParameterType]]


class APICallbackType(_APIType[Literal["callback"]]):
    """
    Represents a callback API type.
    """

    arguments: Required[list[APIParameterType]]


APIAnyType: TypeAlias = (
    APISimpleType | APIEnumerationType | APIStructureType | APICallbackType
)


class APICallable(_APIName, _APIDocstring):
    """
    Represents a callable API entity.
    """

    arguments: Required[list[APIParameterType]]
    returns: Required[list[APIParameterType]]


class APIEvent(_APIName, _APIDocstring):
    """
    Represents an event API entity.
    """

    payload: Required[list[APIParameterType]]


_G = TypeVar("_G")


class APIGroup(_APIName, Generic[_G]):
    """
    Represents a group of API entities.
    """

    namespace: NotRequired[str]
    filename: Required[str]
    items: Required[list[_G]]


class APICallableGroup(APIGroup[APICallable]):
    """
    Represents a group of callable API entities.
    """


class APIEventGroup(APIGroup[APIEvent]):
    """
    Represents a group of event API entities.
    """


class APIDocumentation(TypedDict):
    """
    Represents the documentation of an API.
    """

    version: Required[str]
    types: Required[list[APIAnyType]]
    callables: Required[list[APICallableGroup]]
    events: Required[list[APIEventGroup]]
