# Protocolo portable de runner

Los scripts delegan la ejecución en un adaptador externo. El adaptador puede
envolver cualquier agente, API o CLI; el núcleo solo conoce este contrato JSON.

## Transporte

- Proporciona el comando como lista JSON mediante `--runner-command-json` o en
  un archivo mediante `--runner-config`.
- El proceso recibe una solicitud JSON por entrada estándar.
- Debe devolver exactamente un objeto JSON por salida estándar.
- Los diagnósticos pertenecen a la salida de error.
- El núcleo ejecuta sin shell y aplica un timeout.

```json
{"command": ["agent-runner", "--json"]}
```

## Operación `evaluate_trigger`

```json
{
  "operation": "evaluate_trigger",
  "query": "Solicitud realista",
  "skill": {
    "name": "example-skill",
    "description": "Qué hace y cuándo usarla",
    "path": "/absolute/path/to/example-skill"
  },
  "model": "optional-model"
}
```

Respuesta mínima:

```json
{"triggered": true}
```

El adaptador debe exponer la skill, ejecutar en contexto limpio y detectar la
activación mediante señales reales del host.

## Operación `generate_text`

```json
{
  "operation": "generate_text",
  "prompt": "Instrucciones para optimizar la descripción",
  "model": "optional-model"
}
```

Respuesta mínima:

```json
{"text": "Respuesta generada"}
```

## Errores

El adaptador termina con código distinto de cero y escribe un diagnóstico sin
secretos en la salida de error. Una respuesta vacía, JSON inválido o campos
obligatorios ausentes es un error, nunca un resultado negativo silencioso.
