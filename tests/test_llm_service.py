"""Comprueba la integración CAG con la API Responses sin conexión de red."""

import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from pydantic import SecretStr

from app.context.examples import ESTIMATION_EXAMPLES
from app.services.llm_service import (
    StreamMetrics,
    generate_estimation_details,
    generate_estimation_stream,
)


class FakeOpenAIClient:
    def __init__(self, *, api_key: str) -> None:
        self.api_key = api_key
        self.responses = SimpleNamespace(create=AsyncMock())

    async def __aenter__(self) -> "FakeOpenAIClient":
        return self

    async def __aexit__(self, *_args: object) -> None:
        return None


class FakeSyncOpenAIClient:
    def __init__(self, *, api_key: str) -> None:
        self.api_key = api_key
        self.responses = SimpleNamespace(create=MagicMock())

    def __enter__(self) -> "FakeSyncOpenAIClient":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


class LlmServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_context_transcription_and_usage(self) -> None:
        settings = SimpleNamespace(
            llm_provider="openai",
            llm_model="gpt-4o-mini",
            openai_api_key=SecretStr("test-key"),
        )
        client = FakeOpenAIClient(api_key="test-key")
        client.responses.create.return_value = SimpleNamespace(
            output_text="  ## Estimación de prueba  ",
            id="resp_test",
            usage=SimpleNamespace(
                input_tokens=1000,
                output_tokens=200,
                total_tokens=1200,
                input_tokens_details=SimpleNamespace(cached_tokens=100),
            ),
        )
        transcription = "El cliente solicita una aplicación de reservas."

        with (
            patch("app.services.llm_service.get_settings", return_value=settings),
            patch("app.services.llm_service.AsyncOpenAI", return_value=client) as sdk,
        ):
            result = await generate_estimation_details(transcription)

        sdk.assert_called_once_with(api_key="test-key")
        client.responses.create.assert_awaited_once()
        kwargs = client.responses.create.await_args.kwargs
        self.assertEqual(kwargs["model"], "gpt-4o-mini")
        self.assertEqual([item["role"] for item in kwargs["input"]], ["system", "user"])
        self.assertEqual(kwargs["input"][1]["content"], transcription)
        system_prompt = kwargs["input"][0]["content"]
        for example in ESTIMATION_EXAMPLES:
            with self.subTest(example=example["meeting_summary"][:30]):
                self.assertIn(example["meeting_summary"], system_prompt)
                self.assertIn(example["estimation"], system_prompt)
        self.assertEqual(result.estimation, "## Estimación de prueba")
        tokens_used = result.tokens_used
        self.assertIsNotNone(tokens_used)
        assert tokens_used is not None
        self.assertEqual(tokens_used.total_tokens, 1200)
        self.assertEqual(tokens_used.cached_input_tokens, 100)
        self.assertEqual(result.estimated_cost_usd, 0.0002625)
        self.assertEqual(result.response_id, "resp_test")

    def test_generate_estimation_stream_yields_deltas(self) -> None:
        settings = SimpleNamespace(
            llm_provider="openai",
            llm_model="gpt-4o-mini",
            openai_api_key=SecretStr("test-key"),
        )
        fake_events = [
            SimpleNamespace(type="response.created"),
            SimpleNamespace(type="response.output_text.delta", delta="Estimación "),
            SimpleNamespace(type="response.output_text.delta", delta="en "),
            SimpleNamespace(type="response.output_text.delta", delta="tiempo real."),
            SimpleNamespace(type="response.completed"),
        ]
        client = FakeSyncOpenAIClient(api_key="test-key")
        client.responses.create.return_value = fake_events

        with (
            patch("app.services.llm_service.get_settings", return_value=settings),
            patch("app.services.llm_service.OpenAI", return_value=client) as sdk,
        ):
            chunks = list(generate_estimation_stream("Transcripción de reunión"))

        sdk.assert_called_once_with(api_key="test-key")
        client.responses.create.assert_called_once()
        kwargs = client.responses.create.call_args.kwargs
        self.assertTrue(kwargs.get("stream"))
        self.assertEqual(kwargs["model"], "gpt-4o-mini")
        self.assertEqual(chunks, ["Estimación ", "en ", "tiempo real."])

    def test_generate_estimation_stream_reports_metrics_when_callback_provided(self) -> None:
        settings = SimpleNamespace(
            llm_provider="openai",
            llm_model="gpt-4o-mini",
            openai_api_key=SecretStr("test-key"),
        )
        fake_events = [
            SimpleNamespace(type="response.created"),
            SimpleNamespace(type="response.output_text.delta", delta="Texto generado"),
            SimpleNamespace(
                type="response.completed",
                response=SimpleNamespace(
                    usage=SimpleNamespace(input_tokens=120, output_tokens=35),
                ),
            ),
        ]
        client = FakeSyncOpenAIClient(api_key="test-key")
        client.responses.create.return_value = fake_events

        captured_metrics: list[StreamMetrics] = []

        with (
            patch("app.services.llm_service.get_settings", return_value=settings),
            patch("app.services.llm_service.OpenAI", return_value=client),
        ):
            chunks = list(
                generate_estimation_stream(
                    "Transcripción con métricas",
                    on_metrics=captured_metrics.append,
                )
            )

        self.assertEqual(chunks, ["Texto generado"])
        self.assertEqual(len(captured_metrics), 1)
        metric = captured_metrics[0]
        self.assertEqual(metric.model, "gpt-4o-mini")
        self.assertEqual(metric.input_tokens, 120)
        self.assertEqual(metric.output_tokens, 35)
        self.assertGreaterEqual(metric.duration_seconds, 0.0)

    def test_generate_estimation_stream_reports_default_tokens_if_no_usage(self) -> None:
        settings = SimpleNamespace(
            llm_provider="openai",
            llm_model="gpt-4o-mini",
            openai_api_key=SecretStr("test-key"),
        )
        fake_events = [
            SimpleNamespace(type="response.output_text.delta", delta="Texto"),
            SimpleNamespace(type="response.completed", response=None),
        ]
        client = FakeSyncOpenAIClient(api_key="test-key")
        client.responses.create.return_value = fake_events

        captured_metrics: list[StreamMetrics] = []

        with (
            patch("app.services.llm_service.get_settings", return_value=settings),
            patch("app.services.llm_service.OpenAI", return_value=client),
        ):
            list(
                generate_estimation_stream(
                    "Transcripción sin usage",
                    on_metrics=captured_metrics.append,
                )
            )

        self.assertEqual(len(captured_metrics), 1)
        metric = captured_metrics[0]
        self.assertEqual(metric.input_tokens, 0)
        self.assertEqual(metric.output_tokens, 0)
        self.assertEqual(metric.model, "gpt-4o-mini")
        self.assertGreaterEqual(metric.duration_seconds, 0.0)


if __name__ == "__main__":
    unittest.main()
