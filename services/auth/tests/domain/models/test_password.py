import pytest

from services.auth.domain.models import Password
from services.auth.domain.const import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
from services.auth.domain.exc import ValidationError


@pytest.mark.parametrize(
    "raw_password",
    [
        pytest.param("a" * PASSWORD_MIN_LENGTH, id="min-length"),
        pytest.param("a" * (PASSWORD_MIN_LENGTH + 5), id="middle-length"),
        pytest.param("abc def ghi", id="inner-space"),
        pytest.param("a" * PASSWORD_MAX_LENGTH, id="max-length"),
    ],
)
def test_good_passwords(raw_password):
    password = Password(raw_password)
    assert password.value == raw_password


@pytest.mark.parametrize(
    "raw_password",
    [
        pytest.param("a" * (PASSWORD_MIN_LENGTH - 1), id="too-short"),
        pytest.param("", id="empty-string"),
    ],
)
def test_too_short_passwords(raw_password):
    with pytest.raises(ValidationError) as exc_info:
        Password(raw_password)

    err = exc_info.value
    assert isinstance(err, ValidationError)
    assert err.errors
    messages = err.errors.get("password")
    assert messages
    assert any(f"too short (min {PASSWORD_MIN_LENGTH})" in m for m in messages)


@pytest.mark.parametrize(
    "raw_password, field",
    [
        pytest.param(
            " " + "a" * PASSWORD_MIN_LENGTH,
            "cannot start with a space",
            id="start-space",
        ),
        pytest.param(
            "a" * PASSWORD_MIN_LENGTH + " ", "cannot end with a space", id="end-space"
        ),
        pytest.param(
            " " + "a" * PASSWORD_MIN_LENGTH + " ",
            " both-sides-space ",
            id="both-sides-space",
        ),
    ],
)
def test_password_spaces(raw_password, field):
    with pytest.raises(ValidationError) as exc_info:
        Password(raw_password)

    err = exc_info.value
    assert isinstance(err, ValidationError)
    assert err.errors
    messages = err.errors.get("password")
    assert messages


@pytest.mark.parametrize(
    "raw_password",
    [
        pytest.param("a" * (PASSWORD_MAX_LENGTH + 1), id="too-long"),
        pytest.param(
            " " + "a" * (PASSWORD_MAX_LENGTH + 1) + " ", id="too-long-with-spaces"
        ),
    ],
)
def test_too_long_passwords(raw_password):
    with pytest.raises(ValidationError) as exc_info:
        Password(raw_password)

    err = exc_info.value
    assert isinstance(err, ValidationError)
    assert err.errors
    messages = err.errors.get("password")
    assert messages
    assert any(f"too long (max {PASSWORD_MAX_LENGTH})" in m for m in messages)
