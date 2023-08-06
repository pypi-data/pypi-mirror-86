import dataclasses

import pytest

from horkos import _casters
from horkos import _definitions
from horkos import errors


def test_cast_happy_path():
    """Should be able to cast each of a records values to its expected type."""
    bool_field = _definitions.Field(
        name='bool_field',
        type_='boolean',
        description='Some description',
        required=True,
        nullable=False,
        checks={},
        labels={},
    )
    field_map = {
        'bool_field_1': dataclasses.replace(bool_field, name='bool_field_1'),
        'bool_field_2': dataclasses.replace(bool_field, name='bool_field_2'),
        'bool_field_3': dataclasses.replace(bool_field, name='bool_field_3'),
        'bool_field_4': dataclasses.replace(bool_field, name='bool_field_4'),
        'bool_field_5': dataclasses.replace(bool_field, name='bool_field_5'),
        'int_field': _definitions.Field(
            name='int_field',
            type_='integer',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'str_field': _definitions.Field(
            name='str_field',
            type_='string',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
    }
    record = {
        'bool_field_1': 'true',
        'bool_field_2': 'False',
        'bool_field_3': 1,
        'bool_field_4': 0,
        'bool_field_5': True,
        'int_field': '123',
        'str_field': 12345
    }

    cast = _casters.cast(record, field_map)

    assert cast['bool_field_1'] is True
    assert cast['bool_field_2'] is False
    assert cast['bool_field_3'] is True
    assert cast['bool_field_4'] is False
    assert cast['bool_field_5'] is True
    assert cast['int_field'] == 123
    assert cast['str_field'] == '12345'


def test_cast_raises_all_errors():
    """Should raise all errors when present."""
    field_map = {
        'bool_field': _definitions.Field(
            name='bool_field',
            type_='boolean',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'float_field': _definitions.Field(
            name='float_field',
            type_='float',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'int_field_1': _definitions.Field(
            name='int_field_1',
            type_='integer',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'int_field_2': _definitions.Field(
            name='int_field_2',
            type_='integer',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'str_field_1': _definitions.Field(
            name='str_field_1',
            type_='string',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'str_field_2': _definitions.Field(
            name='str_field_2',
            type_='string',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
    }
    record = {
        'bool_field': 'T',
        'float_field': 'word',
        'int_field_1': 1.123,
        'int_field_2': 'word',
        'str_field_1': None,
    }

    with pytest.raises(errors.RecordValidationError) as err:
        _casters.cast(record, field_map)

    msg = 'value of "T" for bool_field could not be cast to boolean'
    assert msg in str(err.value)
    msg = 'value of "word" for float_field could not be cast to float'
    assert msg in str(err.value)
    msg = 'value of "1.123" for int_field_1 could not be cast to integer'
    assert msg in str(err.value)
    msg = 'value of "word" for int_field_2 could not be cast to integer'
    assert msg in str(err.value)
    msg = 'str_field_1 cannot be null'
    assert msg in str(err.value)
    msg = 'str_field_2 is required'
    assert msg in str(err.value)


def test_str_less_aggressive():
    """The string caster in _casters should not aggressively cast to strings."""
    value = {'foo': 'bar'}

    with pytest.raises(ValueError) as err:
        _casters._str(value)

    msg = "Cannot unambiguously convert {'foo': 'bar'} to a string"
    assert msg in str(err.value)
