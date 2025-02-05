import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


KEY_GEMINI_GOOLE = os.getenv("GEMINI_API_KEY")
MODEL_GEMINI = "gemini-1.5-flash"
genai.configure(api_key=KEY_GEMINI_GOOLE)


def generation_img(path):
    temp_file = genai.upload_file(
        path=path, display_name="Imagem Enviada"
    )
    print(f"Imagem Enviada: {temp_file.uri}")

    return temp_file
