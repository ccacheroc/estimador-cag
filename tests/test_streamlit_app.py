"""Pruebas de la interfaz Streamlit sin ejecutar una sesión web real."""

import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from app.services.llm_service import StreamMetrics
# This focused test intentionally exercises the UI adapter's private sync bridge.
from app.streamlit_app import (
    LAST_METRICS_KEY,
    _chat_history,  # pyright: ignore[reportPrivateUsage]
    _generate_estimation_stream,  # pyright: ignore[reportPrivateUsage]
    _get_last_metrics,  # pyright: ignore[reportPrivateUsage]
)


class StreamlitAppTests(unittest.TestCase):
    def test_generate_estimation_stream_reuses_service(self) -> None:
        fake_chunks = iter(["Estimación ", "en ", "streaming"])
        with patch(
            "app.streamlit_app.generate_estimation_stream",
            return_value=fake_chunks,
        ) as service:
            stream = _generate_estimation_stream("Transcripción de prueba")

        self.assertIs(stream, fake_chunks)
        service.assert_called_once_with("Transcripción de prueba", on_metrics=None)

    def test_generate_estimation_stream_passes_on_metrics(self) -> None:
        fake_chunks = iter(["chunk"])
        captured: list[StreamMetrics] = []
        with patch(
            "app.streamlit_app.generate_estimation_stream",
            return_value=fake_chunks,
        ) as service:
            stream = _generate_estimation_stream("Transcripción", on_metrics=captured.append)

        self.assertIs(stream, fake_chunks)
        service.assert_called_once_with("Transcripción", on_metrics=captured.append)

    def test_chat_contract_is_present_and_api_key_is_not_hardcoded(self) -> None:
        source = Path("app/streamlit_app.py").read_text(encoding="utf-8")

        self.assertIn("st.chat_message", source)
        self.assertIn("st.chat_input", source)
        self.assertIn("st.session_state", source)
        self.assertIn("st.write_stream", source)
        self.assertIn("st.sidebar", source)
        self.assertIn("build_system_prompt", source)
        self.assertIn("ESTIMATION_EXAMPLES", source)
        self.assertNotIn("sk-", source)

    def test_sidebar_initial_state_shows_empty_metrics_and_expanders(self) -> None:
        app = AppTest.from_file("../app/streamlit_app.py").run()
        self.assertEqual(len(app.exception), 0)

        # Check that sidebar has the information message when no metrics yet
        info_messages = [msg.value for msg in app.sidebar.info]
        self.assertTrue(
            any("Aún no se ha realizado ninguna estimación" in msg for msg in info_messages),
            f"Expected empty metrics info message, found: {info_messages}",
        )

        # Check that expanders for system prompt and CAG examples are present
        expander_labels = [exp.label for exp in app.sidebar.expander]
        self.assertTrue(any("System prompt" in label for label in expander_labels))
        self.assertTrue(any("Contexto CAG" in label for label in expander_labels))

    def test_sidebar_renders_metrics_when_present_in_session_state(self) -> None:
        app = AppTest.from_file("../app/streamlit_app.py")
        app.session_state[LAST_METRICS_KEY] = StreamMetrics(
            model="gpt-4o-mini",
            input_tokens=1250,
            output_tokens=340,
            duration_seconds=2.15,
        )
        app.run()
        self.assertEqual(len(app.exception), 0)

        # Check metrics in sidebar
        metric_values = {metric.label: metric.value for metric in app.sidebar.metric}
        self.assertEqual(metric_values.get("Modelo"), "gpt-4o-mini")
        self.assertEqual(metric_values.get("Tiempo"), "2.15 s")
        self.assertEqual(metric_values.get("Tokens entrada"), "1250")
        self.assertEqual(metric_values.get("Tokens salida"), "340")

    def test_get_last_metrics_returns_typed_or_none(self) -> None:
        state: dict[str, object] = {}
        with patch("app.streamlit_app.st.session_state", state):
            self.assertIsNone(_get_last_metrics())

        state[LAST_METRICS_KEY] = "invalid"
        with patch("app.streamlit_app.st.session_state", state):
            self.assertIsNone(_get_last_metrics())

        valid_metrics = StreamMetrics(
            model="gpt-4o-mini",
            input_tokens=10,
            output_tokens=5,
            duration_seconds=0.5,
        )
        state[LAST_METRICS_KEY] = valid_metrics
        with patch("app.streamlit_app.st.session_state", state):
            self.assertEqual(_get_last_metrics(), valid_metrics)

    def test_chat_history_initializes_empty_list_and_persists(self) -> None:
        state: dict[str, object] = {}
        with patch("app.streamlit_app.st.session_state", state):
            history = _chat_history()
            self.assertEqual(history, [])
            history.append({"role": "user", "content": "hola"})
            self.assertEqual(_chat_history(), [{"role": "user", "content": "hola"}])


if __name__ == "__main__":
    unittest.main()
