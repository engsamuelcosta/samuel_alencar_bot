from config import (
    PRIMARY_AI_PROVIDER,
    BACKUP_AI_PROVIDER,
    ALLOW_BACKUP_API,
    GOOGLE_GENAI_API_KEY,
)


def provider_status() -> str:
    backup_ready = bool(GOOGLE_GENAI_API_KEY)
    backup_mode = "habilitado" if ALLOW_BACKUP_API else "desabilitado"
    return (
        f"primary={PRIMARY_AI_PROVIDER}; "
        f"backup={BACKUP_AI_PROVIDER}; "
        f"backup_api={backup_mode}; "
        f"google_key={'ok' if backup_ready else 'ausente'}"
    )


def should_use_backup() -> bool:
    return ALLOW_BACKUP_API and bool(GOOGLE_GENAI_API_KEY)
