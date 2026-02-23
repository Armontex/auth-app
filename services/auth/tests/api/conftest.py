import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from contextlib import asynccontextmanager
from main import create_app


@pytest.fixture
def app_for_tests() -> FastAPI:
    app = create_app()

    @asynccontextmanager
    async def fake_lifespan(app: FastAPI):
        yield

    app.router.lifespan_context = fake_lifespan
    return app


@pytest.fixture
def client(app_for_tests):
    with TestClient(app_for_tests) as c:
        yield c
