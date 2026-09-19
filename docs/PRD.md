# Product Requirements Document

**Estado:** Inicial — basado en el comportamiento observable del repositorio a 17/09/2026.

## 1. Product Overview

### Product

`estimador-cag` es una API que recibe la transcripción de una reunión con un cliente y devuelve una estimación de un proyecto de software generada por un modelo LLM. La primera versión utiliza contexto aumentado generativo (CAG) mediante cuatro ejemplos de estimaciones sintéticas definidos en código.

### Product Goal

Producir una primera estimación estructurada y coherente de alcance, tareas, horas, costes, equipo y duración a partir de una transcripción, manteniendo visibles el modelo utilizado, el uso de tokens y el coste estimado.

### Problem

El repositorio parte de la necesidad de transformar información narrativa de reuniones en una estimación técnica reproducible con un formato y nivel de detalle consistentes. No hay evidencia en el repositorio sobre usuarios reales, frecuencia de uso, precisión esperada ni impacto económico; esas cuestiones permanecen abiertas.

### Current Scope

La API HTTP de la primera fase CAG: health check, recepción de una transcripción, generación mediante OpenAI Responses API, incorporación de ejemplos estáticos y devolución de la estimación con metadatos.

## 2. Users and Actors

### Solicitante de una estimación — ASSUMPTION

**Context:** Envía a la API la transcripción de una reunión con un cliente.

**Primary job:** Obtener una primera estimación de un proyecto de software sin convertir manualmente la conversación en tareas y costes.

**Desired outcome:** Recibir un texto de estimación en español, adaptado a la transcripción y con un desglose utilizable como punto de partida.

**Relevant permissions:** No hay autenticación ni autorización implementadas. La identidad y los límites del solicitante deben definirse antes de un uso multiusuario o público.

### API / sistema

**Context:** Valida la petición, compone el prompt, consulta OpenAI y serializa la respuesta.

**Primary job:** Mantener el contrato HTTP y separar transporte, configuración, contexto CAG y servicio LLM.

## 3. Jobs, Pains and Desired Outcomes

- **Job:** Convertir una transcripción en una estimación inicial.
- **Pain:** El texto de una reunión no está organizado directamente como tareas, horas, costes, equipo y duración.
- **Desired outcome:** Una estimación adaptable al alcance descrito, con totales coherentes y supuestos de tarifa explícitos cuando falten datos.
- **Límite conocido:** La salida de un LLM es orientativa; el repositorio no define todavía un umbral de precisión ni un proceso de revisión humana.

## 4. Product Principles

1. No atribuir al cliente requisitos que no aparezcan en la transcripción.
2. Usar los ejemplos CAG como referencia de formato y detalle, no como plantilla rígida.
3. Mantener separadas las responsabilidades de API, contratos, servicio, configuración y contexto.
4. Hacer visibles los metadatos de uso y coste cuando el proveedor los devuelva.
5. No presentar el coste estimado como una factura.

## 5. Scope

### Current / MVP

- `GET /health` para comprobar que el proceso responde.
- `POST /api/v1/estimate` con una transcripción no vacía.
- Interfaz de chat Streamlit para escribir o pegar transcripciones.
- Generación en español mediante OpenAI Responses API.
- Cuatro ejemplos estáticos de estimaciones como contexto CAG.
- Desglose de tareas, horas, costes, equipo y duración solicitado en las instrucciones del prompt.
- Devolución de estimación, modelo, proveedor, tokens, coste estimado, timestamp UTC e identificador de respuesta.
- Validación local y pruebas sin llamadas reales a OpenAI.

### Later

- Definir timeouts, reintentos, límites de concurrencia y tratamiento detallado de errores del proveedor.
- Ampliar la cobertura de modelos y proveedores cuando existan tarifas y contratos compatibles.
- Definir revisión humana, precisión esperada y criterios de aceptación de la calidad de la estimación.

### Future

- RAG con ingesta, embeddings y recuperación semántica de ejemplos relevantes.
- Agentes u orquestación especializada.
- Gestión de usuarios, autenticación, autorización y límites de uso si el producto pasa a ser multiusuario.

