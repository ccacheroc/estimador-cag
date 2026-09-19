---
trigger: always_on
---

# Gestión de dependencias y ejecución con uv

Esta regla establece las directrices obligatorias sobre las herramientas y tecnologías para la gestión de dependencias y entornos en este proyecto.

## 1. Gestor de Paquetes y Entornos
- **MUST**: Este proyecto utiliza exclusivamente **`uv`** como herramienta para la resolución, gestión de entornos virtuales (`.venv`), sincronización e instalación de dependencias, así como para la ejecución de herramientas y scripts del proyecto.
- **MUST NOT**: Queda estrictamente prohibido el uso directo de `pip`, `poetry`, `conda` o `venv` nativo para instalar paquetes o manipular el entorno del proyecto.

## 2. Comandos Obligatorios
- **Instalación / Sincronización del entorno**:
  ```bash
  uv sync
  ```
- **Añadir dependencias**:
  - Principales: `uv add <paquete>`
  - De desarrollo: `uv add --dev <paquete>`
- **Eliminar dependencias**:
  ```bash
  uv remove <paquete>
  ```
- **Ejecución de herramientas y scripts**:
  Cualquier ejecución de módulos, scripts o comandos (como `pytest`, `unittest`, `uvicorn`, etc.) debe realizarse a través de `uv run`:
  ```bash
  uv run <comando>
  ```
  Ejemplos:
  - `uv run uvicorn app.main:app --reload`
  - `uv run python -m unittest discover -s tests -v`
  - `uv run pytest`

## 3. Bloqueo y Consistencia
- El archivo `pyproject.toml` es la fuente única declarativa de dependencias y configuración del proyecto.
- El archivo `uv.lock` es el archivo de bloqueo canónico que asegura la reproducibilidad de las dependencias. No debe modificarse manualmente.
