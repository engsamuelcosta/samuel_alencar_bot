import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def speak(text: str) -> str:
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )

    filename = "reply.mp3"

    with open(filename, "wb") as f:
        f.write(speech.content)

    return filename
