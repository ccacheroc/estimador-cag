"""Verify the HTTP contract without calling the external provider."""

import unittest
from datetime import datetime, timezone
from typing import Protocol, cast
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.llm_service import EstimationResult, TokenUsage


class HttpHeaders(Protocol):
    def __getitem__(self, key: str) -> str: ...


class HttpResponse(Protocol):
    @property
    def status_code(self) -> int: ...

    @property
    def headers(self) -> HttpHeaders: ...

    @property
    def text(self) -> str: ...

    def json(self) -> object: ...


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()

    def assert_problem_response(
        self,
        response: HttpResponse,
        *,
        status: int,
        problem_type: str,
        title: str,
    ) -> dict[str, object]:
        self.assertEqual(response.status_code, status)
        self.assertEqual(
            response.headers["content-type"], "application/problem+json"
        )
        body = cast(dict[str, object], response.json())
        self.assertEqual(body["type"], problem_type)
        self.assertEqual(body["title"], title)
        self.assertEqual(body["status"], status)
        self.assertIsInstance(body["detail"], str)
        self.assertTrue(body["detail"])
        return body

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
        body = self.assert_problem_response(
            response,
            status=422,
            problem_type="urn:estimador-cag:problem:validation-error",
            title="Petición no válida",
        )
        self.assertIn("errors", body)
        self.assertNotIn("   ", response.text)

    def test_configuration_error_uses_problem_details(self) -> None:
        with patch(
            "app.routers.estimations.generate_estimation_details",
            new=AsyncMock(side_effect=ValueError("Configuración no disponible.")),
        ):
            response = self.client.post(
                "/api/v1/estimate", json={"transcription": "Reunión de prueba"}
            )

        body = self.assert_problem_response(
            response,
            status=503,
            problem_type="urn:estimador-cag:problem:configuration-error",
            title="Servicio no disponible",
        )
        self.assertEqual(body["detail"], "Configuración no disponible.")

    def test_provider_error_uses_problem_details(self) -> None:
        with patch(
            "app.routers.estimations.generate_estimation_details",
            new=AsyncMock(side_effect=RuntimeError("raw provider failure")),
        ):
            response = self.client.post(
                "/api/v1/estimate", json={"transcription": "Reunión de prueba"}
            )

        body = self.assert_problem_response(
            response,
            status=502,
            problem_type="urn:estimador-cag:problem:provider-error",
            title="Error del proveedor",
        )
        self.assertEqual(body["detail"], "No se pudo generar la estimación.")
        self.assertNotIn("raw provider failure", response.text)

    def test_unknown_route_uses_problem_details(self) -> None:
        response = self.client.get("/missing")

        self.assert_problem_response(
            response,
            status=404,
            problem_type="urn:estimador-cag:problem:http-404",
            title="Recurso no encontrado",
        )

    def test_unexpected_error_uses_problem_details(self) -> None:
        with (
            patch(
                "app.routers.estimations.generate_estimation_details",
                new=AsyncMock(side_effect=Exception("raw internal failure")),
            ),
            patch("app.http_errors.logger.error"),
            TestClient(app, raise_server_exceptions=False) as client,
        ):
            response = client.post(
                "/api/v1/estimate", json={"transcription": "Reunión de prueba"}
            )

        body = self.assert_problem_response(
            response,
            status=500,
            problem_type="urn:estimador-cag:problem:internal-error",
            title="Error interno del servidor",
        )
        self.assertEqual(body["detail"], "La petición no pudo completarse.")
        self.assertNotIn("raw internal failure", response.text)

    def test_openapi_documents_all_estimation_errors(self) -> None:
        responses = app.openapi()["paths"]["/api/v1/estimate"]["post"]["responses"]

        for status in ("422", "500", "502", "503"):
            with self.subTest(status=status):
                self.assertIn(status, responses)
                content = responses[status]["content"]
                self.assertEqual(list(content), ["application/problem+json"])
                self.assertIn("schema", content["application/problem+json"])


if __name__ == "__main__":
    unittest.main()
