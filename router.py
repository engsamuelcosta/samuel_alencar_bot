def route_agent(text: str) -> str:
    normalized = (text or "").lower().strip()

    # Modo atual: concentrado no Manager.
    # Ele delega internamente para Developer + QA + DevOps
    # e devolve um único relatório consolidado.
    if normalized.startswith("/developer"):
        return "developer"
    if normalized.startswith("/qa"):
        return "qa"
    if normalized.startswith("/devops"):
        return "devops"

    return "manager"
