# Trabajo pendiente

Este documento recoge trabajo identificado pero todavía no implementado. No
describe capacidades disponibles en el estado actual del proyecto.

## Pruebas E2E con Playwright

- [ ] Crear pruebas E2E reales para Streamlit bajo `tests/e2e/`, comenzando por
  un *smoke test* en Chromium.
- [ ] Cubrir los flujos críticos del chat: carga de la aplicación, envío de una
  transcripción, respuesta generada, actualización de métricas y tratamiento de
  errores.
- [ ] Implementar fixtures que arranquen y detengan Streamlit en un puerto
  aislado o configurable durante las pruebas.
- [ ] Proporcionar al proceso Streamlit un proveedor o configuración falsa del
  LLM para evitar red real, credenciales y consumo de tokens. Un `monkeypatch`
  limitado al proceso de pytest no es suficiente si la aplicación se ejecuta
  en otro proceso.
- [ ] Añadir a GitHub Actions la ejecución explícita de
  `uv run --no-sync pytest tests/e2e` cuando exista al menos una prueba.
- [ ] Conservar trazas y capturas de Playwright cuando fallen las pruebas y
  publicarlas como artefactos de CI.
- [ ] Actualizar el README para presentar la suite E2E como operativa una vez
  que los comandos documentados ejecuten pruebas reales.

## Dockerización

- [ ] Decidir si FastAPI y Streamlit se distribuyen en una imagen común o como
  servicios separados.
- [ ] Crear los `Dockerfile`, `.dockerignore` y, si procede, `compose.yaml`.
- [ ] Ejecutar los contenedores con un usuario sin privilegios y suministrar
  secretos exclusivamente mediante variables de entorno o el mecanismo de
  secretos de la plataforma.
- [ ] Añadir *health checks* y documentar puertos, variables y comandos de
  construcción y ejecución.
- [ ] Incorporar una validación automatizada que construya las imágenes y
  compruebe el arranque de los servicios.
