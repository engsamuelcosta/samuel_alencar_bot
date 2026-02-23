import json
from typing import Any

import websocket

OPENCLAW_WS = "ws://127.0.0.1:18789"


def _safe_parse(payload: str) -> str:
    try:
        data: Any = json.loads(payload)
        if isinstance(data, dict):
            event = data.get("event")
            if event == "connect.challenge":
                return "CONNECT_CHALLENGE"
            return str(data.get("result") or data.get("message") or data)
        return str(data)
    except Exception:
        return payload


def send_command(command: str) -> str:
    try:
        ws = websocket.create_connection(OPENCLAW_WS, timeout=20)

        payload = {
            "type": "command",
            "command": command,
        }

        ws.send(json.dumps(payload, ensure_ascii=False))
        result = ws.recv()
        ws.close()

        return _safe_parse(result)

    except Exception as exc:
        return (
            "Falha ao conectar no OpenClaw local (ws://127.0.0.1:18789). "
            f"Erro: {exc}"
        )
