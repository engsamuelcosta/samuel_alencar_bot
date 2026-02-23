from services.openclaw_client import send_command


def _local_fallback(task: str) -> str:
    return (
        "DevOps (modo local - sem execução real):\n"
        f"Solicitação: {task}\n"
        "Resultado: NÃO EXECUTADO — falha de conexão/autenticação com OpenClaw local.\n"
        "Deploy: BLOQUEADO até restabelecer integração.\n"
    )


def run(task: str) -> str:
    command = f"""
Atue como DevOps Engineer.
Crie um plano de deploy seguro com rollback e validação pós-deploy.
Inclua variáveis de ambiente e verificações de observabilidade.
Regra obrigatória: responda SEMPRE em português do Brasil (pt-BR), sem inglês.

Solicitação: {task}
"""
    result = send_command(command)

    if any(x in result for x in ["CONNECT_CHALLENGE", "Falha ao conectar", "OPENCLAW_UNAUTH"]):
        return _local_fallback(task)

    return f"DevOps:\n{result}"
