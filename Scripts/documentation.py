from typing import Any, Optional

from Scripts.types import (
    APIAnyType,
    APICallable,
    APICallableGroup,
    APICallbackType,
    APIDocumentation,
    APIEnumerationItemType,
    APIEnumerationType,
    APIEvent,
    APIEventGroup,
    APIParameterType,
    APISimpleType,
    APIStructureType,
)

# Helpers


def _assert_parameter(
    name_data: Any,
    type_index_data: Any,
    nilable_table_data: Any,
    stride_data: Any,
    default_data: Any,
    docstring_data: Any,
) -> APIParameterType:
    """
    Asserts the validity of a parameter data structure.

    Args:
        name_data: The data representing the parameter name.
        type_index_data: The data representing the parameter type index.
        nilable_table_data: The data representing nilable and table flags of the parameter.
        stride_data: The data representing the stride index of the parameter.
        default_data: The data representing the default value of the parameter.
        docstring_data: The data representing the docstring of the parameter.

    Returns:
        A validated parameter structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    name = _assert_name(name_data)
    type_index = _assert_type_index(type_index_data)
    nilable, table, stride = _assert_nilable_table_stride(
        nilable_table_data, stride_data
    )
    default = _assert_default(default_data)
    docstring = _assert_docstring(docstring_data)

    parameter = APIParameterType(
        {"name": name, "type_name": str(type_index), "nilable": nilable}
    )

    if table:
        parameter["table"] = True
    if stride is not None:
        parameter["stride"] = stride
    if default is not None:
        parameter["default"] = default
    if docstring is not None:
        parameter["docstring"] = docstring

    return parameter


def _assert_name(data: Any) -> str:
    """
    Asserts the validity of a parameter name.

    Args:
        data: The data representing the parameter name.

    Returns:
        A validated parameter name.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, str)

    return data


def _assert_type_index(data: Any) -> int:
    """
    Asserts the validity of a type index.

    Args:
        data: The data representing the type index.

    Returns:
        A validated type index.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, int)

    return data


def _assert_nilable_table_stride(
    nilable_table_data: Any, stride_data: Any
) -> tuple[bool, bool, Optional[int]]:
    """
    Asserts the validity of nilable, table, and stride properties.

    Args:
        nilable_table_data: The data representing nilable and table flags.
        stride_data: The data representing the stride index.

    Returns:
        A validated tuple representing nilable, table, and stride properties.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(nilable_table_data, int)
    # 0: Nilable=false; 1: Nilable=true; 2: Nilable=false,table; 3: Nilable=true,table 4: Nilable=false,StrideIndex=1 (vararg)
    assert nilable_table_data in [0, 1, 2, 3, 4]

    # 1: StrideIndex=1; 2: StrideIndex=2; 3: StrideIndex=3
    assert stride_data is None or isinstance(stride_data, int)

    return (nilable_table_data in [1, 3], nilable_table_data in [2, 3], stride_data)


def _assert_default(data: Any) -> Optional[str]:
    """
    Asserts the validity of a default value.

    Args:
        data: The data representing the default value.

    Returns:
        A validated default value.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    if data is not None:
        return str(data)

    return data


def _assert_docstring(data: Any) -> Optional[str]:
    """
    Asserts the validity of a docstring.

    Args:
        data: The data representing the docstring.

    Returns:
        A validated docstring.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert data is None or isinstance(data, str)

    return data


# Documentation


