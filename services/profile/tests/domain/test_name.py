import pytest

from services.profile.domain.models import Name
from services.profile.domain.const import NAME_MAX_LENGTH
from services.profile.domain.exc import ValidationError
from services.profile.domain.utils import VALID_NAME_SYMBOLS


def test_name_valid_value():
    value = "John"

    name = Name(value)

    assert name.value == value


def test_name_empty_string_raises_validation_error():
    with pytest.raises(ValidationError) as exc_info:
        Name("")

    err = exc_info.value
    assert err.errors == {"value": ["cannot be empty"]}


def test_name_too_long_raises_validation_error():
    value = "a" * (NAME_MAX_LENGTH + 1)

    with pytest.raises(ValidationError) as exc_info:
        Name(value)

    err = exc_info.value
    assert "value" in err.errors
    assert f"too long (max {NAME_MAX_LENGTH})" in err.errors["value"]


def test_name_invalid_characters_collect_errors():
    value = "John!#"

    with pytest.raises(ValidationError) as exc_info:
        Name(value)

    err = exc_info.value
    messages = err.errors.get("value")
    assert messages
    assert "Invalid character '!'" in messages
    assert "Invalid character '#'" in messages


def test_name_valid_symbols_no_invalid_character_errors():

    sample = "".join(list(VALID_NAME_SYMBOLS)[:5]) or "abcde"

    name = Name(sample)

    assert name.value == sample
