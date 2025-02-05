import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from hellṕer import load, save
from person_select import persons, select_person
load_dotenv()


KEY_GEMINI_GOOLE = os.getenv("GEMINI_API_KEY")
MODEL_GEMINI = "gemini-1.5-flash"
context = load('dados/musicmart.text')

genai.configure(api_key=KEY_GEMINI_GOOLE)

def create_bot():
    person = 'neutro'
    prompt_system = f"""
        # PERSONA

        Você é um chatbot de atendimento a clientes de um e-commerce.
        Você não deve responder perguntas que não sejam dados do ecommerce informado!

        Utilizar somente os dados que estejam dentro do 'contexto'

        Você deve ultilizar tecnicar de

        # CONTEXTO
        {context}

        # PERSONALIDADE
        {person}

        # Histórico
        Acesso sempre o histórico de menssagens, e recupe informações ditas anteriomente.
        """
    setting_module = {
        "temperature" : 0.1,
        "max_output_tokens" : 8192
    }

    llm = genai.GenerativeModel(
        model_name=MODEL_GEMINI,
        system_instruction=prompt_system,
        generation_config=setting_module,
    )

    chatbot = llm.start_chat(history=[])
    return chatbot

chatbot = create_bot()

def bot(prompt:str):
    max_retry= 1
    retry: 0
    while True:
        try:
            person = persons[select_person(prompt)]
            msg_user = f"""
                            Considerar esta personalidade para responder a mensagem:
                            {person}

                            Respona a seguinte mensagem sempre lembrando o hitórico da conversa
                            {prompt}
                        """
            response = chatbot.send_message(msg_user)
            return response.text

        except Exception as erro:
            retry += 1
            if retry >= max_retry:
             return "Error no Gemini: %s" % erro

            sleep(50)
