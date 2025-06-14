#!/bin/sh
set -e
echo "Waiting for postgres"
sleep 10
# Перейдём в директорию app, если alembic.ini там
cd /app

echo "Applying Alembic migrations..."
alembic upgrade head

echo "Starting application..."
exec python main.py
