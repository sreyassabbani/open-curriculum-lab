#!/bin/sh
set -eu

: "${CANVAS_ACCESS_TOKEN:?Set CANVAS_ACCESS_TOKEN in the host secret manager}"
: "${CONTROL_PLANE_API_KEY:?Set CONTROL_PLANE_API_KEY in the host secret manager}"
: "${OPENAI_TUNNEL_ID:?Set OPENAI_TUNNEL_ID for the private ChatGPT app}"

tunnel-client init --sample sample_mcp_stdio_local --profile math2551 --tunnel-id "$OPENAI_TUNNEL_ID" --mcp-command "mcp run /app/canvas_bridge/server.py --transport stdio"
exec tunnel-client run --profile math2551
