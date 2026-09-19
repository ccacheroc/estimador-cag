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

Los errores HTTP con cuerpo siguen RFC 9457 y usan
`application/problem+json`. El OpenAPI generado documenta los contratos `422`,
`500`, `502` y `503` de la estimación, incluidos sus tipos de problema estables.

`app/main.py` registra el router con el prefijo `/api/v1`, ofrece `GET /health` con `{"status": "ok"}` y configura el título y la descripción visibles en Swagger UI (`/docs`). El health check confirma que la API responde; no consulta al proveedor LLM.

## Guía de desarrollo (Development Guide)

Esta guía detalla el paso a paso para configurar el entorno local, arrancar los servicios y ejecutar la suite de pruebas unitarias, de integración y End-to-End con Playwright.

### 1. Requisitos previos

- **Python** `>=3.13`
- [uv](https://docs.astral.sh/uv/) (gestor exclusivo de dependencias y entornos del proyecto)
- **Git**

### 2. Clonación y configuración del entorno

Clona el repositorio si aún no lo has hecho y sitúate en la raíz del proyecto:

```bash
git clone <url-del-repositorio>
cd estimador-cag
```

Copia la plantilla de configuración `.env.example` para generar tu archivo `.env`:

```bash
cp .env.example .env
```

Configura las variables necesarias en `.env`:
- `OPENAI_API_KEY`: Clave de API de OpenAI (necesaria para interactuar con el LLM en local).
- `LLM_PROVIDER`: Proveedor de LLM (por defecto `openai`).
- `LLM_MODEL`: Modelo a utilizar (por defecto `gpt-4o-mini`).
- `APP_ENV`: Entorno (`development`, `local`, etc.).
- `LOG_LEVEL`: Nivel de detalle del logging (`INFO`, `DEBUG`, etc.).

### 3. Instalación de dependencias

Sincroniza el entorno virtual y las dependencias (incluidas las de desarrollo):

```bash
uv sync
```

### 4. Instalación de navegadores para Playwright

Para habilitar las pruebas End-to-End (E2E), instala los binarios de los navegadores gestionados por Playwright:

```bash
uv run playwright install
```

*(Opcional)* Si estás en Linux y necesitas instalar dependencias del sistema operativo para los navegadores:

```bash
uv run playwright install --with-deps
```

### 5. Arranque de los servicios en desarrollo

#### Backend (API FastAPI)
Inicia la API con recarga automática en caliente:

```bash
uv run uvicorn app.main:app --reload
```
- **Endpoint base:** `http://127.0.0.1:8000`
- **Health Check:** `http://127.0.0.1:8000/health`
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### Frontend (Chat Streamlit)
Inicia la interfaz web interactiva en una nueva terminal:

```bash
uv run streamlit run app/streamlit_app.py
```
- **Interfaz web:** `http://127.0.0.1:8501`

### 6. Suite de Pruebas (Testing)

#### Pruebas unitarias y de integración
Ejecuta todas las pruebas unitarias y de integración con `pytest`:

```bash
uv run pytest tests/test_*.py -v
```

#### Pruebas End-to-End (E2E) con Playwright
Las pruebas de navegador verifican la interfaz Streamlit y los flujos integrados:

- **Ejecución en modo headless (por defecto, para terminal y CI):**
  ```bash
  uv run pytest tests/e2e -v
  ```
- **Ejecución con navegador visible (modo headed / interactivo):**
  ```bash
  uv run pytest tests/e2e --headed
  ```
- **Ejecución con captura de trazas (Trace Viewer para depurar):**
  ```bash
  uv run pytest tests/e2e --tracing=on
  ```
- **Generador interactivo de código de Playwright:**
  ```bash
  uv run playwright codegen http://127.0.0.1:8501
  ```

#### Comprobación de tipos estáticos (Pyright)
Verifica el tipado estricto en `app/` y `tests/`:

```bash
uv run --no-sync pyright
```

## Documentación y decisiones de arquitectura

- Estado actual de la arquitectura: [docs/architecture-state.md](docs/architecture-state.md)
- Elección de framework HTTP: [docs/decisions/ADR-001-fastapi.md](docs/decisions/ADR-001-fastapi.md)
- Elección de framework E2E Playwright: [docs/decisions/ADR-002-playwright-e2e.md](docs/decisions/ADR-002-playwright-e2e.md)

La validación automática continua se define en [.github/workflows/ci.yml](.github/workflows/ci.yml). En cada push a `main` y en cada pull request, GitHub Actions instala las dependencias fijadas en `uv.lock`, comprueba `app/` y `tests/` con Pyright en modo estricto y ejecuta la suite de pruebas automatizadas con dobles de prueba para OpenAI.
