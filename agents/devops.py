from services.openclaw_client import send_command


def _local_fallback(task: str) -> str:
    return (
        "DevOps (modo local):\n"
        f"Plano para: {task}\n"
        "1) preparar variáveis de ambiente\n"
        "2) gerar build\n"
        "3) deploy controlado\n"
        "4) validação pós-deploy\n"
        "5) rollback pronto\n"
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
