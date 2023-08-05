from typing import Union


def attach_namespace(namespace_or_context: Union[str, dict], response_map: dict) -> dict:
    """
    Attaches the given namespace to the response map

    Example:
        >>> attach_namespace('echo', {'response' : 'hello world'})
        {'@echo': {'response': 'hello world'}}
        >>> attach_namespace({'namespace' : 'echo.incoming'}, {'response' : 'hello world'})
        {'@echo': {'response': 'hello world'}}

    :param namespace_or_context: either a string specifying the namespace or the evaluation context
    :param response_map:
    :return:
    """
    if type(namespace_or_context) == str:
        return {'@{}'.format(namespace_or_context): response_map}
    if type(namespace_or_context) == dict:
        extracted_ns = namespace_or_context.get("namespace")

        if extracted_ns is None:
            _raise_on_missing_namespace(namespace_or_context)

        parent_ns = extracted_ns.split('.')[0]
        return attach_namespace(parent_ns, response_map)
    raise TypeError('Can not extract namespace from the given type {}'.format(type(namespace_or_context)))


def is_namespace(context: dict, namespace: str):
    """
    Checks is the current context is in the given namespace.
    :raises Exception if a invalid context is passed

    Example:
        >>> is_namespace({'namespace': 'test.incoming'}, 'test')
        True
        >>> is_namespace({'namespace': '`test`.incoming'}, 'test')
        True

    :param context:
    :param namespace:
    :return:
    """
    _check_context(context)
    ns = context.get("namespace")
    if ns is None:
        _raise_on_missing_namespace(context)
    relevant_namespace = _extract_relevant(ns)
    return namespace == relevant_namespace or "`{}`".format(namespace) == relevant_namespace


def _extract_relevant(namespace: str) -> str:
    """
    Extracts the relevant part of a full namespace
    Given the namespace 'test.incoming' => 'test'
    :param namespace:
    :return:
    """
    if namespace is None:
        raise TypeError('None is not a valid namespace')
    split = namespace.split(".")
    return split[0]


# side effects:
def _raise_on_missing_namespace(corrupted_context):
    raise Exception(
        'The passed context does not contain a namespace - did you really pass the evaluation context?\ncontext={}'.format(
            corrupted_context))


def _check_context(context):
    if type(context) != dict:
        raise TypeError("'{}' is not an evaluation context!".format(context))
