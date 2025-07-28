#!/usr/bin/env bash
set -euo pipefail

# Build the Docker image
docker build -t churn-api .

# Run the container in detached mode
docker run --rm -d -p 8000:8000 --name churn-api churn-api

echo "🚀 churn-api is running at http://localhost:8000"
