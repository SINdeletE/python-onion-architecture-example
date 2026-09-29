from fastapi import FastAPI
from sqlalchemy import text

from api.rest.v1.controllers import v1_router
from api.rest.v1.di import AsyncSessionDep, database_lifespan
from api.rest.v1.handlers import initialize_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(
        title="To-Do Router API",
        version="1.0.0",
        lifespan=database_lifespan
    )
    initialize_exception_handlers(app)
    app.include_router(v1_router, prefix="/api/v1")

    @app.get("/health", include_in_schema=False)
    async def health(session: AsyncSessionDep) -> dict[str, str]:
        await session.execute(text("SELECT 1"))
        return {"status": "ok"}

    return app

app = create_app()
