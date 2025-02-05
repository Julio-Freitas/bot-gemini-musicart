import os;
import google.generativeai as genai
from dotenv import load_dotenv;

load_dotenv();
API_KEY_GOOGLE = os.getenv('GEMINI_API_KEY');
module_gemini = 'gemini-1.5-flash';

genai.configure(api_key=API_KEY_GOOGLE);

def load_file(path: str):
    try:
        with open(path, 'r') as file:
            data = file.read()
            return data;
    except IOError as error:
        print(f'Erro in load file\n {error}');

prompt_system = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_user = load_file('dados/lista_de_compras_100_clientes.csv');

module_flash = genai.GenerativeModel(f'models/{module_gemini}');
qte = module_flash.count_tokens(prompt_user)

LIMIT_TOKENS = 3000;

if qte.total_tokens >= LIMIT_TOKENS:
   module_gemini = 'gemini-1.5-pro';

print(f'O modelo utilizado é:\n {module_gemini}')


llm = genai.GenerativeModel(
    model_name=module_gemini,
    system_instruction=prompt_system
)

answer = llm.generate_content(prompt_user)

print(f'R: {answer.text}')
