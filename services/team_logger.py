import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def log_team(agent: str, stage: str, detail: str = "") -> None:
    msg = f"[{agent}] {stage}"
    if detail:
        msg += f" | {detail}"
    logging.info(msg)
