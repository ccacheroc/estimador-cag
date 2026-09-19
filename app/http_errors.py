"""Translate framework exceptions into RFC 9457 Problem Details responses."""

import logging
from dataclasses import dataclass
from typing import cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.schemas.problem import (
    ProblemDetails,
    ValidationIssue,
    ValidationProblemDetails,
)

PROBLEM_MEDIA_TYPE = "application/problem+json"
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProblemMetadata:
    type: str
    title: str
    default_detail: str


HTTP_PROBLEMS: dict[int, ProblemMetadata] = {
    404: ProblemMetadata(
        type="urn:estimador-cag:problem:http-404",
        title="Recurso no encontrado",
        default_detail="La ruta solicitada no existe.",
    ),
    405: ProblemMetadata(
        type="urn:estimador-cag:problem:http-405",
        title="Método no permitido",
        default_detail="El método HTTP no está permitido para esta ruta.",
    ),
    502: ProblemMetadata(
        type="urn:estimador-cag:problem:provider-error",
        title="Error del proveedor",
        default_detail="No se pudo generar la estimación.",
    ),
    503: ProblemMetadata(
        type="urn:estimador-cag:problem:configuration-error",
        title="Servicio no disponible",
        default_detail="La configuración del servicio no está disponible.",
    ),
}


def _problem_response(problem: ProblemDetails) -> JSONResponse:
    return JSONResponse(
        status_code=problem.status,
        content=problem.model_dump(mode="json", exclude_none=True),
        media_type=PROBLEM_MEDIA_TYPE,
    )


def _object_dict(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError("Expected an object while normalizing OpenAPI.")
    return cast(dict[str, object], value)


def normalize_problem_openapi(schema: object) -> None:
    paths = _object_dict(_object_dict(schema)["paths"])
    operation = _object_dict(
        _object_dict(_object_dict(paths["/api/v1/estimate"])["post"])
    )
    responses = _object_dict(operation["responses"])
    for status in ("422", "500", "502", "503"):
        response = _object_dict(responses[status])
        content = _object_dict(response["content"])
        json_media = _object_dict(content.pop("application/json"))
        problem_media = _object_dict(content[PROBLEM_MEDIA_TYPE])
        problem_media["schema"] = json_media["schema"]


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    issues = [
        ValidationIssue(
            location=list(error["loc"]),
            code=error["type"],
        )
        for error in exc.errors()
    ]
    return _problem_response(
        ValidationProblemDetails(
            type="urn:estimador-cag:problem:validation-error",
            title="Petición no válida",
            status=422,
            detail="La petición no cumple el contrato esperado.",
            errors=issues,
        )
    )


async def http_exception_handler(
    _request: Request, exc: HTTPException
) -> JSONResponse:
    metadata = HTTP_PROBLEMS.get(
        exc.status_code,
        ProblemMetadata(
            type=f"urn:estimador-cag:problem:http-{exc.status_code}",
            title=f"Error HTTP {exc.status_code}",
            default_detail="La petición no pudo completarse.",
        ),
    )
    detail = (
        metadata.default_detail if exc.status_code in {404, 405} else exc.detail
    )
    response = _problem_response(
        ProblemDetails(
            type=metadata.type,
            title=metadata.title,
            status=exc.status_code,
            detail=detail,
        )
    )
    response.headers.update(exc.headers or {})
    return response


async def unexpected_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error(
        "unhandled_http_error",
        extra={"event": "unhandled_http_error", "path": request.url.path},
        exc_info=exc,
    )
    return _problem_response(
        ProblemDetails(
            type="urn:estimador-cag:problem:internal-error",
            title="Error interno del servidor",
            status=500,
            detail="La petición no pudo completarse.",
        )
    )


def register_exception_handlers(app: FastAPI) -> None:
    # FastAPI dispatches each handler only for its registered exception subtype.
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,  # pyright: ignore[reportArgumentType]
    )
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,  # pyright: ignore[reportArgumentType]
    )
    app.add_exception_handler(Exception, unexpected_exception_handler)
