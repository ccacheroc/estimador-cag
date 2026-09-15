"""Pruebas del contrato HTTP sin llamadas al proveedor externo."""

import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.llm_service import EstimationResult, TokenUsage


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()

    def test_health_and_estimation_contract(self) -> None:
        self.assertEqual(self.client.get("/health").json(), {"status": "ok"})

        result = EstimationResult(
            estimation="## Estimación: portal de clientes",
            model="gpt-4o-mini",
            provider="openai",
            tokens_used=TokenUsage(100, 30, 130, 10),
            estimated_cost_usd=0.00003225,
            timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            response_id="resp_test",
        )
        with patch(
            "app.routers.estimations.generate_estimation_details",
            new=AsyncMock(return_value=result),
        ) as service:
            response = self.client.post(
                "/api/v1/estimate", json={"transcription": "Reunión de prueba"}
            )

        self.assertEqual(response.status_code, 200)
        service.assert_awaited_once_with("Reunión de prueba")
        body = response.json()
        self.assertEqual(body["estimation"], result.estimation)
        self.assertEqual(body["model"], result.model)
        self.assertEqual(body["provider"], result.provider)
        self.assertEqual(body["tokens_used"]["total_tokens"], 130)
        self.assertEqual(body["estimated_cost_usd"], result.estimated_cost_usd)
        self.assertEqual(body["response_id"], result.response_id)
        self.assertIsNotNone(body["timestamp"])

    def test_empty_transcription_is_rejected(self) -> None:
        response = self.client.post(
            "/api/v1/estimate", json={"transcription": "   "}
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
