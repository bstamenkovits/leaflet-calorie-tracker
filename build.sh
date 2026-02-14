#!/bin/bash

# Exit on error
set -e

echo "Building frontend..."
cd frontend
npm install
npx ng build

echo "Installing backend dependencies..."
cd ../backend
pip install -r requirements.txt
