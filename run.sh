#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " NoCountry - Acelerador de Integraciones Open Source (B2B)"
echo "=========================================================="

PORT=${PORT:-8080}
HOST=${HOST:-"0.0.0.0"}

echo "Verificando entorno de ejecución..."
python3 --version

echo "Inicializando base de datos SQLite con FTS5..."
python3 -c "from backend.database import init_db, seed_if_empty; init_db(); count = seed_if_empty(); print(f'Catálogo cargado con {count} repositorios.')"

echo ""
echo "-> Servidor web listo en: http://localhost:${PORT}"
echo "-> Presiona Ctrl+C para detener."
echo ""

exec python3 backend/app.py
