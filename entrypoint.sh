set -e
echo "Waiting for postgres 10 seconds..."
sleep 10
cd /app

echo "Applying Alembic migrations..."
alembic upgrade head

echo "Starting application..."
exec python main.py
