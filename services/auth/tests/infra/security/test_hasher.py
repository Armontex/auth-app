import pytest

from services.auth.infra.security.hasher import PasswordHasher


@pytest.fixture
def hasher():
    return PasswordHasher()


def test_hash_returns_non_empty_string(hasher):
    password = "secret123"

    hashed = hasher.hash(password)

    assert isinstance(hashed, str)
    assert hashed != ""


def test_verify_success(hasher):
    password = "secret123"
    hashed = hasher.hash(password)

    assert hasher.verify(password, hashed) is True


def test_verify_failure(hasher):
    password = "secret123"
    other_password = "wrong-password"
    hashed = hasher.hash(password)

    assert hasher.verify(other_password, hashed) is False
