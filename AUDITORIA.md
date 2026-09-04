# Auditoría de Seguridad - Fase 1

## Resultados Bandit (Código propio)

| # | ID | Archivo | Línea | Descripción | Severidad | Confianza | CWE |
|---|-----|---------|-------|-------------|-----------|-----------|-----|
| 1 | B105 | `app.py` | 10 | Contraseña hardcodeada en texto plano (`DB_PASS`) | Low | Medium | CWE-259 |
| 2 | B608 | `app.py` | 25 | Inyección SQL por concatenación de entrada del usuario | Medium | Low | CWE-89 |
| 3 | B311 | `app.py` | 30 | Uso de `random` no criptográficamente seguro | Low | High | CWE-330 |
| 4 | B201 | `app.py` | 35 | `debug=True` en Flask expone ejecución remota de código | High | Medium | CWE-94 |
| 5 | B104 | `app.py` | 35 | Enlace a todas las interfaces (`0.0.0.0`) | Medium | Medium | CWE-605 |
| 6 | B101 | `test_app.py` | 7 | Uso de `assert` en pruebas (eliminado en bytecode optimizado) | Low | High | CWE-703 |

## Resumen

- **High:** 1
- **Medium:** 2
- **Low:** 3

## Comando ejecutado

```bash
bandit -r . -x ./venv,./__pycache__ -f txt
```

> Nota: Se excluyeron `venv` y `__pycache__` para analizar únicamente el código fuente de la aplicación.
