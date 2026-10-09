#!/usr/bin/env bash
# Builds the ZIP for OpenAI's plugin portal (platform.openai.com/plugins, "With MCP").
# Export the shared Codex source to the portable OpenAI submission format.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/package-openai.py "$@"
