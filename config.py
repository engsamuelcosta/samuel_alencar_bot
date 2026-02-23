import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") # Adicione esta linha
CRONJOB_API_KEY = os.getenv("CRONJOB_API_KEY")
CRONJOB_API_BASE = os.getenv("CRONJOB_API_BASE", "https://api.cron-job.org")

# Estratégia de provedores:
# 1) PRIMARY_AI_PROVIDER=codex_local (sem API)
# 2) BACKUP_AI_PROVIDER=google_genai (usa API apenas no fallback)
PRIMARY_AI_PROVIDER = os.getenv("PRIMARY_AI_PROVIDER", "google_genai")
BACKUP_AI_PROVIDER = os.getenv("BACKUP_AI_PROVIDER", "google_genai")
ALLOW_BACKUP_API = os.getenv("ALLOW_BACKUP_API", "false").lower() == "true"
