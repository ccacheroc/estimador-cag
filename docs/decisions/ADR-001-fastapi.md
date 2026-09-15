# ADR-001: FastAPI para la API de estimaciones

**Estado:** Aceptada

## Contexto

El estimador CAG expondrá una API que recibe la transcripción de una reunión, incorpora ejemplos de estimaciones al prompt y consulta un LLM externo. La espera de esa respuesta es I/O de red y puede ser mucho más larga que el trabajo local de validación o serialización. La latencia y la concurrencia reales dependerán del proveedor, el modelo, la carga y el despliegue; este proyecto aún no tiene mediciones.

El repositorio usa Python, declara FastAPI, Pydantic Settings y el SDK de OpenAI, y separa `app/main.py`, `routers/`, `services/` y `context/`. Un prototipo en un único `main.py` podría mezclar endpoint HTTP, configuración del cliente, prompt, llamada LLM y formato de respuesta. Esa mezcla dificultaría añadir proveedores, probar el prompt o cambiar el contrato de la API. La [arquitectura prevista](../architecture.md) asigna cada responsabilidad a una capa.

## Decisión

Usar **FastAPI sobre ASGI** para la API HTTP del estimador. Los routers recibirán, validarán, delegarán al servicio y devolverán respuestas con contratos Pydantic. El servicio construirá el prompt, utilizará el contexto CAG y realizará la llamada al proveedor. `app/main.py` compondrá la aplicación y registrará los routers.

Las rutas que esperen operaciones de red asíncronas usarán `async def` y un cliente compatible con `await`. Una llamada síncrona al SDK dentro de una ruta `async` bloquearía el event loop; la mera presencia de `async def` no aporta concurrencia durante esa llamada. La [guía de FastAPI](https://fastapi.tiangolo.com/async/) distingue las bibliotecas que admiten `await` de las llamadas bloqueantes y explica cuándo usar una ruta síncrona.

FastAPI es una elección del proyecto por su encaje con el stack Python y por sus mecanismos de `APIRouter` y modelos de entrada y salida. No se adopta una cifra de peticiones concurrentes ni una ventaja de memoria como garantía sin una prueba de carga de esta aplicación.

## Alternativas consideradas

| Alternativa | Capacidad relevante | Motivo para no elegirla en esta fase |
| --- | --- | --- |
| **Django** | Con ASGI admite vistas y un stack de petición asíncronos; bajo WSGI las vistas async tienen una adaptación por petición y no obtienen la misma eficiencia para solicitudes largas. El middleware síncrono puede requerir un hilo. [Documentación de Django](https://docs.djangoproject.com/en/6.0/topics/async/). | Su plataforma completa de ORM, administración y plantillas no es necesaria para esta API centrada en un LLM y ejemplos estáticos. Django ASGI sería una opción válida si esas capacidades pasan a ser requisitos. |
| **Rails con Puma** | Puma usa un pool de hilos y puede solapar esperas de I/O; una petición que espera una API externa ocupa recursos del pool hasta terminar. Se pueden ajustar hilos y procesos. [Documentación de Puma](https://github.com/puma/puma/blob/main/README.md). | Para este servicio independiente exigiría incorporar Ruby junto al código CAG y de configuración que ya está en Python. Sería razonable si la estimación debiera integrarse dentro de una aplicación Rails existente. |
| **Express sobre Node.js** | Node.js también usa un event loop y admite I/O de red no bloqueante. [Documentación de Node.js](https://nodejs.org/learn/asynchronous-work/dont-block-the-event-loop). | La concurrencia no lo descarta; la elección evitaría trasladar a JavaScript el paquete Python, los modelos Pydantic y la integración LLM ya iniciados. |

## Consecuencias

- La API puede mantener separados transporte, contratos, lógica LLM y contexto. `APIRouter` facilita registrar rutas desde módulos y Pydantic permite documentar y validar respuestas. [Guía de aplicaciones en varios archivos de FastAPI](https://fastapi.tiangolo.com/tutorial/bigger-applications/), [guía de modelos de respuesta](https://fastapi.tiangolo.com/tutorial/response-model/).
- El beneficio de concurrencia requiere I/O asíncrona de extremo a extremo. Si una dependencia solo ofrece operaciones bloqueantes, habrá que ejecutarla fuera del event loop o usar una ruta síncrona. Esto incluye evitar el cliente síncrono `OpenAI` directamente dentro del ejemplo de endpoint `async` aportado como contexto.
- La integración LLM tendrá que definir timeouts, tratamiento de errores, reintentos y límites de concurrencia. El número de workers y la capacidad deberán ajustarse con mediciones de carga y límites del proveedor.
- La facilidad para crear una API en un archivo no elimina la obligación de mantener routers delgados y la lógica en servicios. Las pruebas del prompt podrán ejecutarse sin HTTP y las pruebas HTTP podrán sustituir la llamada real al LLM.
- Esta decisión fija el framework HTTP. El servicio asíncrono de OpenAI, `POST /api/v1/estimate` y `GET /health` ya están implementados.
