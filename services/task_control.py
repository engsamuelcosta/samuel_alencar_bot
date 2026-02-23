from datetime import datetime, timedelta


def build_control_item(task: str, responsavel: str, status: str, prazo_horas: int = 24, observacao: str = "") -> dict:
    now = datetime.now()
    prazo = now + timedelta(hours=prazo_horas)
    return {
        "tarefa": task.strip(),
        "responsavel": responsavel,
        "status": status,
        "prazo": prazo.strftime("%d/%m/%Y %H:%M"),
        "observacao": observacao or "-",
    }


def render_control_board(items: list[dict], feito: str) -> str:
    lines = [
        "\n[Controle do Gerente]",
        "Tarefa | Responsável | Status | Prazo | Observação",
        "--- | --- | --- | --- | ---",
    ]

    for i in items:
        lines.append(
            f"{i['tarefa']} | {i['responsavel']} | {i['status']} | {i['prazo']} | {i['observacao']}"
        )

    lines.append("\nO que foi feito:")
    lines.append(feito.strip() or "-")
    return "\n".join(lines)
