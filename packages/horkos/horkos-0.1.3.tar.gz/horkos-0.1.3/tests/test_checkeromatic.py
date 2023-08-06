import json
import typing
from unittest import mock
import uuid

import pytest

from horkos import _checkeromatic


def test_json_string_checker_happy_path():
    """Should be able check a valid json string."""
    value = json.dumps({'foo': 'bar'})
    checker = _checkeromatic.JsonStringChecker()

    passes = checker(value)

    assert passes


def test_json_string_checker_bad_json():
    """Should be able check an invalid json string."""
    checker = _checkeromatic.JsonStringChecker()

    passes = checker('<xml></xml>')

    assert not passes


def test_json_array_string_checker_happy_path():
    """Should be able check a valid json array string."""
    value = json.dumps(['foo', 'bar'])
    checker = _checkeromatic.JsonArrayStringChecker()

    passes = checker(value)

    assert passes


def test_json_object_string_checker_happy_path():
    """Should be able check a valid json object string."""
    value = json.dumps({'foo': 'bar'})
    checker = _checkeromatic.JsonObjectStringChecker()

    passes = checker(value)

    assert passes


def test_json_string_checker_wrong_type():
    """Should be able check a value of the wrong type."""
    checker = _checkeromatic.JsonStringChecker()

    passes = checker(12)

    assert not passes


def test_choice_checker_happy_path():
    """
    Should be able to check that a value is within a valid set of
    choices.
    """
    checker = _checkeromatic.ChoiceChecker(options=['foo', 'bar'])

    passes = checker('foo')

    assert passes


def test_choice_checker_bad_value():
    """
    Should be able to see that a value is not within a valid set of
    choices.
    """
    checker = _checkeromatic.ChoiceChecker(options=['foo', 'bar'])

    passes = checker('fizbuzz')

    assert not passes


def test_email_checker_happy_path():
    """Should be able to validate an email."""
    checker = _checkeromatic.EmailChecker()

    passes = checker('could.be@an-email.com')

    assert passes


def test_email_checker_bad_value():
    """Should be able to identify an invalid email."""
    checker = _checkeromatic.EmailChecker()

    passes = checker('for-sure-not-valid')

    assert not passes


def test_uuid_checker_happy_path():
    """Should be able to validate a uuid."""
    value = str(uuid.uuid4())
    checker = _checkeromatic.UuidChecker()

    passes = checker(value)

    assert passes


def test_uuid_checker_bad_value():
    """Should be able to identify a non-uuid."""
    value = '398l159z-8m4n-455o-pqr0-75s66tu074jk'
    checker = _checkeromatic.UuidChecker()

    passes = checker(value)

    assert not passes


def test_iso_timestamp_checker_happy_path():
    """Should be able to identify a iso compliant timestamp."""
    value = '2020-03-18T12:34:56'
    checker = _checkeromatic.IsoTimestampChecker()

    passes = checker(value)

    assert passes


def test_max_checker_happy_path():
    """Should be able to identify a value less than the limit."""
    value = 0.5
    checker = _checkeromatic.MaxChecker(limit=1)

    passes = checker(value)

    assert passes


def test_min_checker_happy_path():
    """Should be able to identify a value greater than the limit."""
    value = 1
    checker = _checkeromatic.MinChecker(limit=1)

    passes = checker(value)

    assert passes


@mock.patch('json.loads')
def test_keyboard_interupts_surface(loads: mock.MagicMock):
    """A keyboard interupt should always get reraised."""
    loads.side_effect = KeyboardInterrupt
    checker = _checkeromatic.JsonStringChecker()

    with pytest.raises(KeyboardInterrupt):
        checker('some-value')


JSON_CHECKERS = [
    (_checkeromatic.JsonStringChecker, json.dumps({'f': float('NaN')})),
    (_checkeromatic.JsonObjectStringChecker, json.dumps({'f': float('NaN')})),
    (_checkeromatic.JsonArrayStringChecker, json.dumps([float('NaN')])),
]


@pytest.mark.parametrize('checker_cls,value', JSON_CHECKERS)
def test_json_checker_doesnt_tolerate_nan(
        checker_cls: typing.Callable,
        value: str,
):
    """Should fail to validate json with Nans."""
    value = json.dumps({'foo': float('NaN')})
    checker = checker_cls()

    passes = checker(value)

    assert not passes


def test_max_length_checker_happy_path():
    """Should be able to validate a string within the max length."""
    value = 'short'
    checker = _checkeromatic.MaxLengthChecker(limit=10)

    passes = checker(value)

    assert passes


def test_max_length_checker_sad_path():
    """Should be able to reject a string outside the max length."""
    value = 'very-very-very-very-long'
    checker = _checkeromatic.MaxLengthChecker(limit=10)

    passes = checker(value)

    assert not passes
