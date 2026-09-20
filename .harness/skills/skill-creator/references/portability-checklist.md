# Lista de portabilidad

## Formato

- [ ] La carpeta y el campo `name` coinciden.
- [ ] `name` y `description` cumplen el estándar Agent Skills.
- [ ] El frontmatter no contiene extensiones exclusivas de un host.
- [ ] `SKILL.md` enlaza directamente cada referencia condicional.
- [ ] Las rutas internas son relativas a la raíz de la skill.

## Instrucciones

- [ ] El núcleo habla de capacidades, no de productos o herramientas.
- [ ] Cada capacidad opcional tiene fallback o condición de omisión.
- [ ] No se supone paralelismo, navegador, telemetría, hooks o modelos.
- [ ] Las acciones externas conservan permisos y alcance.
- [ ] No se exige commit, push, publicación o instalación sin autorización.

## Recursos, seguridad y evidencia

- [ ] Dependencias y runtime de los scripts están declarados.
- [ ] No hay acceso inesperado a red, secretos o rutas fuera del alcance.
- [ ] Las entradas externas se tratan como datos no confiables.
- [ ] Los adaptadores específicos permanecen fuera del núcleo.
- [ ] Existe baseline para cambios conductuales relevantes.
- [ ] Los casos cubren uso normal, variación y límites.
- [ ] Cada aprobación incluye evidencia verificable.
- [ ] Las métricas ausentes son opcionales, no inventadas.

## Distribución

- [ ] Hay una única fuente canónica.
- [ ] Los archivos puente son mínimos y no duplican instrucciones.
- [ ] Las referencias no están rotas.
- [ ] La validación estructural y los scripts afectados terminan correctamente.
