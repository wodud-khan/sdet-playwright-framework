"""FastAPI entry point for the controlled portfolio system under test."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from demo_app.database import Database
from demo_app.repository import OrderRepository
from demo_app.schemas import HealthResponse, OrderCreate, OrderResponse

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app(database_url: str | None = None) -> FastAPI:
    """Create an application using an explicit or environment-provided database."""
    configured_url = database_url
    if configured_url is None:
        configured_url = os.environ.get(
            "DATABASE_URL",
            "postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio",
        )
    database = Database(configured_url)
    repository = OrderRepository(database)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        database.initialize()
        yield

    app = FastAPI(
        title="SDET Portfolio Demo API",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.state.database = database
    app.state.order_repository = repository
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        if not database.is_healthy():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is unavailable",
            )
        return HealthResponse(status="ok", database="ok")

    @app.post(
        "/api/orders",
        response_model=OrderResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_order(payload: OrderCreate) -> OrderResponse:
        return repository.create(payload)

    @app.get("/api/orders/{order_id}", response_model=OrderResponse)
    def get_order(order_id: str) -> OrderResponse:
        order = repository.get(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return order

    @app.delete(
        "/api/orders/{order_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_order(order_id: str) -> Response:
        if not repository.delete(order_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
