from services.openclaw_client import send_command


def run(task: str) -> str:
    command = f"""
Atue como QA Engineer.
Monte checklist de validação para a solicitação abaixo,
com casos felizes, edge cases e critérios de aprovação.
Responda em português e de forma prática.

Solicitação: {task}
"""
    result = send_command(command)
    return f"QA:\n{result}"
