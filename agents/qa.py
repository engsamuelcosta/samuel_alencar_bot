from services.openclaw_client import send_command


def _local_fallback(task: str) -> str:
    return (
        "QA (modo local):\n"
        f"Checklist para: {task}\n"
        "- Caso feliz\n"
        "- Casos de borda\n"
        "- Validação de erros\n"
        "- Critério de aprovação\n"
        "Se quiser, eu detalho cada item agora."
    )


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

    if any(x in result for x in ["CONNECT_CHALLENGE", "Falha ao conectar", "OPENCLAW_UNAUTH"]):
        return _local_fallback(task)

    return f"QA:\n{result}"
