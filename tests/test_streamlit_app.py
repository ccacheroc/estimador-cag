"""Pruebas de la interfaz Streamlit sin ejecutar una sesión web real."""

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

# This focused test intentionally exercises the UI adapter's private sync bridge.
from app.streamlit_app import _generate_estimation  # pyright: ignore[reportPrivateUsage]


class StreamlitAppTests(unittest.TestCase):
    def test_generate_estimation_reuses_service(self) -> None:
        result = SimpleNamespace(estimation="## Estimación de prueba")
        with patch(
            "app.streamlit_app.generate_estimation_details",
            new=AsyncMock(return_value=result),
        ) as service:
            generated = _generate_estimation("Transcripción de prueba")

        self.assertIs(generated, result)
        service.assert_awaited_once_with("Transcripción de prueba")

    def test_chat_contract_is_present_and_api_key_is_not_hardcoded(self) -> None:
        source = Path("app/streamlit_app.py").read_text(encoding="utf-8")

        self.assertIn("st.chat_message", source)
        self.assertIn("st.chat_input", source)
        self.assertIn("st.session_state", source)
        self.assertNotIn("sk-", source)


if __name__ == "__main__":
    unittest.main()
