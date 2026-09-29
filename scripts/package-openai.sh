#!/usr/bin/env bash
# Builds the ZIP for OpenAI's plugin portal (platform.openai.com/plugins, "With MCP").
# The archive holds the plugin folder with only its Codex manifest, so the portal
# never has to choose between the Claude and Codex manifests.
set -euo pipefail
cd "$(dirname "$0")/.."
version=$(python3 -c 'import json; print(json.load(open("plugins/revelica/.codex-plugin/plugin.json"))["version"])')
out="dist/revelica-openai-$version.zip"
mkdir -p dist
rm -f "$out"
(cd plugins && zip -rqX "../$out" revelica -x 'revelica/.claude-plugin/*' '*.DS_Store')
unzip -l "$out"
