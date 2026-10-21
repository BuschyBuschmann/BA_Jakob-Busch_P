#!/bin/bash
# Richtet in Cloud-Sessions die Python-3.11-Umgebung des Projekts unter software/ ein.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

export PATH="/root/.local/bin:$PATH"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
SOFTWARE_DIR="$PROJECT_DIR/software"

if [ ! -f "$SOFTWARE_DIR/pyproject.toml" ]; then
  exit 0
fi

command -v uv >/dev/null || { echo "session-start: uv nicht gefunden" >&2; exit 1; }

cd "$SOFTWARE_DIR"
uv sync --python 3.11
