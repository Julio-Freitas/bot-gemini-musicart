import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from hellṕer import load
from person_select import persons, select_person
from custom_history import destroy_old_history
from summary_history import summary_history
from generate_image import generation_img
import config

load_dotenv()
KEY_GEMINI_GOOLE = os.getenv("GEMINI_API_KEY")
MODEL_GEMINI = "gemini-1.5-flash"
context = load("dados/musicmart.text")

genai.configure(api_key=KEY_GEMINI_GOOLE)


def create_bot():
    person = "neutro"
    prompt_system = f"""
        # PERSONA

        Você é um chatbot de atendimento a clientes de um e-commerce.
        Você não deve responder perguntas que não sejam sobre os dados do e-commerce informado!

        Utilizar somente as informações que estejam dentro do 'contexto'.

        Você deve utilizar técnicas de linguagem natural para tornar as respostas mais naturais e envolventes.

        # CONTEXTO
        {context}

        # PERSONALIDADE
        {person}

        # HISTÓRICO

        Acessar sempre o histórico de mensagens e recuperar informações mencionadas anteriormente, garantindo continuidade e coerência no atendimento.

        """

    setting_module = {"temperature": 0.1, "max_output_tokens": 8192}

    llm = genai.GenerativeModel(
        model_name=MODEL_GEMINI,
        system_instruction=prompt_system,
        generation_config=setting_module,
    )

    chatbot = llm.start_chat(history=[])
    return chatbot


chatbot = create_bot()


def bot(prompt: str):
    max_retry = 1
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

            if config.path_img:
                msg_user += "\n Utilize as caracteristicas da imagem em sua resposta"
                file_image = generation_img(config.path_img)
                response = chatbot.send_message([file_image, msg_user])
                os.remove(config.path_img)
                config.path_img = None
            else:
                response = chatbot.send_message(msg_user)

            prompt = "Olá, posso ajudar em algo?"
            chatbot.history.append({"role": "user", "parts": [prompt]})
            if len(chatbot.history) > 4:
                chatbot.history = summary_history(chatbot.history)

            resposta = chatbot.send_message(prompt)
            chatbot.history.append({"role": "model", "parts": [resposta.text]})

            return response.text

        except Exception as erro:
            retry += 1
            if retry >= max_retry:
                return "Error no Gemini: %s" % erro

            if config.path_img:
                os.remove(config.path_img)
                config.path_img = None
            sleep(50)
