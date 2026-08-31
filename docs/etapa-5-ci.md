# Etapa 5 — Integración continua (GitHub Actions)

`.github/workflows/ci.yml` define un workflow que corre automáticamente en cada `push` o
`pull request` contra la rama `main`.

## Pasos del workflow

1. **Checkout** del repositorio.
2. **Configurar Python 3.10**.
3. **Instalar dependencias** (`docker/requirements.txt` + `requirements-dev.txt`).
4. **Lint con `flake8`** sobre `app/` y `tests/`.
5. **Tests con `pytest`** sobre la API (`tests/test_api.py`).

## Resultado

```{code} text
✓ Set up job
✓ Checkout del repositorio
✓ Configurar Python
✓ Instalar dependencias
✓ Lint con flake8      → 0 issues
✓ Tests con pytest     → 4 / 4 passed
✓ Complete job

Duración total: 57s
```

Puedes ver el historial de ejecuciones en la pestaña
[Actions](https://github.com/valeriaflorezs/heart-disease-mlops/actions) del repositorio.