### Explicitly Out of Scope

- Presentar una estimación como compromiso contractual o presupuesto definitivo.
- Inferir requisitos no expresados en la transcripción.
- Afirmar que la calidad del resultado está validada por el hecho de que la llamada al LLM haya terminado correctamente.
- Elegir una base de datos vectorial o un proveedor adicional sin una decisión de producto y arquitectura.

## 6. User Journeys and Main Flows

### FLOW-ESTIMATION-001 — Generar una estimación

**Actor:** Solicitante de una estimación.

**Trigger:** Envía una petición `POST /api/v1/estimate`.

**Preconditions:** API disponible; proveedor configurado como `openai`; `OPENAI_API_KEY`, `LLM_MODEL`, `APP_ENV` y `LOG_LEVEL` configurados; el modelo tiene tarifas registradas.

**Main flow:**

1. El solicitante envía una transcripción.
2. La API elimina espacios extremos y rechaza una transcripción vacía.
3. El servicio comprueba proveedor, credenciales, modelo y tarifas.
4. El servicio compone instrucciones, cuatro ejemplos CAG y la nueva transcripción.
5. OpenAI genera la estimación.
6. La API devuelve la estimación y sus metadatos.

**Successful outcome:** El solicitante recibe una respuesta `200` con una estimación en español y los metadatos disponibles.

**Alternative paths:** Si OpenAI no devuelve datos de uso, `tokens_used` y `estimated_cost_usd` pueden ser `null`.

**Failure paths:** Petición inválida `422`; configuración o credenciales no utilizables `503`; error del proveedor o salida no utilizable `502`.

### FLOW-HEALTH-001 — Comprobar disponibilidad del proceso

**Actor:** Cliente técnico o monitor.

**Trigger:** Envía `GET /health`.

**Main flow:** La API responde `{"status": "ok"}`.

**Successful outcome:** Se confirma que el proceso HTTP responde; no se comprueba la disponibilidad de OpenAI.

### FLOW-ESTIMATION-002 — Generar una estimación desde el chat

**Actor:** Solicitante de una estimación.

**Trigger:** Escribe o pega una transcripción en el chat Streamlit.

**Preconditions:** Interfaz iniciada; configuración del proveedor disponible en `.env` o en el entorno; la sesión Streamlit tiene un historial inicializable.

**Main flow:**

1. La interfaz muestra el historial de mensajes de la sesión.
2. El solicitante introduce una transcripción mediante `st.chat_input`.
3. La interfaz muestra el texto como mensaje del usuario.
4. La interfaz llama al mismo servicio que el endpoint HTTP.
5. La interfaz muestra la estimación como mensaje del asistente y conserva ambos mensajes en `st.session_state`.

**Successful outcome:** El solicitante ve la estimación en el chat sin que el system prompt CAG ni la gestión de credenciales se dupliquen en la interfaz.

**Failure paths:** La interfaz muestra un error legible si la configuración está incompleta o el proveedor no devuelve una estimación.

## 7. Product Requirements

### REQ-ESTIMATION-001 — Recibir una transcripción

**Status:** Active

**Actor:** Solicitante de una estimación.

**Problem / Job:** Necesita enviar la conversación que sirve de base para estimar el proyecto.

**Expected outcome:** La API acepta texto no vacío y lo entrega al servicio sin espacios extremos.

**Requirement:** `POST /api/v1/estimate` debe aceptar un objeto con `transcription` de longitud mínima 1 después de eliminar espacios extremos.

**Priority:** Core

**Acceptance criteria:**

- Given una petición JSON con una transcripción no vacía, When se envía a `/api/v1/estimate`, Then la petición pasa la validación del contrato.
- Given una transcripción compuesta solo por espacios, When se envía a `/api/v1/estimate`, Then la API responde `422`.

**Edge cases:** La longitud mínima de 50 caracteres aparece como propuesta arquitectónica, pero no está activa.

**Related flows:** `FLOW-ESTIMATION-001`.

### REQ-ESTIMATION-002 — Generar una estimación contextualizada

**Status:** Active

**Actor:** Solicitante de una estimación.

