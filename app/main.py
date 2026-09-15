"""Composición de la API FastAPI."""

from fastapi import FastAPI

from app.routers.estimations import router as estimations_router


app = FastAPI(
    title="Estimador CAG",
    description=(
        "API para generar estimaciones de proyectos de software a partir de "
        "transcripciones de reuniones, usando ejemplos previos como contexto CAG."
    ),
)
app.include_router(estimations_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Confirma que el proceso de la API responde."""
    return {"status": "ok"}
