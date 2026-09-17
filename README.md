# estimador-cag

Estructura inicial del paquete `app`:

```text
app/
├── __init__.py
├── main.py
├── config.py
├── routers/
│   ├── __init__.py
│   └── estimations.py
├── services/
│   ├── __init__.py
│   └── llm_service.py
├── schemas/
│   ├── __init__.py
│   └── estimation.py
└── context/
    ├── __init__.py
    └── examples.py
```

`app/config.py` define `Settings` con Pydantic Settings y carga el archivo `.env` de la raíz. `.env.example` enumera las variables necesarias sin valores y `.env` está excluido de Git. Añade una clave API real para el proveedor que utilices antes de llamar al LLM.

`app/context/examples.py` contiene cuatro estimaciones sintéticas para usar como referencias en el prompt. Cada caso incluye un resumen de reunión, un desglose de horas y costes calculado con una tarifa ilustrativa de 60 €/hora, el equipo recomendado y una duración aproximada.

`app/services/llm_service.py` construye el prompt CAG con los cuatro ejemplos y llama de forma asíncrona a la API Responses de OpenAI con el modelo indicado por `LLM_MODEL` en `.env`. Envía las instrucciones y ejemplos como `system`, la transcripción como `user` y devuelve el texto generado por el asistente. `generate_estimation(transcription)` sigue devolviendo solo texto; `generate_estimation_details(transcription)` añade uso de tokens, coste estimado y metadatos. Requiere `LLM_PROVIDER=openai` y `OPENAI_API_KEY` configurada.

`POST /api/v1/estimate` recibe `{"transcription": "..."}` y devuelve `estimation`, `model`, `provider`, `tokens_used`, `estimated_cost_usd`, `timestamp` y `response_id`. Los tokens proceden de la API Responses; las tarifas de texto de `gpt-4o-mini` están centralizadas en `app/config.py` y deben declararse con `Decimal("...")`, no con números `float`. Si cambias `LLM_MODEL`, registra también las tarifas de ese modelo en `MODEL_RATES`: el servicio rechazará la petición antes de llamar a OpenAI mientras falten. El coste es orientativo, no una factura, y será `null` si la API no devuelve datos de uso.

`app/main.py` registra el router con el prefijo `/api/v1`, ofrece `GET /health` con `{"status": "ok"}` y configura el título y la descripción visibles en Swagger UI (`/docs`). El health check confirma que la API responde; no consulta al proveedor LLM.

## Cómo arrancar el proyecto

### 1. Requisitos previos

- Python `>=3.13`
- [uv](https://docs.astral.sh/uv/) instalado en el sistema.

### 2. Instalación de dependencias

Sincroniza el entorno virtual y las dependencias del proyecto:

```bash
uv sync
```

### 3. Configuración de variables de entorno

Copia la plantilla de configuración `.env.example` para generar tu archivo `.env`:

```bash
cp .env.example .env
```

Define los valores en `.env`:
- `OPENAI_API_KEY`: Clave de API de OpenAI (necesaria para generar estimaciones reales con el LLM).
- `LLM_PROVIDER`: Proveedor de LLM (por ejemplo, `openai`).
- `LLM_MODEL`: Modelo a utilizar (por defecto `gpt-4o-mini`).
- `APP_ENV`: Entorno de ejecución (`development`, `local`, etc.).
- `LOG_LEVEL`: Nivel de logging (`INFO`, `DEBUG`, etc.).

### 4. Arrancar el servidor de desarrollo

Inicia la API con recarga automática en caliente:

```bash
uv run uvicorn app.main:app --reload
```

El servidor estará escuchando por defecto en `http://127.0.0.1:8000`.

### 5. Verificación y uso

- **Comprobación de salud (Health check):**
  ```bash
  curl http://127.0.0.1:8000/health
  ```
- **Documentación interactiva (Swagger UI):**
  Disponible en el navegador en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- **Petición de estimación de ejemplo:**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/v1/estimate \
    -H 'Content-Type: application/json' \
    -d '{"transcription":"El cliente necesita un portal para consultar pedidos y descargar facturas."}'
  ```

## Documentación y pruebas

La arquitectura prevista y el estado actual se describen en [docs/architecture.md](docs/architecture.md). Las tecnologías están en [docs/technology.md](docs/technology.md), y la elección de FastAPI en [ADR-001](docs/decisions/ADR-001-fastapi.md).

La validación automática está en [`.github/workflows/ci.yml`](.github/workflows/ci.yml). En cada push a `main` y en cada pull request, GitHub Actions instala las dependencias fijadas en `uv.lock` y ejecuta las pruebas de `tests/`. Estas comprueban que existen los archivos obligatorios, que `/health` y `POST /api/v1/estimate` cumplen el contrato, y que el servicio envía el contexto CAG y la transcripción a la API Responses. La llamada a OpenAI se simula, así que el pipeline no necesita `OPENAI_API_KEY` ni incurre en costes. Para ejecutar las mismas pruebas en tu terminal:

```bash
uv sync --locked
uv run --no-sync python -m unittest discover -s tests -v
```

Una ejecución correcta de CI verifica el código y el contrato local; no confirma que las credenciales o el proveedor externo estén disponibles en producción.
