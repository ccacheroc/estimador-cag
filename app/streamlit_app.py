"""Interfaz Streamlit de chat para el estimador CAG."""

import asyncio

import streamlit as st
from openai import OpenAIError

from app.services.llm_service import EstimationResult, generate_estimation_details


CHAT_HISTORY_KEY = "chat_history"


def _chat_history() -> list[dict[str, str]]:
    """Devuelve el historial de mensajes de la sesión actual."""
    if CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[CHAT_HISTORY_KEY] = []
    return st.session_state[CHAT_HISTORY_KEY]


def _generate_estimation(transcription: str) -> EstimationResult:
    """Ejecuta la misma lógica asíncrona de estimación usada por la API."""
    return asyncio.run(generate_estimation_details(transcription))


def main() -> None:
    st.set_page_config(page_title="Estimador CAG", page_icon="🧮")
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
        with st.spinner("Generando la estimación…"):
            try:
                result = _generate_estimation(transcription)
                response = result.estimation
                st.markdown(response)
                if result.estimated_cost_usd is not None:
                    st.caption(
                        f"Modelo: {result.model} · "
                        f"Coste estimado: ${result.estimated_cost_usd:.8f}"
                    )
            except ValueError as exc:
                response = f"⚠️ No se pudo generar la estimación: {exc}"
                st.error(response)
            except (OpenAIError, RuntimeError):
                response = "⚠️ No se pudo generar la estimación con el proveedor LLM."
                st.error(response)

    history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
