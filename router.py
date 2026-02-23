KEYWORDS = {
    "devops": ["deploy", "publicar", "infra", "docker", "cloud run", "ci", "cd", "pipeline"],
    "qa": ["teste", "testar", "bug", "erro", "validar", "homolog", "regress"],
    "developer": ["produto", "cliente", "feature", "funcionalidade", "api", "backend", "frontend", "refator"],
}


def route_agent(text: str) -> str:
    normalized = (text or "").lower()

    for agent, words in KEYWORDS.items():
        if any(word in normalized for word in words):
            return agent

    return "manager"