**Problem / Job:** Necesita una estimación adaptada al alcance descrito, no una respuesta genérica.

**Expected outcome:** El servicio consulta OpenAI con instrucciones en español, cuatro ejemplos CAG y la transcripción como consulta del usuario.

**Requirement:** El servicio debe usar la API Responses de OpenAI de forma asíncrona y devolver el texto generado, sin añadir requisitos ausentes de la transcripción.

**Priority:** Core

**Acceptance criteria:**

- Given una configuración válida y una transcripción, When el servicio llama al proveedor, Then el input contiene un elemento `system` con instrucciones y ejemplos y un elemento `user` con la transcripción.
- Given una respuesta del proveedor con texto, When la API la procesa, Then devuelve el texto sin espacios exteriores.
- Given una respuesta sin texto utilizable, When la API la procesa, Then responde con un error de proveedor `502`.

**Dependencies:** OpenAI Responses API, `OPENAI_API_KEY`, `LLM_PROVIDER`, `LLM_MODEL` y `MODEL_RATES`.

**Related flows:** `FLOW-ESTIMATION-001`.

### REQ-ESTIMATION-003 — Devolver metadatos de estimación

**Status:** Active

**Actor:** Solicitante de una estimación.

**Problem / Job:** Necesita interpretar el resultado y conocer el coste orientativo de la llamada.

**Expected outcome:** La respuesta incluye metadatos suficientes para identificar el modelo y observar el uso.

**Requirement:** La API debe devolver `estimation`, `model`, `provider`, `tokens_used`, `estimated_cost_usd`, `timestamp` y `response_id`.

**Priority:** Important

**Acceptance criteria:**

- Given una respuesta del proveedor con uso, When se devuelve la estimación, Then `tokens_used` contiene tokens de entrada, salida, totales y caché.
- Given tarifas conocidas y uso disponible, When se devuelve la estimación, Then `estimated_cost_usd` es no negativo y orientativo.
- Given uso ausente, When se devuelve la estimación, Then los metadatos de uso y coste pueden ser `null`.

### REQ-STREAMLIT-001 — Conversación de estimación en Streamlit

**Status:** Active

**Actor:** Solicitante de una estimación.

**Problem / Job:** Necesita introducir una transcripción de forma interactiva y consultar la estimación dentro de una conversación visible.

**Expected outcome:** La interfaz permite enviar texto y muestra la respuesta del LLM como mensaje del asistente, conservando el contexto visible durante la sesión.

**Requirement:** La aplicación Streamlit debe usar `st.chat_message`, `st.chat_input` y `st.session_state`; debe delegar en `generate_estimation_details` para reutilizar el system prompt y la lógica CAG del endpoint; y no debe contener una API key.

**Priority:** Important

**Acceptance criteria:**

- Given una sesión Streamlit, When el solicitante introduce una transcripción, Then la interfaz muestra el texto como mensaje `user`.
- Given una transcripción válida y configuración disponible, When el servicio responde, Then la interfaz muestra `result.estimation` como mensaje `assistant`.
- Given mensajes previos en la sesión, When Streamlit vuelve a ejecutar el script, Then el historial sigue visible mediante `st.session_state`.
- Given una configuración sin API key o un error del proveedor, When se intenta generar la estimación, Then la interfaz muestra un error sin exponer credenciales.

**Dependencies:** Streamlit, `app.services.llm_service.generate_estimation_details` y la configuración existente en `.env`.

**Related flows:** `FLOW-ESTIMATION-002`.

### REQ-HEALTH-001 — Comprobar que la API responde

**Status:** Active

**Actor:** Monitor o cliente técnico.

**Problem / Job:** Necesita detectar si el proceso HTTP está atendiendo peticiones.

**Expected outcome:** Un endpoint sencillo confirma la respuesta del proceso sin depender del LLM.

**Requirement:** `GET /health` debe devolver `{"status": "ok"}`.

**Priority:** Core

**Acceptance criteria:**

- Given el proceso HTTP activo, When se solicita `/health`, Then la respuesta es `200` con `{"status": "ok"}`.
- Given el proveedor OpenAI no disponible, When se solicita `/health`, Then el endpoint no intenta consultar OpenAI.

