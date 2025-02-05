from instace_gmini import genai, MODULE_GEMINI
setting_model = {
    'temperature': 0.1,
    'top_p': 1,
    'top_k': 2,
    'max_output_tokens':8192,
    'response_mime_type': 'application/json'
}



prompt_system = 'Liste apanas os nomes dos produtos e ofereça uma brave descrição.';

llm = genai.GenerativeModel(
    model_name=MODULE_GEMINI,
    system_instruction=prompt_system,
    generation_config=setting_model
    )
ask = "liste três produtos de moda sustentável para ir ao shopping.";
answer = llm.generate_content(ask);

print(f'Resposta: \n {answer.text}');