def _assert_api_documentation(data: Any) -> APIDocumentation:
    """
    Asserts the validity of the API documentation data structure.

    Args:
        data: The data representing the API documentation.

    Returns:
        A validated API documentation structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, dict)
    assert sorted(data.keys()) == sorted(["api", "version", "types"])

    version = data["version"]
    assert isinstance(version, str)

    types_data = data["types"]
    assert isinstance(types_data, list)

    api_types = [_assert_api_type(api_type) for api_type in types_data]

    api_declarations = data["api"]
    assert isinstance(api_declarations, list)

    api_callables: list[APICallableGroup] = []
    api_events: list[APIEventGroup] = []
    for api_declaration_data in api_declarations:
        callable_group, event_group = _assert_declaration_group(api_declaration_data)
        if len(callable_group["items"]) > 0:
            api_callables.append(callable_group)
        if len(event_group["items"]) > 0:
            api_events.append(event_group)

    return {
        "version": version,
        "types": api_types,
        "callables": api_callables,
        "events": api_events,
    }


# Types


def _assert_api_type(data: Any) -> APIAnyType:
    """
    Asserts the validity of an API type data structure.

    Args:
        data: The data representing an API type.

    Returns:
        A validated API type structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) in [1, 4]

    name = data[0]
    assert isinstance(name, str)

    if len(data) == 4:
        alias = data[1]
        assert isinstance(alias, str)

        mixin = data[2]
        assert mixin is None or isinstance(mixin, str)

        data = data[3]
        assert isinstance(data, list)

        if alias == name:
            assert len(data) == 0

            return APISimpleType(
                {"name": name if mixin is None else mixin, "kind": "simple"}
            )
        else:
            assert mixin is None

            match alias:
                case "Enumeration":
                    return APIEnumerationType(
                        {
                            "name": name,
                            "kind": "enumeration",
                            "items": [_assert_enumeration_item(item) for item in data],
                        }
                    )
                case "Structure":
                    return APIStructureType(
                        {
                            "name": name,
                            "kind": "structure",
                            "fields": [
                                _assert_structure_field(field) for field in data
                            ],
                        }
                    )
                case "function":
                    return APICallbackType(
                        {
                            "name": name,
                            "kind": "callback",
                            "arguments": [
                                _assert_callback_argument(argument) for argument in data
                            ],
                        }
                    )
                case _:
                    assert False

    return APISimpleType({"name": name, "kind": "simple"})


def _assert_enumeration_item(data: Any) -> APIEnumerationItemType:
    """
    Asserts the validity of an enumeration item data structure.

    Args:
        data: The data representing an enumeration item.

    Returns:
        A validated enumeration item structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) == 5

    name = data[0]
    assert isinstance(name, str)

    unknown_2 = data[1]
    assert isinstance(unknown_2, int)

    unknown_3 = data[2]
    assert unknown_3 is None

    value = data[3]
    assert isinstance(value, int)

    # unused
    unknown_5 = data[4]
    assert isinstance(unknown_5, int)
    assert unknown_5 == 0

    return APIEnumerationItemType({"name": name, "value": value})


def _assert_structure_field(data: Any) -> APIParameterType:
    """
    Asserts the validity of a structure field data structure.

    Args:
        data: The data representing a structure field.

    Returns:
        A validated structure field structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) in [5, 6, 7]

    field = _assert_parameter(
        data[0],
        data[1],
        data[4],
        None,
        data[5] if len(data) >= 6 else None,
        data[6] if len(data) == 7 else None,
    )

    mixin = data[2]
    assert mixin is None or isinstance(mixin, str)

    unknown_4 = data[3]
    assert unknown_4 is None

    return field


