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
        # 1. Baixa o arquivo de voz do Telegram
        voice_file = await update.message.voice.get_file()
        local_audio_input = "audio.ogg"
        await voice_file.download_to_drive(local_audio_input)

        # 2. Transcreve o áudio (usando sua nova função Gemini)
        text = transcribe(local_audio_input)
        
        # 3. Roteamento e Log
        agent = route_agent(text)
        log_team("Sistema", "áudio transcrito", f"roteado_para={agent}")
        
        # 4. Execução da lógica e normalização da resposta
        raw_response = execute(agent, text)
        response = normalize_response(raw_response)
        
        log_team("Sistema", "resposta gerada para voz", f"agente={agent}")

        # 5. Gera a voz de resposta (usando gTTS grátis)
        audio_output_path = speak(response)

        # 6. Envio do áudio de volta ao usuário
        if audio_output_path and os.path.exists(audio_output_path):
            with open(audio_output_path, "rb") as audio_file:
                await update.message.reply_voice(voice=audio_file, caption="Aqui está minha resposta:")
        else:
            # Fallback caso a geração do áudio falhe
            await update.message.reply_text(response)

    except Exception as e:
        log_team("Sistema", "Erro crítico no handle_voice", str(e))
        print(f"Erro detalhado: {e}")
        await update.message.reply_text("Desculpe, tive um problema ao processar sua mensagem de voz.")
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