## 8. Business Rules

### RULE-ESTIMATION-001 — No inventar requisitos

**Rule:** La estimación no debe atribuir al cliente requisitos que no aparezcan en la transcripción.

**Reason:** Evitar que el resultado supere el alcance conocido de la reunión.

**Applies to:** Instrucciones del prompt y contenido generado.

### RULE-ESTIMATION-002 — Tarifas explícitas por modelo

**Rule:** No se puede usar un modelo sin tarifas registradas en `MODEL_RATES`.

**Reason:** Mantener coherente el cálculo del coste orientativo.

**Applies to:** Generación de estimaciones con uso de tokens.

**Exceptions:** Ninguna definida.

### RULE-ESTIMATION-003 — Coste no contractual

**Rule:** `estimated_cost_usd` representa el coste orientativo de la llamada al proveedor, no un precio final para el cliente.

**Reason:** El resultado no incluye todavía reglas comerciales, margen, impuestos, contingencia ni validación humana.

## 9. Product Data Model

### EstimationRequest

**Purpose:** Representar la transcripción de entrada.

**Key fields:** `transcription`.

**Important constraints:** Cadena no vacía después de eliminar espacios extremos.

### EstimationResponse

**Purpose:** Representar la estimación y sus metadatos.

**Key fields:** `estimation`, `model`, `provider`, `tokens_used`, `estimated_cost_usd`, `timestamp`, `response_id`.

**Lifecycle / states:** No se ha definido persistencia ni ciclo de vida; la respuesta se devuelve en línea.

### TokenUsage

**Purpose:** Informar del consumo de tokens de una respuesta.

**Key fields:** `input_tokens`, `output_tokens`, `total_tokens`, `cached_input_tokens`.

## 10. Roles and Permissions

No hay autenticación, autorización, propiedad de datos ni separación de tenants implementadas. Antes de exponer la API a múltiples usuarios debe definirse quién puede enviar transcripciones, consultar resultados y conocer el coste.

## 11. UX Requirements

La interfaz actual incluye la API HTTP y el chat Streamlit; no existe una UI web persistente más allá de la sesión actual.

La interfaz Streamlit ofrece un chat de sesión única. No hay autenticación, persistencia entre sesiones ni sincronización entre usuarios.

### Success

Respuesta `200` con la estimación y los metadatos disponibles.

### Validation error

Respuesta `422` cuando falta la transcripción o está vacía.

### Configuration error

Respuesta `503` cuando el proveedor, la API key, el modelo o sus tarifas no son utilizables.

### Provider error

Respuesta `502` cuando OpenAI falla o no devuelve texto utilizable.

### Streamlit chat

La entrada se realiza con `st.chat_input`, los mensajes se representan con `st.chat_message` y el historial se mantiene en `st.session_state`. Los errores se muestran dentro del mensaje del asistente.

### Loading / timeout

No hay comportamiento de timeout definido; queda como decisión pendiente.

## 12. Analytics and Success

### Product outcome

Reducir el trabajo manual necesario para convertir una transcripción en una primera estimación utilizable.

### Success metric

Threshold not yet defined. El repositorio no contiene datos de uso, evaluación de calidad ni feedback de usuarios.

### Supporting metrics

- Proporción de peticiones que devuelven `200`.
- Latencia de generación.
- Coste estimado por petición.
- Porcentaje de respuestas revisadas y aceptadas por una persona.

Estas métricas son propuestas de observación, no instrumentación existente.

### Relevant events

No hay eventos de analítica implementados.

## 13. Validation

### HYP-ESTIMATION-001 — El contexto CAG mejora la utilidad de la primera estimación

**Hypothesis:** Los ejemplos previos ayudan a producir estimaciones con formato y nivel de detalle consistentes.

**Why it matters:** Es la premisa principal de la fase CAG.

**Evidence currently available:** Tests que verifican que los cuatro ejemplos se envían al prompt; no hay evaluación de calidad por expertos ni usuarios.

**How it can be tested:** Comparar estimaciones con y sin contexto CAG sobre un conjunto de transcripciones representativas y revisión ciega de utilidad, cobertura y coherencia.

