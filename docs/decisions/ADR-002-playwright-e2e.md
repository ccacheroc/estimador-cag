# ADR-002: Playwright para pruebas End-to-End (E2E)

**Estado:** Aceptada

## Contexto

El estimador CAG dispone de una interfaz web interactiva basada en Streamlit (`app/streamlit_app.py`) y una API HTTP basada en FastAPI (`app/main.py`). La interfaz de Streamlit re-ejecuta su script en cada interacción del usuario, mantiene estado en memoria de sesión (`st.session_state`) y renderiza componentes dinámicos en el navegador que se comunican vía WebSockets con el servidor de la aplicación.

Las pruebas unitarias y de integración existentes en `tests/` ejercitan el servicio de estimación y el adaptador HTTP sin levantar un navegador real. Aunque Streamlit ofrece utilidades de prueba en memoria (`AppTest`), estas no validan el renderizado real en el DOM, la reactividad visual, el comportamiento de carga en navegadores web ni la integración completa de extremo a extremo.

Se requiere un framework de automatización de navegador para ejecutar pruebas E2E deterministas sobre la interfaz de usuario y sus flujos principales.

## Decisión

Adoptar **Playwright** (a través de la integración oficial `pytest-playwright` en Python) como el framework estándar para pruebas End-to-End (E2E) en el repositorio.

Los tests E2E residirán en `tests/e2e/`, se ejecutarán mediante `uv run pytest tests/e2e` y por defecto funcionarán en modo *headless*. Conforme a las reglas de determinismo y aislamiento del proyecto, los tests E2E interceptarán o simularán la frontera del LLM (mediante dobles de prueba o configuración local) para evitar consumo de tokens de OpenAI y latencias no deterministas durante las pruebas automatizadas.

El alcance inicial de compatibilidad y ejecución automatizada se limita a
**Chromium**. Firefox y WebKit quedan fuera del soporte actual hasta que exista
un requisito explícito que justifique ampliar la matriz de navegadores.

## Justificación frente a alternativas

### 1. Frente a Cypress

| Criterio | Playwright (`pytest-playwright`) | Cypress |
| --- | --- | --- |
| **Alineación con el stack del proyecto** | **Ventaja:** Integración nativa en Python con `pytest`. No introduce dependencias de Node.js, `package.json`, `npm` ni herramientas ajenas al ecosistema `uv` del proyecto. | **Inconveniente:** Requiere introducir Node.js y npm en un proyecto exclusivamente Python, creando una configuración dual y duplicando herramientas de CI/CD. |
| **Arquitectura de ejecución** | **Ventaja:** Control del navegador fuera del proceso mediante el protocolo DevTools/CDP y sockets nativos. Admite múltiples pestañas, ventanas independientes, iframes y contextos de navegador aislados. | **Inconveniente:** Se ejecuta dentro del mismo bucle de eventos del navegador, lo que impone limitaciones en el manejo de múltiples pestañas, dominios cruzados y control de bajo nivel. |
| **Soporte de navegadores** | Soporta Chromium, Firefox y WebKit (Safari) de forma homogénea en Linux, macOS y Windows. | Soporta Chromium y Firefox; el soporte de WebKit es experimental. |
| **Herramientas de depuración** | Dispone de Playwright Inspector, Trace Viewer y generador de código (`codegen`). | **Ventaja de Cypress:** El Test Runner interactivo de Cypress es muy maduro y visualmente intuitivo para depuración manual paso a paso en JavaScript. |

### 2. Frente a Selenium WebDriver

| Criterio | Playwright (`pytest-playwright`) | Selenium WebDriver |
| --- | --- | --- |
| **Manejo de sincronización (esperas)** | **Ventaja:** Mecanismo de *auto-waiting* integrado para elementos interactivos, navegación y peticiones de red. Crucial para Streamlit, cuyos elementos aparecen y desaparecen dinámicamente tras re-ejecutar el script. | **Inconveniente:** Requiere configurar esperas explícitas (`WebDriverWait`) frecuentes para evitar fallos por elementos no interactivos (*flakiness*). |
| **Gestión de navegadores y drivers** | **Ventaja:** Binarios de navegadores gestionados e instalados automáticamente (`playwright install`) sin desajustes de versiones de drivers locales (ChromeDriver, GeckoDriver). | **Inconveniente:** Depende de la instalación y sincronización manual o mediante librerías accesorias de drivers para cada navegador. |
| **Diagnóstico y rendimiento** | **Ventaja:** Generación integrada de trazas completas (*traces* con capturas de pantalla, árbol de red y consola) ante fallos; ejecución más rápida y ligera. | **Inconveniente:** Registro de diagnósticos más complejo de instrumentar y mayor sobrecarga de comunicación HTTP por comando con los drivers. |
| **Compatibilidad con navegadores legacy** | Enfocado en versiones modernas de los motores de navegación principales. | **Ventaja de Selenium:** Mayor compatibilidad con versiones antiguas y plataformas legacy que no forman parte de los objetivos del proyecto. |

### 3. Frente a Streamlit AppTest (Pruebas unitarias nativas en memoria)

| Criterio | Playwright (`pytest-playwright`) | Streamlit AppTest |
| --- | --- | --- |
| **Fidelidad con el usuario final** | **Ventaja:** Prueba la experiencia real en el navegador: renderizado HTML/CSS real, comportamiento del cliente WebSocket, accesibilidad y eventos de puntero/teclado. | **Inconveniente:** Simula el estado interno de widgets en Python sin renderizar el DOM del navegador ni verificar errores de frontend JS/CSS. |
| **Velocidad de ejecución** | Más lenta que la simulación en memoria al requerir levantar el proceso de Streamlit y el motor del navegador. | **Ventaja de AppTest:** Se ejecuta directamente en el proceso de test a nivel de microsegundos/milisegundos. |
| **Rol en el proyecto** | Diseñado para la verificación End-to-End de flujos críticos de la interfaz de usuario. | Complementario: adecuado para pruebas rápidas de lógica de presentación sin interacción real de navegador. |

## Consecuencias

- Se añade `pytest-playwright` al grupo de desarrollo en `pyproject.toml` gestionado por `uv`.
- La configuración del entorno local y de CI requiere el paso adicional `uv run playwright install chromium` para descargar el binario soportado.
- Los tests E2E deben organizarse en `tests/e2e/` y configurarse para ejecutar el servidor de Streamlit contra un puerto efímero o configurable, asegurando el aislamiento frente a instancias locales en ejecución.
- Toda prueba E2E debe cumplir con las directrices de aislamiento y determinismo establecidas en `.harness/rules/testing-standards.md`, sustituyendo las llamadas a la API de OpenAI por respuestas simuladas o dobles de prueba para evitar consumo de créditos y mitigar tiempos de espera aleatorios.
