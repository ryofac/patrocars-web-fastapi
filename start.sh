#!/bin/bash
# Rodar migrações com o Alembic
alembic upgrade head

# Iniciar o servidor FastAPI
uvicorn patrocars.app:app --host 0.0.0.0 --port 8000