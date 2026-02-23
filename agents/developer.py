from services.openclaw_client import send_command


def run(task: str) -> str:
    command = f"""
Entre no projeto em C:/dev/grupo-vsa.
Analise o código e trabalhe em apenas UMA feature por vez.
Responda em português com:
- análise técnica
- plano de implementação
- execução proposta
- riscos

Tarefa: {task}
"""
    result = send_command(command)
    return f"Developer:\n{result}"
