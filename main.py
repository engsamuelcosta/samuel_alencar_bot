import google.generativeai as genai
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from config import TELEGRAM_TOKEN
from router import route_agent

from agents import manager, developer, qa, devops
from services.speech_to_text import transcribe
from services.text_to_speech import speak
from services.team_logger import setup_logging, log_team


fload_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')
try:
    response = model.generate_content("Olá, responda apenas: Conexão OK")
    print(response.text)
except Exception as e:
    print(f"Erro na API: {e}")




def execute(agent: str, text: str) -> str:
    if agent == "developer":
        return developer.run(text)

    if agent == "qa":
        return qa.run(text)

    if agent == "devops":
        return devops.run(text)

    return manager.run(text)


def normalize_response(response: str) -> str:
    content = (response or "").strip()

    if (
        "CONNECT_CHALLENGE" in content
        or "connect.challenge" in content
        or "'type': 'event'" in content
        or '"event":"connect.challenge"' in content
    ):
        return (
            "Ainda não consegui autenticar a conexão com o OpenClaw local. "
            "Mas já recebi sua solicitação e vou seguir em português do Brasil. "
            "Me diga o tema que eu te entrego agora: análise, plano, execução e próximo passo."
        )

    return content or "Não consegui gerar uma resposta agora."


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if not text:
        await update.message.reply_text("Não recebi texto válido.")
        return

    agent = route_agent(text)
    log_team("Sistema", "mensagem recebida", f"roteado_para={agent}")
    response = normalize_response(execute(agent, text))
    log_team("Sistema", "resposta gerada", f"agente={agent}")

    await update.message.reply_text(response)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = await update.message.voice.get_file()
    await voice.download_to_drive("audio.ogg")

    text = transcribe("audio.ogg")
    agent = route_agent(text)
    log_team("Sistema", "áudio transcrito", f"roteado_para={agent}")
    response = normalize_response(execute(agent, text))
    log_team("Sistema", "resposta de voz gerada", f"agente={agent}")

    audio = speak(response)
    await update.message.reply_voice(audio)


def main() -> None:
    setup_logging()

    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN não configurado no .env")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    app.run_polling()


if __name__ == "__main__":
    main()