def _assert_callback_argument(data: Any) -> APIParameterType:
    """
    Asserts the validity of a callback argument data structure.

    Args:
        data: The data representing a callback argument.

    Returns:
        A validated callback argument structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) == 4

    argument = _assert_parameter(data[0], data[1], data[3], None, None, None)

    mixin = data[2]
    assert mixin is None

    return argument


# Declarations


def _assert_declaration_group(data: Any) -> tuple[APICallableGroup, APIEventGroup]:
    """
    Asserts the validity of a declaration group data structure.

    Args:
        data: The data representing a declaration group.

    Returns:
        A validated declaration group structure containing callable and event groups.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) > 0

    meta = data[0]
    assert isinstance(meta, list)
    assert len(meta) == 4

    name = meta[0]
    assert isinstance(name, str)

    namespace = meta[1]
    assert namespace is None or isinstance(namespace, str)

    category = meta[2]
    assert isinstance(category, str)
    assert category in ["ScriptObject", "System"]

    filename = meta[3]
    assert isinstance(filename, str)

    assert namespace is None or isinstance(namespace, str)
    callable_group = APICallableGroup({"name": name, "filename": filename, "items": []})
    event_group = APIEventGroup({"name": name, "filename": filename, "items": []})

    if namespace is not None:
        callable_group["namespace"] = namespace
        event_group["namespace"] = namespace

    for declaration_data in data[1:]:
        declaration = _assert_declaration(declaration_data)

        if "payload" in declaration:
            event_group["items"].append(declaration)
        else:
            callable_group["items"].append(declaration)

    return (callable_group, event_group)


def _assert_declaration(data: Any) -> APICallable | APIEvent:
    """
    Asserts the validity of a declaration data structure.

    Args:
        data: The data representing a declaration.

    Returns:
        A validated declaration structure, which can be either a callable or an event.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) in [3, 4]

    name = data[0]
    assert isinstance(name, str)

    arguments_or_e = data[1]
    assert isinstance(arguments_or_e, (str, list))

    returns_or_payload = data[2]
    assert isinstance(returns_or_payload, list)

    docstring = data[3] if len(data) == 4 else None
    assert docstring is None or isinstance(docstring, str)

    if isinstance(arguments_or_e, str):
        assert arguments_or_e == "e"

        event = APIEvent(
            {
                "name": name,
                "payload": [_assert_payload(p) for p in returns_or_payload],
            }
        )

        if docstring is not None:
            event["docstring"] = docstring

        return event

    _callable = APICallable(
        {
            "name": name,
            "arguments": [_assert_argument(p) for p in arguments_or_e],
            "returns": [_assert_payload(p) for p in returns_or_payload],
        }
    )

    if docstring is not None:
        _callable["docstring"] = docstring

    return _callable


def _assert_payload(data: Any) -> APIParameterType:
    """
    Asserts the validity of a payload data structure.

    Args:
        data: The data representing a payload.

    Returns:
        A validated payload structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) in [4, 5, 6]

    payload = _assert_parameter(
        data[0],
        data[1],
        data[3],
        data[4] if len(data) > 4 else None,
        data[2],
        data[5] if len(data) == 6 else None,
    )

    return payload


def _assert_argument(data: Any) -> APIParameterType:
    """
    Asserts the validity of an argument data structure.

    Args:
        data: The data representing an argument.

    Returns:
        A validated argument structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    assert isinstance(data, list)
    assert len(data) in [4, 5]

    argument = _assert_parameter(
        data[0], data[1], data[3], None, data[2], data[4] if len(data) == 5 else None
    )

    return argument


def rebuild_documentation(data: Any) -> APIDocumentation:
    """
    Rebuilds the API documentation structure.

    Args:
        data: The data representing the API documentation.

    Returns:
        The rebuilt API documentation structure.

    Raises:
        AssertionError: If the data structure does not meet the expected format.
    """
    api_documentation = _assert_api_documentation(data)

    api_types = api_documentation["types"]

    def resolve_parameter_types(parameters: list[APIParameterType]):
        for parameter in parameters:
            parameter["type_name"] = api_types[int(parameter["type_name"])]["name"]

    for api_type in api_types:
        if "arguments" in api_type:
            resolve_parameter_types(api_type["arguments"])
        elif "fields" in api_type:
            resolve_parameter_types(api_type["fields"])

    for api_callable_group in api_documentation["callables"]:
        for api_callables in api_callable_group["items"]:
            resolve_parameter_types(api_callables["arguments"])
            resolve_parameter_types(api_callables["returns"])

    for api_callable_group in api_documentation["events"]:
        for api_callables in api_callable_group["items"]:
            resolve_parameter_types(api_callables["payload"])

    return api_documentation
