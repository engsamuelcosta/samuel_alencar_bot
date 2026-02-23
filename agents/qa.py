from services.openclaw_client import send_command


def _local_fallback(task: str) -> str:
    return (
        "Engenheiro de Testes (modo local - sem execução real):\n"
        f"Solicitação: {task}\n"
        "Resultado dos testes: NÃO EXECUTADO — falha de conexão/autenticação com OpenClaw local.\n"
        "Veredicto: REPROVADO (não há evidência de execução)."
    )


def run(task: str) -> str:
    command = f"""
Atue como Engenheiro de Testes.
Monte checklist de validação para a solicitação abaixo,
com casos felizes, casos de borda e critérios de aprovação.
Regra obrigatória: responda SEMPRE em português do Brasil (pt-BR), sem inglês.
Responda em português e de forma prática.

Solicitação: {task}
"""
    result = send_command(command)

    if any(x in result for x in ["CONNECT_CHALLENGE", "Falha ao conectar", "OPENCLAW_UNAUTH"]):
        return _local_fallback(task)

    return f"Engenheiro de Testes:\n{result}"
