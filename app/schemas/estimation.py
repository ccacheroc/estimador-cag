"""Schemas Pydantic para el endpoint de estimación."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


#tipos de los objetos que recibe y devuelve el router, que actúa de adaptador entre la API y el servicio de estimación. 
class EstimationRequest(BaseModel):
    transcription: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class TokenUsageResponse(BaseModel):
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)
    cached_input_tokens: int = Field(ge=0)


class EstimationResponse(BaseModel):
    estimation: str
    model: str
    provider: str
    tokens_used: TokenUsageResponse | None
    estimated_cost_usd: float | None = Field(ge=0)
    timestamp: datetime
    response_id: str | None
