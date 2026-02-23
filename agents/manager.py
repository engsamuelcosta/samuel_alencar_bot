from services.openclaw_client import send_command


def run(task: str) -> str:
    command = f"""
Você é o Manager de uma empresa de IA.
Regra obrigatória: responda SEMPRE em português do Brasil (pt-BR), sem inglês.
Analise a solicitação abaixo e devolva um plano objetivo em português com:
1) análise
2) plano
3) próximo passo

Solicitação: {task}
"""
    result = send_command(command)
    return f"Manager:\n{result}"
