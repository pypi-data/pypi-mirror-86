from pytest import mark

from kuber import definitions
from kuber.latest import core_v1


def test_definition_serialization():
    """Should create a Definition object and serialize as expected."""
    d = definitions.Definition('1.11', 'Deployment')
    d._properties = {'foo': 1, 'bar': None, 'baz': 'hello'}
    d._types = {'bar': (float, None), 'baz': (str, None)}

    serialized = d.to_dict()
    assert {'baz': 'hello'} == serialized
    assert d.kuber_uid is not None


DESERIALIZATION_SCENARIOS = [
    {'fooBar': 1, 'barFoo': None, 'barBaz': 'hello', 'BAZQux': True},
    {'foo_bar': 1, 'bar_foo': None, 'bar_baz': 'hello', 'baz_qux': True},
    {'FOOBAR': 1, 'bar_foo': None, 'BARBAZ': 'hello', 'BAZQUX': True},
]


@mark.parametrize('scenario', DESERIALIZATION_SCENARIOS)
def test_definition_deserialization(scenario: dict):
    """Should create a Definition object populated from the serialized data."""
    d = definitions.Definition('1.11', 'Deployment')
    d._types = {
        'fooBar': (float, None),
        'barBaz': (str, None),
        'BAZQux': (bool, None)
    }
    expected = {'barBaz': 'hello', 'fooBar': 1, 'BAZQux': True}
    assert expected == d.from_dict({'a': 1, 'b': 2, **scenario})._properties


def test_collection_yaml_serialization():
    """Should serialize the Collection to a YAML string."""
    pod_list = core_v1.PodList()
    pod_list.metadata.resource_version = 'foo'
    assert 'foo' in pod_list.to_yaml()


def test_collection_json_serialization():
    """Should serialize the Collection to a JSON string."""
    namespace_list = core_v1.NamespaceList()
    namespace_list.metadata.resource_version = 'foo'
    assert 'foo' in namespace_list.to_json()


SCENARIOS = [
    ('foo_bar_baz', 'fooBarBaz'),
    ('foo-bar-baz', 'fooBarBaz'),
    ('fooBarBaz', 'fooBarBaz')
]


@mark.parametrize('source, expected', SCENARIOS)
def test_to_camel_case(source: str, expected: str):
    """Should convert the source string to the expected camelCase result."""
    assert expected == definitions.to_camel_case(source)
