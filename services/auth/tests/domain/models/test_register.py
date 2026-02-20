import pytest
import services.auth.domain.models.register as rf


def _extract_errors(exc: rf.DomainValidationError) -> dict:
    if hasattr(exc, "errors") and isinstance(getattr(exc, "errors"), dict):
        return exc.errors
    if getattr(exc, "args", None) and isinstance(exc.args[0], dict):
        return exc.args[0]
    raise AssertionError(f"Cannot extract errors dict from {exc!r}")


def _valid_form_kwargs(**overrides):
    base = {
        "email": object(),
        "password": "a" * rf.PASSWORD_MIN_LENGTH,
        "confirm_password": "a" * rf.PASSWORD_MIN_LENGTH,
    }
    base.update(overrides)
    return base


def test_valid_form_ok():
    rf.RegisterForm(**_valid_form_kwargs())


def test_password_too_short_error_only_short():
    short = "a" * (rf.PASSWORD_MIN_LENGTH - 1)

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(password=short, confirm_password=short))

    errors = _extract_errors(exc_info.value)
    assert "password" in errors
    assert f"too short (min {rf.PASSWORD_MIN_LENGTH})" in errors["password"]


def test_password_cannot_start_with_space():
    p = " " + ("a" * (rf.PASSWORD_MIN_LENGTH - 1))

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(password=p, confirm_password=p))

    errors = _extract_errors(exc_info.value)
    assert "password" in errors
    assert "cannot start with a space" in errors["password"]


def test_password_cannot_end_with_space():
    p = ("a" * (rf.PASSWORD_MIN_LENGTH - 1)) + " "

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(password=p, confirm_password=p))

    errors = _extract_errors(exc_info.value)
    assert "password" in errors
    assert "cannot end with a space" in errors["password"]


def test_password_too_long_error():
    p = "a" * (rf.PASSWORD_MAX_LENGTH + 1)

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(password=p, confirm_password=p))

    errors = _extract_errors(exc_info.value)
    assert "password" in errors
    assert f"too long (max {rf.PASSWORD_MAX_LENGTH})" in errors["password"]


def test_confirm_password_empty_gives_two_errors():
    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(confirm_password=""))

    errors = _extract_errors(exc_info.value)
    assert "confirm_password" in errors
    assert "cannot be empty" in errors["confirm_password"]
    assert "passwords do not match" in errors["confirm_password"]


def test_confirm_password_mismatch_error():
    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(
            **_valid_form_kwargs(confirm_password="b" * rf.PASSWORD_MIN_LENGTH)
        )

    errors = _extract_errors(exc_info.value)
    assert "confirm_password" in errors
    assert "passwords do not match" in errors["confirm_password"]


def test_multiple_fields_errors_collected():
    short = "a" * (rf.PASSWORD_MIN_LENGTH - 1)

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(
            **_valid_form_kwargs(
                password=short,
                confirm_password="",
            )
        )

    errors = _extract_errors(exc_info.value)
    assert set(errors.keys()) >= {
        "password",
        "confirm_password",
    }
