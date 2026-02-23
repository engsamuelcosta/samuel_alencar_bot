from agents import developer, qa, devops
from services.provider_selector import provider_status
from services.team_logger import log_team


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

    report = "Gerente: delegação concluída com retorno da equipe.\n"
    report += f"Provedores IA: {provider_status()}\n"
    report += _section("Developer", dev_result)
    report += _section("Engenheiro de Testes", qa_result)
    report += _section("DevOps", devops_result)
    report += "\nPróximo passo: me diga se você quer que eu priorize correção, teste ou deploy."

    log_team("Gerente", "fim da iteração")
    return report
