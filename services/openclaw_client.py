import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Usando o novo SDK 'google-genai'
client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

def send_command(command: str) -> str:
    try:
        # Configurado para o modelo atual gratuito
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=command
        )
        
        if response.text:
            return response.text
        return "IA retornou vazio."

    except Exception as exc:
        print(f"Erro Gemini: {exc}")
        return f"CONNECT_CHALLENGE - {str(exc)}"