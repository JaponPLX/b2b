#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " NoCountry - Acelerador de Integraciones Open Source (B2B)"
echo " Servidor Habilitado para Multiples Dispositivos (PWA)"
echo "=========================================================="

PORT=${PORT:-8080}
HOST=${HOST:-"0.0.0.0"}

# Soporte para apertura automatica de tunel publico mundial
if [ "$1" == "--public" ] || [ "$1" == "-p" ] || [ "$2" == "--public" ]; then
  exec ./public_tunnel.sh "$PORT"
fi

echo "Verificando entorno de ejecucion..."
python3 --version

echo "Inicializando base de datos SQLite con FTS5..."
python3 -c "from backend.database import init_db, seed_if_empty; init_db(); count = seed_if_empty(); print(f'Catalogo cargado con {count} repositorios.')"

exec python3 backend/app.py "$PORT"
