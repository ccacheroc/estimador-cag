"""Composición de la API FastAPI."""

from fastapi import FastAPI

from app.http_errors import normalize_problem_openapi, register_exception_handlers
from app.routers.estimations import router as estimations_router


app = FastAPI(
    title="Estimador CAG",
    description=(
        "API para generar estimaciones de proyectos de software a partir de "
        "transcripciones de reuniones, usando ejemplos previos como contexto CAG."
    ),
)
register_exception_handlers(app)
app.include_router(estimations_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Confirma que el proceso de la API responde."""
    return {"status": "ok"}


normalize_problem_openapi(app.openapi())
