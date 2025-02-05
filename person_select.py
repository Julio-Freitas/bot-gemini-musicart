import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
from hellṕer import load

KEY_GEMINI_GOOLE = os.getenv("GEMINI_API_KEY")
MODEL_GEMINI = "gemini-1.5-flash"
genai.configure(api_key=KEY_GEMINI_GOOLE)

positive = load("dados/positive.text")
neutro = load("dados/neutro.text")
negative = load("dados/negative.text")

persons = {"positivo": f"{positive}", "neutro": f"{neutro}", "negativo": f"{negative}"}


def select_person(msg: str):
    prompt_system = f"""
        Assuma que você é um analisador de sentimentos de mensagem.

        1. Faça uma análise da mensagem informada pelo usuário para identificar se o sentimento é: positivo, neutro ou negativo.
        2. Retorne apenas um dos três tipos de sentimentos informados como resposta.

        Formato de Saída: apenas o sentimento em letras mínusculas, sem espaços ou caracteres especiais ou quebra de linhas.

        # Exemplos

        Se a mensagem for: "Eu amo o MusiMart! Vocês são incríveis! 😍♻️"
        Saída: positivo

        Se a mensagem for: "Gostaria de saber mais sobre o horário de funcionamento da loja."
        Saída: neutro

        se a mensagem for: "Estou muito chateado com o atendimento que recebi. 😔"
        Saída: negativo
        """

    setting_module = {"temperature": 0.1, "max_output_tokens": 8192}
    llm = genai.GenerativeModel(
        model_name=MODEL_GEMINI,
        system_instruction=prompt_system,
        generation_config=setting_module,
    )
    reponse = llm.generate_content(msg)
    return reponse.text.strip().lower()
