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

`POST /api/v1/estimate` recibe `{"transcription": "..."}` y devuelve `estimation`, `model`, `provider`, `tokens_used`, `estimated_cost_usd`, `timestamp` y `response_id`. Los tokens proceden de la API Responses; las tarifas de texto de `gpt-4o-mini` están centralizadas en `app/config.py` y deben declararse con `Decimal("...")`, no con números `float`. Si cambias `LLM_MODEL`, registra también las tarifas de ese modelo en `MODEL_RATES`: el servicio rechazará la petición antes de llamar a OpenAI mientras falten. El coste es orientativo, no una factura, y será `null` si la API no devuelve datos de uso. Para iniciar la API: `uv run uvicorn app.main:app --reload`.

`app/main.py` registra el router con el prefijo `/api/v1`, ofrece `GET /health` con `{"status": "ok"}` y configura el título y la descripción visibles en Swagger UI (`/docs`). El health check confirma que la API responde; no consulta al proveedor LLM.

Con la API en ejecución, una petición de ejemplo es:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/estimate \
  -H 'Content-Type: application/json' \
  -d '{"transcription":"El cliente necesita un portal para consultar pedidos y descargar facturas."}'
```

La arquitectura prevista y el estado actual se describen en [docs/architecture.md](docs/architecture.md). Las tecnologías están en [docs/technology.md](docs/technology.md), y la elección de FastAPI en [ADR-001](docs/decisions/ADR-001-fastapi.md).
