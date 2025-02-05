import os;
import google.generativeai as genai
from dotenv import load_dotenv;

load_dotenv();

API_KEY_GOOGLE = os.getenv('GEMINI_API_KEY');
MODULE_GEMINI = 'gemini-1.5-flash';

MODULE_GEMINI_PRO="gemini-1.5-pro";
MODULE_GEMINI_FLASH = 'gemini-1.5-flash';

cost_input_flash = 0.075;
cost_output_flash = 0.3;


cost_input_pro = 3.5;
cost_output_pro = 10.50;

genai.configure(api_key=API_KEY_GOOGLE);
modele_flash = genai.get_model(f"models/{MODULE_GEMINI_FLASH}")



limits_moudle_flash = {
    'tokens_input': modele_flash.input_token_limit,
    'tokens_output':modele_flash.output_token_limit,
}


print(f'Limites de modelos FLAHS:\n {limits_moudle_flash}');


llm_flash = genai.GenerativeModel(f'models/{MODULE_GEMINI_FLASH}');
qtd_tokens = llm_flash.count_tokens('O que é uma calça de shopping?');

print(f'qtd: {qtd_tokens}')
