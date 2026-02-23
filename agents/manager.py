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

    controles = [
        build_control_item(task, "Developer", "Concluído", 24, "Análise/execução técnica retornada"),
        build_control_item(task, "Engenheiro de Testes", "Concluído", 24, "Checklist e validação retornados"),
        build_control_item(task, "DevOps", "Concluído", 24, "Plano de deploy/infra retornado"),
    ]

    feito = (
        "1) Delegação para Developer concluída.\n"
        "2) Delegação para Engenheiro de Testes concluída.\n"
        "3) Delegação para DevOps concluída."
    )

    report = "Gerente: delegação concluída com retorno da equipe.\n"
    report += f"Provedores IA: {provider_status()}\n"
    report += render_control_board(controles, feito)
    report += _section("Developer", dev_result)
    report += _section("Engenheiro de Testes", qa_result)
    report += _section("DevOps", devops_result)

    normalized_task = (task or "").lower()
    if any(k in normalized_task for k in ["monitor", "saúde", "saude", "cron", "zabbix"]):
        report += "\n" + monitoring_report() + "\n"

    report += "\nPróximo passo: me diga se você quer que eu priorize correção, teste, deploy ou monitoramento."

    log_team("Gerente", "fim da iteração")
    return report
