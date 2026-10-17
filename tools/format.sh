#!/usr/bin/env bash
set -euo pipefail

echo "Formatting Quicklab project"
if command -v black >/dev/null 2>&1; then
  black backend
fi

echo "Project formatted."
