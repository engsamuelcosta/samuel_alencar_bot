from services.openclaw_client import send_command


def run(task: str) -> str:
    command = f"""
Atue como DevOps Engineer.
Crie um plano de deploy seguro com rollback e validação pós-deploy.
Inclua variáveis de ambiente e verificações de observabilidade.
Regra obrigatória: responda SEMPRE em português do Brasil (pt-BR), sem inglês.

Solicitação: {task}
"""
    result = send_command(command)
    return f"DevOps:\n{result}"
