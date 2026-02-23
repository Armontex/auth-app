import pytest

from services.auth.domain.models import RegisterForm, EmailAddress, Password
from services.auth.domain.exc import ValidationError


def test_register_form_ok():
    email = EmailAddress("user@example.com")
    password = Password("super-secret-password")
    form = RegisterForm(email=email, password=password, confirm_password=password.value)

    assert form.email is email
    assert form.password is password
    assert form.confirm_password == password.value


@pytest.mark.parametrize(
    "password_value, confirm_value",
    [
        pytest.param("secret-1", "secret-2", id="different-values"),
        pytest.param("secret-1", "", id="empty-confirm"),
        pytest.param("secret-1", "secret-1 ", id="extra-space"),
    ],
)
def test_register_form_passwords_do_not_match(password_value, confirm_value):
    email = EmailAddress("user@example.com")
    password = Password(password_value)

    with pytest.raises(ValidationError) as exc_info:
        RegisterForm(email=email, password=password, confirm_password=confirm_value)

    err = exc_info.value
    assert isinstance(err, ValidationError)
    assert err.errors
    messages = err.errors.get("password")
    assert messages
    assert "passwords do not match" in messages
