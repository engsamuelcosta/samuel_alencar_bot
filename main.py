import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Configurações e Agentes
from config import TELEGRAM_TOKEN
from router import route_agent
from agents import manager, developer, qa, devops
from services.speech_to_text import transcribe
from services.text_to_speech import speak
from services.team_logger import setup_logging, log_team

# 1. Carregamento de ambiente centralizado
load_dotenv()

def execute(agent: str, text: str) -> str:
    """Delega a tarefa para o agente correspondente."""
    if agent == "developer":
        return developer.run(text)
    if agent == "qa":
        return qa.run(text)
    if agent == "devops":
        return devops.run(text)
    
    return manager.run(text)

def normalize_response(response: str) -> str:
    """Trata a resposta e limpa mensagens de erro de infraestrutura."""
    content = (response or "").strip()

    # Se ainda houver resquício de falha de conexão no client
    if any(x in content for x in ["CONNECT_CHALLENGE", "OPENCLAW_UNAUTH", "Falha ao conectar"]):
        return (
            "⚠️ O sistema está operando em modo de contingência.\n\n"
            "Não consegui conectar ao OpenClaw local, mas a API Gemini está ativa. "
            "Por favor, verifique se o serviço local está configurado ou se a chave API no .env está correta."
        )

    return content or "Desculpe, não consegui processar sua solicitação agora."

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if not text:
        await update.message.reply_text("Não recebi um texto válido.")
        return

    agent = route_agent(text)
    log_team("Sistema", "mensagem recebida", f"roteado_para={agent}")
    
    # Executa a lógica dos agentes
    raw_response = execute(agent, text)
    response = normalize_response(raw_response)
    
    log_team("Sistema", "resposta gerada", f"agente={agent}")
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        voice = await update.message.voice.get_file()
        await voice.download_to_drive("audio.ogg")

        text = transcribe("audio.ogg")
        agent = route_agent(text)
        
        log_team("Sistema", "áudio transcrito", f"roteado_para={agent}")
        
        raw_response = execute(agent, text)
        response = normalize_response(raw_response)
        
        log_team("Sistema", "resposta de voz gerada", f"agente={agent}")

        audio_path = speak(response)
        await update.message.reply_voice(audio_path)
    except Exception as e:
        log_team("Sistema", "Erro voz", str(e))
        await update.message.reply_text("Houve um erro ao processar seu áudio.")

def main() -> None:
    setup_logging()

    if not TELEGRAM_TOKEN:
        print("CRITICAL: TELEGRAM_TOKEN não configurado no .env")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("🤖 Bot iniciado e pronto para o trabalho!")
    app.run_polling()

if __name__ == "__main__":
    main()