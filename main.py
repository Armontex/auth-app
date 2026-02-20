from fastapi import FastAPI
from api.v1.routers import api_router
from config.settings import settings
from lifespan import lifespan


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.debug, lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()