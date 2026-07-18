#!/bin/bash
echo "Running pre-start script: Downloading dataset..."
python download_data.py

echo "Starting Uvicorn server..."
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
