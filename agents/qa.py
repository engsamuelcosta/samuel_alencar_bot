from services.openclaw_client import send_command


def run(task: str) -> str:
    command = f"""
Atue como QA Engineer.
Monte checklist de validação para a solicitação abaixo,
com casos felizes, casos de borda e critérios de aprovação.
Regra obrigatória: responda SEMPRE em português do Brasil (pt-BR), sem inglês.
Responda em português e de forma prática.

Solicitação: {task}
"""
    result = send_command(command)
    return f"QA:\n{result}"
