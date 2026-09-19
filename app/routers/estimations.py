"""Ruta HTTP para estimar proyectos a partir de una reunión."""

from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from openai import OpenAIError

from app.schemas.estimation import EstimationRequest, EstimationResponse
from app.schemas.problem import ProblemDetails, ValidationProblemDetails
from app.services.llm_service import generate_estimation_details


router = APIRouter(tags=["estimations"])


@router.post(
    "/estimate",
    response_model=EstimationResponse,
    responses={
        422: {
            "model": ValidationProblemDetails,
            "description": "La petición no cumple el contrato esperado.",
            "content": {"application/problem+json": {}},
        },
        502: {
            "model": ProblemDetails,
            "description": "El proveedor no pudo generar una estimación.",
            "content": {"application/problem+json": {}},
        },
        500: {
            "model": ProblemDetails,
            "description": "La petición falló de forma inesperada.",
            "content": {"application/problem+json": {}},
        },
        503: {
            "model": ProblemDetails,
            "description": "La configuración impide atender la petición.",
            "content": {"application/problem+json": {}},
        },
    },
)
async def estimate(request: EstimationRequest) -> EstimationResponse:
    try:
        result = await generate_estimation_details(request.transcription)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except (OpenAIError, RuntimeError) as exc:
        raise HTTPException(status_code=502, detail="No se pudo generar la estimación.") from exc

    return EstimationResponse.model_validate(asdict(result))
