def load(file_name: str):
    try:
        with open(file_name, "rb") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")


def save(file_name, content):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Error ao salvar arquivo: {e}")
