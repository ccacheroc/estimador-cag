"""Casos sintéticos de estimaciones para usar como referencias en el prompt."""

from textwrap import dedent


ESTIMATION_EXAMPLES: list[dict[str, str]] = [
    {
        "meeting_summary": dedent(
            """\
            Una empresa de distribución con dos almacenes quiere consultar existencias
            desde el navegador, registrar entradas y salidas, importar su catálogo
            inicial por CSV y recibir avisos de stock bajo. El personal podrá operar
            el inventario y los administradores gestionarán usuarios. La primera
            versión no necesita integración con su ERP.
            """
        ).strip(),
        "estimation": dedent(
            """\
            ## Estimación: Gestión de inventario para dos almacenes

            Tarifa ilustrativa: 60 €/hora. Costes de desarrollo sin IVA ni licencias.

            ### Desglose de tareas
            1. Análisis funcional y diseño UI/UX: 36 horas × 60 €/hora = 2.160 €
            2. API de productos, movimientos y existencias: 72 horas × 60 €/hora = 4.320 €
            3. Interfaz de catálogo y operaciones de almacén: 56 horas × 60 €/hora = 3.360 €
            4. Autenticación y roles: 28 horas × 60 €/hora = 1.680 €
            5. Importación CSV y alertas de stock bajo: 24 horas × 60 €/hora = 1.440 €
            6. Pruebas, correcciones y despliegue: 32 horas × 60 €/hora = 1.920 €

            **Total estimado: 248 horas · 14.880 €**
            **Equipo recomendado: 2 desarrolladores full-stack + 1 diseñador UI/UX (a tiempo parcial)**
            **Duración estimada: 6-8 semanas**
            """
        ).strip(),
    },
    {
        "meeting_summary": dedent(
            """\
            Una clínica de fisioterapia con tres sedes quiere que sus pacientes
            reserven y cancelen citas online según la disponibilidad de cada
            profesional. Recepción necesita bloquear horarios, consultar la agenda
            y enviar recordatorios por correo. Se pide exportar las reservas a
            Google Calendar, sin sincronización bidireccional en esta fase.
            """
        ).strip(),
        "estimation": dedent(
            """\
            ## Estimación: Portal de reservas para clínica

            Tarifa ilustrativa: 60 €/hora. Costes de desarrollo sin IVA ni licencias.

            ### Desglose de tareas
            1. Flujos de reserva y diseño UI/UX: 28 horas × 60 €/hora = 1.680 €
            2. API de disponibilidad, reservas y cancelaciones: 60 horas × 60 €/hora = 3.600 €
            3. Portal de pacientes y agenda de recepción: 56 horas × 60 €/hora = 3.360 €
            4. Exportación de citas a Google Calendar: 32 horas × 60 €/hora = 1.920 €
            5. Correos de confirmación y recordatorio: 20 horas × 60 €/hora = 1.200 €
            6. Pruebas, correcciones y despliegue: 28 horas × 60 €/hora = 1.680 €

            **Total estimado: 224 horas · 13.440 €**
            **Equipo recomendado: 2 desarrolladores full-stack + 1 diseñador UI/UX (a tiempo parcial)**
            **Duración estimada: 5-7 semanas**
            """
        ).strip(),
    },
    {
        "meeting_summary": dedent(
            """\
            Un operador logístico quiere reunir datos de entregas procedentes
            de dos sistemas externos en un panel interno actualizado cada día.
            Dirección necesita ver entregas a tiempo, retrasos por zona y
            evolución mensual, con filtros y exportación CSV. No se solicita
            predicción de retrasos ni actualización en tiempo real.
            """
        ).strip(),
        "estimation": dedent(
            """\
            ## Estimación: Panel de indicadores logísticos

            Tarifa ilustrativa: 60 €/hora. Costes de desarrollo sin IVA ni licencias.

            ### Desglose de tareas
            1. Requisitos, indicadores y diseño de datos: 40 horas × 60 €/hora = 2.400 €
            2. Integración con dos APIs y carga diaria: 80 horas × 60 €/hora = 4.800 €
            3. Modelo de datos y consultas agregadas: 48 horas × 60 €/hora = 2.880 €
            4. Panel con gráficos y filtros: 64 horas × 60 €/hora = 3.840 €
            5. Control de acceso y exportación CSV: 32 horas × 60 €/hora = 1.920 €
            6. Pruebas, monitorización y despliegue: 40 horas × 60 €/hora = 2.400 €

            **Total estimado: 304 horas · 18.240 €**
            **Equipo recomendado: 1 ingeniero de datos + 1 desarrollador full-stack + 1 especialista QA (a tiempo parcial)**
            **Duración estimada: 7-9 semanas**
            """
        ).strip(),
    },
    {
        "meeting_summary": dedent(
            """\
            Una consultora de 120 empleados quiere sustituir las solicitudes
            de compra por correo por un portal interno. Cada solicitud tendrá
            adjuntos y pasará por aprobación del responsable y de finanzas según
            el importe. El cliente necesita avisos y un historial auditable; la
            firma electrónica y la conexión contable quedan fuera del alcance.
            """
        ).strip(),
        "estimation": dedent(
            """\
            ## Estimación: Flujo interno de aprobación de compras

            Tarifa ilustrativa: 60 €/hora. Costes de desarrollo sin IVA ni licencias.

            ### Desglose de tareas
            1. Análisis del proceso y diseño de pantallas: 32 horas × 60 €/hora = 1.920 €
            2. API de solicitudes, estados y aprobaciones: 72 horas × 60 €/hora = 4.320 €
            3. Portal de empleados y revisores: 68 horas × 60 €/hora = 4.080 €
            4. Roles, avisos e historial de cambios: 36 horas × 60 €/hora = 2.160 €
            5. Gestión y almacenamiento de adjuntos: 40 horas × 60 €/hora = 2.400 €
            6. Pruebas, correcciones y despliegue: 36 horas × 60 €/hora = 2.160 €

            **Total estimado: 284 horas · 17.040 €**
            **Equipo recomendado: 2 desarrolladores full-stack + 1 especialista QA (a tiempo parcial)**
            **Duración estimada: 6-8 semanas**
            """
        ).strip(),
    },
]
