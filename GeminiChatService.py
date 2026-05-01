from dotenv import load_dotenv
from google import genai
import os

load_dotenv()


def send_question(question: str, chat_history: list[dict] = None, system_prompt: str = None) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY fehlt in der .env Datei.")

    try:
        client = genai.Client(api_key=api_key)

        if chat_history:
            history_text = "\n".join(
                f"{msg['role'].capitalize()}: {msg['content']}"
                for msg in chat_history
            )
            contents = f"{history_text}\nUser: {question}"
        else:
            contents = question

        config = None
        if system_prompt:
            config = genai.types.GenerateContentConfig(
                system_instruction=system_prompt
            )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )
        return response.text

    except EnvironmentError:
        raise
    except Exception as e:
        raise RuntimeError(f"Gemini API Fehler: {e}") from e
