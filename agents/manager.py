from services.openclaw_client import send_command


def _local_fallback(task: str) -> str:
    return (
        "Manager (modo local):\n"
        f"ANÁLISE: recebi sua solicitação: {task}\n"
        "PLANO: dividir em etapas curtas, validar resultado a cada etapa e registrar decisões.\n"
        "EXECUÇÃO: começar pelo primeiro bloco prático agora.\n"
        "AUTOMAÇÃO: transformar tarefas repetitivas em rotinas padronizadas.\n"
        "ESCALA: documentar para reutilizar em outros projetos.\n"
        "PRÓXIMO PASSO: me diga o objetivo imediato e eu te devolvo a ação pronta."
    )


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

    if any(x in result for x in ["CONNECT_CHALLENGE", "Falha ao conectar", "OPENCLAW_UNAUTH"]):
        return _local_fallback(task)

    return f"Manager:\n{result}"
