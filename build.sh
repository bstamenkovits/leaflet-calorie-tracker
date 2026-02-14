#!/bin/bash

# Exit on error
set -e

echo "Building frontend..."
cd frontend
npm install
npx ng build

echo "Starting FastAPI backend..."
cd ../backend
pip install -r requirements.txt
