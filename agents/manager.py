from agents import developer, qa, devops
from services.provider_selector import provider_status
from services.team_logger import log_team
from services.task_control import build_control_item, render_control_board
from services.monitor_service import monitoring_report


def _section(title: str, content: str) -> str:
    return f"\n[{title}]\n{content.strip()}\n"


def run(task: str) -> str:
    # Gerente centraliza e delega sempre para a equipe.
    log_team("Gerente", "início da iteração", task)

    log_team("Gerente", "delegando", "Developer")
    dev_result = developer.run(task)
    log_team("Developer", "retorno recebido")

    log_team("Gerente", "delegando", "Engenheiro de Testes")
    qa_result = qa.run(task)
    log_team("Engenheiro de Testes", "retorno recebido")

    log_team("Gerente", "delegando", "DevOps")
    devops_result = devops.run(task)
    log_team("DevOps", "retorno recebido")

    dev_local = "modo local" in dev_result.lower()
    qa_local = "modo local" in qa_result.lower()
    devops_local = "modo local" in devops_result.lower()

    controles = [
        build_control_item(
            task,
            "Developer",
            "Bloqueado" if dev_local else "Concluído",
            24,
            "Sem execução real (OpenClaw indisponível)" if dev_local else "Análise/execução técnica retornada",
        ),
        build_control_item(
            task,
            "Engenheiro de Testes",
            "Bloqueado" if qa_local else "Concluído",
            24,
            "Teste não executado (OpenClaw indisponível)" if qa_local else "Checklist e validação retornados",
        ),
        build_control_item(
            task,
            "DevOps",
            "Bloqueado" if devops_local else "Concluído",
            24,
            "Deploy bloqueado (OpenClaw indisponível)" if devops_local else "Plano de deploy/infra retornado",
        ),
    ]

    feito = (
        "1) Delegação para Developer executada.\n"
        "2) Delegação para Engenheiro de Testes executada.\n"
        "3) Delegação para DevOps executada."
    )

    report = "Gerente: delegação concluída com retorno da equipe.\n"
    report += f"Provedores IA: {provider_status()}\n"
    report += render_control_board(controles, feito)
    report += _section("Developer", dev_result)
    report += _section("Engenheiro de Testes", qa_result)
    report += _section("DevOps", devops_result)

    if dev_local or qa_local or devops_local:
        report += (
            "\n[ALERTA]\n"
            "Integração com OpenClaw local falhou (connect.challenge / autenticação). "
            "Os resultados acima em 'modo local' NÃO representam execução real.\n"
        )

    normalized_task = (task or "").lower()
    if any(k in normalized_task for k in ["monitor", "saúde", "saude", "cron", "zabbix"]):
        report += "\n" + monitoring_report() + "\n"

    report += "\nPróximo passo: me diga se você quer que eu priorize correção, teste, deploy ou monitoramento."

    log_team("Gerente", "fim da iteração")
    return report
