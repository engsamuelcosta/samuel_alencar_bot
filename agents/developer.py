from services.openclaw_client import send_command


def _local_fallback(task: str) -> str:
    return (
        "Developer (modo local - sem execução real):\n"
        f"Solicitação: {task}\n"
        "Resultado: NÃO EXECUTADO — falha de conexão/autenticação com OpenClaw local.\n"
        "Ação necessária: corrigir integração com OpenClaw antes de reportar como concluído."
    )


def run(task: str) -> str:
    command = f"""
Entre no projeto em C:/dev/grupo-vsa.
Analise o código e trabalhe em apenas UMA feature por vez.
Regra obrigatória: responda SEMPRE em português do Brasil (pt-BR), sem inglês.
Responda em português com:
- análise técnica
- plano de implementação
- execução proposta
- riscos

Tarefa: {task}
"""
    result = send_command(command)

    if any(x in result for x in ["CONNECT_CHALLENGE", "Falha ao conectar", "OPENCLAW_UNAUTH"]):
        return _local_fallback(task)

    return f"Developer:\n{result}"
