import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as chaves do .env
load_dotenv()

# Configuração do Google Gemini
API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
genai.configure(api_key=API_KEY)

# Usamos o modelo Flash por ser gratuito e extremamente rápido
model = genai.GenerativeModel('gemini-1.5-flash')

def send_command(command: str) -> str:
    """
    Envia o comando diretamente para a API do Gemini.
    Substitui a conexão WebSocket local para evitar erros de autenticação.
    """
    if not API_KEY:
        return "Erro: GOOGLE_GENAI_API_KEY não encontrada no arquivo .env"

    try:
        # Chamada direta à API
        response = model.generate_content(command)
        
        if response and response.text:
            return response.text
        
        return "A IA retornou uma resposta vazia. Verifique o prompt ou os limites da conta."

    except Exception as exc:
        # Em caso de erro (rede, chave expirada, etc), retornamos 
        # a string que seus agentes já tratam no fallback.
        print(f"Erro na integração direta com Gemini: {exc}")
        return f"CONNECT_CHALLENGE - Erro na API: {str(exc)}"

# Função auxiliar para manter compatibilidade se necessário
def _safe_parse(payload: str) -> str:
    return payload