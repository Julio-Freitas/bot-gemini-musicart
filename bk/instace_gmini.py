import os;
import google.generativeai as genai
from dotenv import load_dotenv;

load_dotenv();

API_KEY_GOOGLE = os.getenv('GEMINI_API_KEY');
MODULE_GEMINI = 'gemini-1.5-flash';

genai.configure(api_key=API_KEY_GOOGLE);
