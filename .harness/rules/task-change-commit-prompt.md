---
trigger: always_on
---

# Confirmación de commit al cambiar de tarea

- **MUST** distinguir entre una aclaración o ajuste de la tarea activa y una solicitud materialmente distinta.
- **MUST** preguntar antes de iniciar una tarea materialmente distinta si existen cambios locales no confirmados de la tarea anterior:
  > Has cambiado de tarea. ¿Quieres que haga commit de los cambios realizados hasta ahora antes de continuar?
- **MUST NOT** crear el commit automáticamente sin una respuesta afirmativa y explícita del usuario.
- **MUST** continuar con la nueva tarea sin crear commit si el usuario responde negativamente.
- **MUST NOT** hacer la pregunta si no existen cambios locales pendientes o si la tarea anterior ya está finalizada y confirmada.
