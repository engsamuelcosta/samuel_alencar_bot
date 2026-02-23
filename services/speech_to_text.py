import os
import base64
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Inicialização do cliente (considerando o novo SDK instalado via pip install google-genai)
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
client = genai.Client(api_key=api_key)

def transcribe(audio_path: str) -> str:
    """
    Usa o Gemini 1.5 Flash para transcrever áudio .ogg do Telegram. 
    """
    if not api_key:
        return "Erro: GOOGLE_GENAI_API_KEY não configurada."

    try:
        # 1. Leitura binária do arquivo
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        # 2. Chamada ao Gemini 1.5 Flash
        # O modelo Flash é excelente para áudio curto e é muito rápido
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                "Transcreva este áudio do Telegram exatamente como dito, em português do Brasil. "
                "Retorne apenas o texto transcrito, sem comentários adicionais.",
                {"mime_type": "audio/ogg", "data": audio_bytes}
            ]
        )

        # 3. Validação da resposta
        if response and response.text:
            transcription = response.text.strip()
            return transcription if transcription else "Áudio sem conteúdo de fala detectado."
        
        return "Não foi possível extrair texto do áudio."

    except Exception as e:
        print(f"❌ Erro crítico na transcrição (Gemini): {e}")
        return f"Erro ao processar sua mensagem de voz: {str(e)}"