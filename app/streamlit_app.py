"""Interfaz Streamlit de chat para el estimador CAG."""

import sys
from collections.abc import Callable, Iterator
from pathlib import Path

# Asegura que la raíz del proyecto esté en sys.path al ejecutar con "streamlit run"
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from openai import OpenAIError
from streamlit.delta_generator import DeltaGenerator

from app.context.examples import ESTIMATION_EXAMPLES
from app.services.llm_service import (
    StreamMetrics,
    build_system_prompt,
    generate_estimation_stream,
)


CHAT_HISTORY_KEY = "chat_history"
LAST_METRICS_KEY = "last_metrics"


def _chat_history() -> list[dict[str, str]]:
    """Devuelve el historial de mensajes de la sesión actual."""
    if CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[CHAT_HISTORY_KEY] = []
    return st.session_state[CHAT_HISTORY_KEY]


def _get_last_metrics() -> StreamMetrics | None:
    """Devuelve las métricas de la última estimación en la sesión actual."""
    value = st.session_state.get(LAST_METRICS_KEY)
    return value if isinstance(value, StreamMetrics) else None


def _render_sidebar_metrics(
    placeholder: DeltaGenerator,
    metrics: StreamMetrics | None,
) -> None:
    """Muestra las métricas de la última llamada en la sidebar."""
    with placeholder.container():
        st.markdown("#### Métricas de la última llamada")
        if metrics is None:
            st.info("Aún no se ha realizado ninguna estimación en esta sesión.")
            return

        col1, col2 = st.columns(2)
        col1.metric("Modelo", metrics.model)
        col2.metric("Tiempo", f"{metrics.duration_seconds:.2f} s")
        col1.metric("Tokens entrada", str(metrics.input_tokens))
        col2.metric("Tokens salida", str(metrics.output_tokens))


def _render_sidebar() -> DeltaGenerator:
    """Configura el panel lateral con inspección CAG y devuelve el slot de métricas."""
    st.sidebar.header("Inspección CAG")
    st.sidebar.caption("Detalles del contexto y recursos utilizados por el modelo.")

    metrics_placeholder = st.sidebar.empty()
    _render_sidebar_metrics(metrics_placeholder, _get_last_metrics())

    st.sidebar.divider()

    with st.sidebar.expander("System prompt activo", expanded=False):
        system_prompt = build_system_prompt()
        st.text_area(
            "System prompt activo",
            value=system_prompt,
            height=300,
            disabled=True,
            label_visibility="collapsed",
        )

    with st.sidebar.expander("Contexto CAG inyectado (ejemplos)", expanded=False):
        for index, example in enumerate(ESTIMATION_EXAMPLES, start=1):
            st.markdown(f"**Ejemplo {index}**")
            st.markdown(f"*Resumen de la reunión:*\n\n{example['meeting_summary']}")
            st.markdown("*Estimación de referencia:*")
            st.markdown(example["estimation"])
            if index < len(ESTIMATION_EXAMPLES):
                st.divider()

    return metrics_placeholder


def _generate_estimation_stream(
    transcription: str,
    on_metrics: Callable[[StreamMetrics], None] | None = None,
) -> Iterator[str]:
    """Transmite la estimación token a token en tiempo real reutilizando el servicio."""
    return generate_estimation_stream(transcription, on_metrics=on_metrics)


def main() -> None:
    st.set_page_config(page_title="Estimador CAG", page_icon="🧮")
    metrics_placeholder = _render_sidebar()

    st.title("Estimador de proyectos de software")
    st.caption("Pega una transcripción de reunión para generar una estimación con contexto CAG.")

    history = _chat_history()
    for message in history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    transcription = st.chat_input("Escribe o pega la transcripción de la reunión…")
    if transcription is None:
        return

    transcription = transcription.strip()
    if not transcription:
        st.warning("La transcripción no puede estar vacía.")
        return

    history.append({"role": "user", "content": transcription})
    with st.chat_message("user"):
        st.markdown(transcription)

    with st.chat_message("assistant"):
        try:
            def _on_metrics(metrics: StreamMetrics) -> None:
                st.session_state[LAST_METRICS_KEY] = metrics
                _render_sidebar_metrics(metrics_placeholder, metrics)

            stream = _generate_estimation_stream(
                transcription,
                on_metrics=_on_metrics,
            )
            response = st.write_stream(stream)
            if not isinstance(response, str):
                response = "".join(str(chunk) for chunk in response)
        except ValueError as exc:
            response = f"⚠️ No se pudo generar la estimación: {exc}"
            st.error(response)
        except (OpenAIError, RuntimeError):
            response = "⚠️ No se pudo generar la estimación con el proveedor LLM."
            st.error(response)

    history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
