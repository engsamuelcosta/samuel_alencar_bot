import os
from gtts import gTTS

def speak(text: str) -> str:
    """
    Converte texto em fala usando o Google TTS (Grátis e Ilimitado).
    """
    if not text:
        return ""

    try:
        # Gera o áudio com sotaque brasileiro
        tts = gTTS(text=text, lang='pt', tld='com.br')
        
        filename = "reply.mp3"
        
        # Salva o arquivo temporariamente
        tts.save(filename)
        
        return filename
    except Exception as e:
        print(f"❌ Erro ao gerar áudio com gTTS: {e}")
        return ""