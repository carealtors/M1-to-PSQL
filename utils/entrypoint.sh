#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h 127.0.0.1 -p 5432 -U postgres; do
  sleep 2
done

echo "PostgreSQL is ready!"

# Run the initial Python scripts after the database is ready
echo "Running Python scripts..."
/app/venv/bin/python /app/parse_ach.py

# Start the PostgreSQL server (default entrypoint)
/usr/local/bin/docker-entrypoint.sh postgres
