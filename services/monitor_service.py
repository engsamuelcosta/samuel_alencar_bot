import os
import shutil
from datetime import datetime

from services.cronjob_client import summarize_jobs

try:
    import psutil  # type: ignore
except Exception:
    psutil = None


def _mem_snapshot() -> tuple[str, str]:
    if psutil:
        vm = psutil.virtual_memory()
        return (f"{vm.percent:.1f}%", f"{vm.available / (1024**3):.2f} GB livre")
    return ("n/d (instale psutil)", "n/d")


def _cpu_snapshot() -> str:
    if psutil:
        return f"{psutil.cpu_percent(interval=0.3):.1f}%"
    return "n/d (instale psutil)"


def _disk_snapshot() -> str:
    total, used, free = shutil.disk_usage("C:\\")
    used_pct = (used / total) * 100 if total else 0
    return f"{used_pct:.1f}% usado | livre {(free / (1024**3)):.2f} GB"


def _app_snapshot() -> str:
    checks = [
        ("TELEGRAM_TOKEN", bool(os.getenv("TELEGRAM_TOKEN"))),
        ("OPENAI_API_KEY", bool(os.getenv("OPENAI_API_KEY"))),
        ("GOOGLE_GENAI_API_KEY", bool(os.getenv("GOOGLE_GENAI_API_KEY"))),
        ("CRONJOB_API_KEY", bool(os.getenv("CRONJOB_API_KEY"))),
    ]
    return " | ".join(f"{name}={'ok' if ok else 'faltando'}" for name, ok in checks)


def monitoring_report() -> str:
    mem_pct, mem_free = _mem_snapshot()
    report = [
        "[Monitoramento]",
        f"Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"CPU: {_cpu_snapshot()}",
        f"Memória: {mem_pct} | {mem_free}",
        f"Disco C: {_disk_snapshot()}",
        f"Saúde de configuração: {_app_snapshot()}",
        summarize_jobs(),
    ]
    return "\n".join(report)
