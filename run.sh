#!/bin/bash

# Navigate to backend source directory
cd backend/src

# Start FastAPI app with Gunicorn and Uvicorn workers
echo "Starting FastAPI backend..."
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
