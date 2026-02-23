import pytest
from services.auth.domain.models import EmailAddress
from services.auth.domain.exc import ValidationError


@pytest.mark.parametrize(
    ["row_email", "expected"],
    [
        pytest.param("Test@example.com", "test@example.com", id="uppercase-in-email"),
        pytest.param(
            "      test@example.com  ", "test@example.com", id="strip-whitespace"
        ),
        pytest.param(
            "Test.test-test+TeSt@Example.COM",
            "test.test-test+test@example.com",
            id="mixed-case-plus-tag",
        ),
        pytest.param(
            "user@subdomain.example.com",
            "user@subdomain.example.com",
            id="with-subdomain",
        ),
    ],
)
def test_good_emails(row_email, expected):
    email = EmailAddress(row_email)
    assert email.value == expected


@pytest.mark.parametrize(
    "invalid_email",
    [
        pytest.param("", id="empty-string"),
        pytest.param("   ", id="only-whitespace"),
        pytest.param("some.address", id="missing-at"),
        pytest.param("test@.com", id="missing-domain"),
        pytest.param("@example.com", id="missing-path"),
        pytest.param("test@example", id="missing-tld"),
        pytest.param("test@@example.com", id="double-at"),
        pytest.param("test test@example.com", id="space-in-path"),
    ],
)
def test_invalid_emails(invalid_email):

    with pytest.raises(ValidationError) as exc_info:
        EmailAddress(invalid_email)

    err = exc_info.value
    assert isinstance(err, ValidationError)
    assert err.errors
    assert err.errors.get("email")
