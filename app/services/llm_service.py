"""Construcción del prompt CAG y generación de estimaciones con OpenAI."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from textwrap import dedent

from openai import AsyncOpenAI

from app.config import TOKENS_PER_MILLION, get_model_rates, get_settings
from app.context.examples import ESTIMATION_EXAMPLES


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cached_input_tokens: int


@dataclass(frozen=True)
class EstimationResult:
    estimation: str
    model: str
    provider: str
    tokens_used: TokenUsage | None
    estimated_cost_usd: float | None
    timestamp: datetime
    response_id: str | None


def build_system_prompt() -> str:
    """Incluye las instrucciones y todos los ejemplos históricos en un único mensaje."""
    instructions = dedent("""\
        Eres un estimador de proyectos de software experto. A partir de la
        transcripción de una nueva reunión, genera una estimación en español
        basada en los ejemplos previos que aparecen a continuación. Usa los
        ejemplos como referencia de formato y nivel de detalle, pero adapta las
        tareas, horas, costes, equipo y duración al alcance de la nueva reunión.
        Incluye un desglose de tareas con horas y costes, un total coherente,
        el equipo recomendado y la duración estimada. Si faltan datos para
        calcular costes, indica la tarifa que asumes. No atribuyas al cliente
        requisitos que no figuren en su transcripción.
    """).strip()
    examples = "\n\n".join(
        f"### Ejemplo previo {index}\n"
        f"Resumen de la reunión:\n{example['meeting_summary']}\n\n"
        f"Estimación generada:\n{example['estimation']}"
        for index, example in enumerate(ESTIMATION_EXAMPLES, start=1)
    )
    return f"{instructions}\n\n## Ejemplos de estimaciones previas\n\n{examples}"


async def generate_estimation(transcription: str) -> str:
    """Devuelve solo el campo de texto del objeto EstimationResult que devuelve la función generate_estimation_details."""
    result = await generate_estimation_details(transcription)
    return result.estimation


async def generate_estimation_details(transcription: str) -> EstimationResult:
    """Envía el contexto CAG y devuelve texto, uso y coste estimado."""
    if not transcription.strip():
        raise ValueError("La transcripción no puede estar vacía.")

    settings = get_settings()
    if settings.llm_provider.strip().lower() != "openai":
        raise ValueError("Este servicio solo admite el proveedor OpenAI.")

    api_key = (
        settings.openai_api_key.get_secret_value()
        if settings.openai_api_key is not None
        else None
    )
    if not api_key:
        raise ValueError("OPENAI_API_KEY debe estar configurada para usar OpenAI.")

    model = settings.llm_model.strip()
    if not model:
        raise ValueError("LLM_MODEL debe estar configurado para usar OpenAI.")
    rates = get_model_rates(model)
    async with AsyncOpenAI(api_key=api_key) as client:
        response = await client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": build_system_prompt()},
                {"role": "user", "content": transcription},
            ],
        )

    if not response.output_text or not response.output_text.strip():
        raise RuntimeError("OpenAI no devolvió una estimación de texto.")

    usage = response.usage
    tokens_used = None
    estimated_cost_usd = None
    if usage is not None:
        cached_tokens = (
            usage.input_tokens_details.cached_tokens
            if usage.input_tokens_details is not None
            else 0
        )
        tokens_used = TokenUsage(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
            cached_input_tokens=cached_tokens,
        )
        cost = (
            Decimal(usage.input_tokens - cached_tokens) * rates.input_rate
            + Decimal(cached_tokens) * rates.cached_input_rate
            + Decimal(usage.output_tokens) * rates.output_rate
        ) / TOKENS_PER_MILLION
        estimated_cost_usd = round(float(cost), 8)

    return EstimationResult(
        estimation=response.output_text.strip(),
        model=model,
        provider="openai",
        tokens_used=tokens_used,
        estimated_cost_usd=estimated_cost_usd,
        timestamp=datetime.now(timezone.utc),
        response_id=response.id,
    )
