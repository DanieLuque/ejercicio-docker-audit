# Reporte de lo Realizado - Ejercicio Docker Audit

---

## FASE 1 — Auditoría

### Qué se hizo
REALIZADO. Se ejecutó un análisis estático de seguridad con Bandit sobre el código fuente del proyecto, enfocándose únicamente en archivos propios (excluyendo `venv` y `__pycache__`). Los hallazgos se registraron en un archivo de auditoría.

### Herramientas utilizadas
- `bandit` (ejecutado desde el entorno virtual del proyecto: `venv/bin/bandit`)

### Archivos creados o modificados
- `AUDITORIA.md` (creado)

### Vulnerabilidades encontradas
Se encontraron 6 vulnerabilidades:

| # | ID | Archivo | Línea | Descripción | Severidad | Confianza | CWE |
|---|-----|---------|-------|-------------|-----------|-----------|-----|
| 1 | B105 | `app.py` | 10 | Contraseña hardcodeada en texto plano (`DB_PASS`) | Low | Medium | CWE-259 |
| 2 | B608 | `app.py` | 25 | Inyección SQL por concatenación de entrada del usuario | Medium | Low | CWE-89 |
| 3 | B311 | `app.py` | 30 | Uso de `random` no criptográficamente seguro | Low | High | CWE-330 |
| 4 | B201 | `app.py` | 35 | `debug=True` en Flask expone ejecución remota de código | High | Medium | CWE-94 |
| 5 | B104 | `app.py` | 35 | Enlace a todas las interfaces (`0.0.0.0`) | Medium | Medium | CWE-605 |
| 6 | B101 | `test_app.py` | 7 | Uso de `assert` en pruebas (eliminado en bytecode optimizado) | Low | High | CWE-703 |

### Resultados obtenidos
- **High:** 1
- **Medium:** 2
- **Low:** 3
- **Total:** 6 hallazgos
