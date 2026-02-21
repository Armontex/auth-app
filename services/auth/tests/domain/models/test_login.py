import pytest
from services.auth.domain.models import LoginForm
from services.auth.domain.exc import ValidationError
from unittest.mock import Mock


@pytest.mark.parametrize(
    "email, password, expected_error",
    [
        pytest.param(Mock(), "123123", False, id="valid-form"),
        pytest.param(Mock(), "", True, id="empty-password"),
        pytest.param(Mock(), "    ", True, id="only-whitespace-in-password"),
    ],
)
def test_login_form(email, password, expected_error):

    if expected_error:
        with pytest.raises(ValidationError):
            LoginForm(email=email, password=password)
    else:
        form = LoginForm(email=email, password=password)
        assert form.email == email and form.password == password
