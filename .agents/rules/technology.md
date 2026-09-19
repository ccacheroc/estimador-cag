# Tecnología del estimador CAG

Este documento registra las tecnologías elegidas o previstas para la fase CAG. Las versiones declaradas son mínimos de `pyproject.toml`; las versiones resueltas están en `uv.lock`. Para el estado funcional y las responsabilidades de producto, véase el [PRD](../../docs/PRD.md).

## Stack declarado

| Tecnología | Declaración actual | Uso |
| --- | --- | --- |
| Python | `>=3.13` | Lenguaje de la aplicación |
| FastAPI | `fastapi[standard]>=0.141.1` | API HTTP y composición ASGI |
| SDK de OpenAI | `openai>=3.14.0` | Cliente asíncrono de la API Responses para generar estimaciones |
| Pydantic Settings | `pydantic-settings>=2.15.0` | Carga y validación de configuración |
| uv | `uv.lock` presente | Resolución, instalación y ejecución del entorno Python |


## FastAPI y llamadas LLM

La decisión de adoptar FastAPI, con sus alternativas y consecuencias, está en [ADR-001](../../docs/decisions/ADR-001-fastapi.md).

FastAPI implementa ASGI y permite rutas `async`. Esto encaja con peticiones que esperan una API externa: mientras una operación asíncrona de red está en `await`, el servidor puede atender otras tareas. FastAPI es la elección de este proyecto por su integración de rutas y modelos Pydantic; otras soluciones ASGI también pueden ofrecer concurrencia para operaciones de red. La ventaja depende de usar un cliente LLM asíncrono; el ejemplo del texto de referencia que llama al cliente síncrono `OpenAI` dentro de `async def` no debe copiarse como implementación final. Si una biblioteca solo ofrece llamadas bloqueantes, se debe usar una ruta síncrona o trasladar esa llamada a un hilo, según la [guía oficial de FastAPI](https://fastapi.tiangolo.com/async/). No se presupone un número de peticiones concurrentes ni una latencia fija del LLM.

La división en routers y servicios sigue el mecanismo de [`APIRouter` e `include_router`](https://fastapi.tiangolo.com/tutorial/bigger-applications/). `POST /api/v1/estimate` está registrado en `app/main.py`; sus modelos Pydantic validan el body y documentan la respuesta mediante [`response_model`](https://fastapi.tiangolo.com/tutorial/response-model/).

## Configuración y secretos

[`app/config.py`](../app/config.py) define `Settings(BaseSettings)` y usa `SettingsConfigDict` para leer el `.env` de la raíz con codificación UTF-8. La ruta se calcula desde el archivo Python, de modo que no depende del directorio desde el que se lance el proceso. `env_ignore_empty=True` evita tratar una entrada vacía como un valor configurado. Las claves API usan `SecretStr`; `llm_provider`, `llm_model`, `app_env` y `log_level` son cadenas obligatorias.

El archivo [`.env.example`](../.env.example) enumera actualmente `OPENAI_API_KEY`, `LLM_PROVIDER`, `LLM_MODEL`, `APP_ENV` y `LOG_LEVEL` sin valores. `.env` contiene la configuración local y está excluido de Git por [`.gitignore`](../.gitignore). Las variables del proceso tienen prioridad sobre el archivo `.env`, según la [documentación de Pydantic Settings](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/).

Las claves API son opcionales en la clase actual. Por tanto, la ausencia de una clave no provoca por sí sola un fallo al crear `Settings`; el servicio valida `OPENAI_API_KEY` antes de llamar a OpenAI. La configuración incluye la función cacheada `get_settings()`.

## Proveedor y modelo

El proyecto declara el SDK de OpenAI. El servicio admite `LLM_PROVIDER=openai` y usa el valor de `LLM_MODEL` cargado por `Settings` para llamar a Responses y devolver el modelo en el JSON. La configuración local actual usa `gpt-4o-mini`. La [guía oficial de OpenAI](https://developers.openai.com/api/docs/quickstart) documenta el uso del SDK y de las claves API.

`llm_service.py` concentra la construcción del prompt con los cuatro ejemplos sintéticos, la llamada asíncrona a `client.responses.create` y la comprobación de `response.output_text`. La lista `input` contiene un mensaje `system` con instrucciones y ejemplos, seguido de un mensaje `user` con la transcripción; el asistente genera la salida. El SDK aplica sus valores predeterminados de timeout y reintentos; aún falta decidir una política específica para ellos.

El servicio lee `usage.input_tokens`, `usage.output_tokens`, `usage.total_tokens` y los tokens de entrada cacheados. `app/config.py` centraliza las [tarifas estándar de texto de `gpt-4o-mini`](https://developers.openai.com/api/docs/models/gpt-4o-mini): 0,15 USD por millón de tokens de entrada, 0,075 USD por millón de tokens de entrada cacheados y 0,60 USD por millón de tokens de salida. Al cambiar `LLM_MODEL` hay que registrar también sus tarifas en `MODEL_RATES`; si faltan, `get_model_rates()` impide llamar a OpenAI y el router devuelve HTTP 503. Solo la ausencia de `usage` hace que `tokens_used` y `estimated_cost_usd` sean `null`. El coste es orientativo y no incluye otros cargos. Los errores de OpenAI o respuestas sin texto se traducen a HTTP 502.

## Gestión del proyecto y comprobaciones

`pyproject.toml` declara las dependencias y `uv.lock` fija la resolución. Los comandos del flujo previsto son:

```bash
uv sync
uv add nombre-del-paquete
uv run uvicorn app.main:app --reload
```

El último comando inicia la aplicación FastAPI registrada en `app/main.py`. La [documentación de uv](https://docs.astral.sh/uv/concepts/projects/sync/) describe el bloqueo, la sincronización y la ejecución con el entorno del proyecto.

La suite [`tests/`](../../tests/) utiliza `unittest` de la biblioteca estándar y `TestClient` de FastAPI. Prueba la estructura mínima, el contrato HTTP, la interfaz Streamlit y la llamada al SDK Responses con un cliente simulado, sin clave API ni tráfico externo. [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) ejecuta `uv sync --locked` y `uv run --no-sync python -m unittest discover -s tests -v` en cada push a `main` y pull request. Esto comprueba el comportamiento local; una prueba de disponibilidad del proveedor real requiere una validación separada con credenciales.