**Success signal:** Threshold not yet defined; debe establecerse antes de declarar validada la hipótesis.

**Failure signal:** Revisores no detectan mejora o encuentran que los ejemplos inducen requisitos no presentes.

**Decision if supported:** Mantener CAG y seleccionar ejemplos por relevancia cuando exista evidencia.

**Decision if unsupported:** Revisar ejemplos, prompt o estrategia de contexto antes de ampliar alcance.

## 14. Risks and Assumptions

### Assumptions

- El solicitante puede proporcionar una transcripción suficientemente informativa.
- El español es el idioma de salida requerido para esta fase.
- Cuatro ejemplos sintéticos son un contexto inicial útil.
- `gpt-4o-mini` y sus tarifas configuradas son adecuados para el prototipo.

### Product risks

- Una estimación plausible puede ser incorrecta y no existe todavía un mecanismo de revisión o confianza.
- La salida puede variar entre llamadas del proveedor.
- El texto de la reunión puede contener datos sensibles; no hay política de retención, anonimización o control de acceso definida.
- El coste y la latencia pueden crecer con transcripciones o contextos mayores.

### Technical risks affecting product behaviour

- Timeouts, reintentos y límites de concurrencia están pendientes.
- Solo está implementado el proveedor OpenAI.
- La restricción de transcripción mínima de 50 caracteres está documentada como propuesta, pero no aplicada.

### Legal / privacy / compliance risks

No hay conclusiones legales en el repositorio. Debe revisarse el tratamiento de transcripciones antes de usar datos reales de clientes.

## 15. Open Questions

1. ¿Quién es el usuario principal y quién revisa o aprueba la estimación?
2. ¿Qué precisión, coherencia o utilidad mínima debe alcanzar una estimación?
3. ¿Debe aplicarse una longitud mínima de 50 caracteres u otra validación de calidad?
4. ¿La estimación debe persistirse, exportarse o compartirse?
5. ¿Qué política de privacidad, retención y anonimización aplica a las transcripciones?
6. ¿Se necesitarán autenticación, autorización, cuotas o separación por cliente?
7. ¿Qué timeout, reintentos y comportamiento de degradación espera el usuario?
8. ¿Qué tarifa, margen, impuestos o contingencia deben formar parte de un presupuesto final?
9. ¿Cómo se evaluará el valor del CAG y cuándo se justificará evolucionar a RAG?

## 16. Product Decisions

- **DEC-2026-09-17-001 — API FastAPI:** El proyecto usa FastAPI sobre ASGI y separa composición, transporte, contratos, servicio y contexto. Detalle técnico en [ADR-001](decisions/ADR-001-fastapi.md).
- **DEC-2026-09-17-002 — Contexto CAG estático:** La primera fase usa cuatro ejemplos sintéticos definidos en código; RAG queda para una fase posterior.
- **DEC-2026-09-17-003 — Proveedor inicial OpenAI:** El servicio admite actualmente `openai` y exige tarifas explícitas para el modelo configurado.
- **DEC-2026-09-17-004 — Interfaz Streamlit sobre el servicio existente:** El chat reutiliza `generate_estimation_details` para mantener el mismo prompt CAG, configuración y gestión de credenciales que la API HTTP.

Estas decisiones reflejan el estado observable del repositorio; las decisiones de producto aún no confirmadas permanecen como supuestos u open questions.

## 17. Change Log

| Date | Change | Requirements affected | Reason |
|---|---|---|---|
| 2026-09-17 | Creación del PRD inicial a partir de README, arquitectura, código y tests existentes. | REQ-ESTIMATION-001, REQ-ESTIMATION-002, REQ-ESTIMATION-003, REQ-HEALTH-001 | Establecer una fuente de intención de producto y separar comportamiento implementado de trabajo futuro. |
| 2026-09-17 | Incorporación de una interfaz de chat Streamlit con historial de sesión y reutilización del servicio CAG. | REQ-STREAMLIT-001 | Facilitar la introducción interactiva de transcripciones sin duplicar el prompt ni las credenciales. |
