#!/usr/bin/env bash
set -euo pipefail

echo "Starting Quicklab local services"
docker compose up --build
