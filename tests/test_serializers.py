import pytest
from src.logstack.serializers import LogSerializer

fields_config = LogSerializer.FIELDS_CONFIG

def test_log_serializer_required_validation():
    data = dict()
    for key, value in fields_config.items():
        if not value.get('required'):
            data[key] = value.get('default')

    with pytest.raises(AttributeError) as ex:
        log = LogSerializer(data=data)
    assert 'is required but not provided in data' in str(ex.value)

def test_log_serializer_type_validation():
    with pytest.raises(TypeError) as ex:
        log = LogSerializer()
        log.__validate_types(str, 'example', 10)

    expected_type = type(str)
    field_type = type(10)
    assert f"Expected {expected_type} but got {field_type}"
