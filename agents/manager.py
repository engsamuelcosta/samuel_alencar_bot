from agents import developer, qa, devops
from services.provider_selector import provider_status


def _section(title: str, content: str) -> str:
    return f"\n[{title}]\n{content.strip()}\n"


def run(task: str) -> str:
    # Gerente centraliza e delega sempre para a equipe.
    dev_result = developer.run(task)
    qa_result = qa.run(task)
    devops_result = devops.run(task)

    report = "Gerente: delegação concluída com retorno da equipe.\n"
    report += f"Provedores IA: {provider_status()}\n"
    report += _section("Developer", dev_result)
    report += _section("Engenheiro de Testes", qa_result)
    report += _section("DevOps", devops_result)
    report += "\nPróximo passo: me diga se você quer que eu priorize correção, teste ou deploy."
    return report
