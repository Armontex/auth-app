import pytest
import services.auth.domain.models.register as rf


def _extract_errors(exc: rf.DomainValidationError) -> dict:
    if hasattr(exc, "errors") and isinstance(getattr(exc, "errors"), dict):
        return exc.errors
    if getattr(exc, "args", None) and isinstance(exc.args[0], dict):
        return exc.args[0]
    raise AssertionError(f"Cannot extract errors dict from {exc!r}")


def _allowed_name_char() -> str:
    for ch in rf.VALID_NAME_SYMBOLS:
        if isinstance(ch, str) and ch and not ch.isspace():
            return ch
    return "A"


def _valid_form_kwargs(**overrides):
    c = _allowed_name_char()
    base = {
        "first_name": f"{c}lex",
        "last_name": f"{c}mith",
        "middle_name": None,
        "email": object(),
        "password": "a" * rf.PASSWORD_MIN_LENGTH,
        "confirm_password": "a" * rf.PASSWORD_MIN_LENGTH,
    }
    base.update(overrides)
    return base


def test_valid_form_ok():
    rf.RegisterForm(**_valid_form_kwargs())


def test_first_name_empty_error():
    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(first_name=""))

    errors = _extract_errors(exc_info.value)
    assert "first_name" in errors
    assert "cannot be empty" in errors["first_name"]


def test_last_name_too_long_error():
    c = _allowed_name_char()
    too_long = c * (rf.NAME_MAX_LENGTH + 1)

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(last_name=too_long))

    errors = _extract_errors(exc_info.value)
    assert "last_name" in errors
    assert f"too long (max {rf.NAME_MAX_LENGTH})" in errors["last_name"]


def test_middle_name_none_no_error_key():
    rf.RegisterForm(**_valid_form_kwargs(middle_name=None))


def test_middle_name_invalid_char_error():
    c = _allowed_name_char()
    bad = f"{c}💥"

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(**_valid_form_kwargs(middle_name=bad))

    errors = _extract_errors(exc_info.value)
    assert "middle_name" in errors
    assert "Invalid character '💥'" in errors["middle_name"]


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
    c = _allowed_name_char()
    bad_name = f"{c}💥"
    short = "a" * (rf.PASSWORD_MIN_LENGTH - 1)

    with pytest.raises(rf.DomainValidationError) as exc_info:
        rf.RegisterForm(
            **_valid_form_kwargs(
                first_name=bad_name,
                last_name="",
                password=short,
                confirm_password="",
            )
        )

    errors = _extract_errors(exc_info.value)
    assert set(errors.keys()) >= {
        "first_name",
        "last_name",
        "password",
        "confirm_password",
    }
