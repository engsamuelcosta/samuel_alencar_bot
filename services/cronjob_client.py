import json
import os
from urllib import request, error

from config import CRONJOB_API_KEY, CRONJOB_API_BASE


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {CRONJOB_API_KEY}",
        "Content-Type": "application/json",
    }


def _get(path: str) -> dict:
    req = request.Request(f"{CRONJOB_API_BASE}{path}", headers=_headers(), method="GET")
    with request.urlopen(req, timeout=15) as resp:
        payload = resp.read().decode("utf-8")
        return json.loads(payload)


def list_jobs() -> dict:
    if not CRONJOB_API_KEY:
        return {"ok": False, "error": "CRONJOB_API_KEY ausente no .env"}

    try:
        data = _get("/jobs")
        jobs = data.get("jobs", [])
        return {"ok": True, "jobs": jobs, "someFailed": data.get("someFailed", False)}
    except error.HTTPError as http_err:
        return {"ok": False, "error": f"HTTP {http_err.code} ao consultar cron-job.org"}
    except Exception as exc:
        return {"ok": False, "error": f"Falha ao consultar cron-job.org: {exc}"}


def summarize_jobs(max_items: int = 5) -> str:
    result = list_jobs()
    if not result.get("ok"):
        return f"cron-job.org: {result.get('error')}"

    jobs = result.get("jobs", [])[:max_items]
    if not jobs:
        return "cron-job.org: nenhum job encontrado."

    lines = ["cron-job.org (resumo):"]
    for job in jobs:
        title = job.get("title", "(sem título)")
        enabled = "on" if job.get("enabled") else "off"
        last_status = job.get("lastStatus", 0)
        next_exec = job.get("nextExecution", 0)
        lines.append(f"- {title} | enabled={enabled} | lastStatus={last_status} | next={next_exec}")

    return "\n".join(lines)
