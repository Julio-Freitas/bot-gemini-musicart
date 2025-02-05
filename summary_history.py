import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

KEY_GEMINI_GOOLE = os.getenv("GEMINI_API_KEY")
MODEL_GEMINI = "gemini-1.5-flash"
genai.configure(api_key=KEY_GEMINI_GOOLE)


def summary_history(history):
    """
    Resumir o histórico de mensagens para manter a relevância e a coerência.
    Este método é chamado quando o histórico atinge 10 mensagens.
    """
    full_text = ""

    for msg in history:
        if isinstance(msg, str) and "parts" in msg:
            for part in msg["parts"]:
                full_text += part.text if hasattr(part, "text") else str(part) + " "

    prompt_summary = f"""
        Resuma o seguinte histórico mantendo as informações essenciais para continuar uma conversa coerente:
        {full_text}
    """

    llm = genai.GenerativeModel(
        model_name=MODEL_GEMINI,
        system_instruction="Você é um assistente de resumo.",
        generation_config={"temperature": 0.5, "max_output_tokens": 512},
    )

    response = llm.generate_content(prompt_summary)
    summary = response.text.strip() if response.text else ""

    return [{"role": "model", "parts": [summary]}]
