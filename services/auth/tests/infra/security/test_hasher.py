import pytest

from services.auth.infra.security.hasher import PasswordHasher


@pytest.fixture
def hasher():
    return PasswordHasher()


def test_hash_returns_different_value_than_plaintext(hasher):
    password = "my-secret-password"

    hashed = hasher.hash(password)

    assert isinstance(hashed, str)
    assert hashed != password
    assert hashed.startswith("$2") 


def test_verify_returns_true_for_correct_password(hasher):
    password = "another-secret"
    hashed = hasher.hash(password)

    assert hasher.verify(password, hashed) is True


def test_verify_returns_false_for_wrong_password(hasher):
    password = "correct-password"
    hashed = hasher.hash(password)

    assert hasher.verify("wrong-password", hashed) is False


def test_hash_generates_unique_hashes_for_same_password(hasher):
    password = "same-password"

    h1 = hasher.hash(password)
    h2 = hasher.hash(password)

    assert h1 != h2
    assert hasher.verify(password, h1) is True
    assert hasher.verify(password, h2) is True
