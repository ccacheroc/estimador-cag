"""Configuration loaded from the project's root .env file."""

from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass(frozen=True)
class ModelRates:
    input_rate: Decimal
    cached_input_rate: Decimal
    output_rate: Decimal

    def __post_init__(self) -> None:
        for name in ("input_rate", "cached_input_rate", "output_rate"):
            rate = getattr(self, name)
            if not isinstance(rate, Decimal) or not rate.is_finite() or rate < 0:
                raise ValueError(f"{name} debe ser un Decimal finito no negativo.")


# Tarifas estándar de texto en USD por millón de tokens:
# https://developers.openai.com/api/docs/models/gpt-4o-mini

TOKENS_PER_MILLION = Decimal(1_000_000)
MODEL_RATES = {
    "gpt-4o-mini": ModelRates(
        Decimal("0.15"), Decimal("0.075"), Decimal("0.60")
    ),
}


def get_model_rates(model: str) -> ModelRates:
    """Exige tarifas explícitas antes de utilizar un modelo."""
    try:
        return MODEL_RATES[model]
    except KeyError as exc:
        raise ValueError(
            f"No hay tarifas configuradas para {model!r}; "
            "actualiza MODEL_RATES en app/config.py antes de usar este modelo."
        ) from exc


class Settings(BaseSettings):
    openai_api_key: SecretStr | None = None
    llm_provider: str = Field(min_length=1)
    llm_model: str = Field(min_length=1)
    app_env: str = Field(min_length=1)
    log_level: str = Field(min_length=1)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )


@lru_cache
def get_settings() -> Settings:
    # BaseSettings supplies required values from the environment at runtime.
    return Settings()  # pyright: ignore[reportCallIssue]
