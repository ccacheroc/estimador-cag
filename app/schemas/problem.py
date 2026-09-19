"""RFC 9457 Problem Details contracts for HTTP API errors."""

from pydantic import BaseModel, Field


class ProblemDetails(BaseModel):
    type: str
    title: str
    status: int = Field(ge=400, le=599)
    detail: str
    instance: str | None = None


class ValidationIssue(BaseModel):
    location: list[str | int]
    code: str


class ValidationProblemDetails(ProblemDetails):
    errors: list[ValidationIssue]
