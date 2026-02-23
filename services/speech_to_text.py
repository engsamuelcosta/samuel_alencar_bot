import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe(audio_path: str) -> str:
    with open(audio_path, "rb") as audio:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
        )

    return result.text
