from instace_gmini import genai, MODULE_GEMINI
def category_product(name_product: str, list_category_able: str):
    prompt_system = f""""
            você é um categorizador de produtos.
            você deve assumir as categorias presentes na lista abaixo:

            # Lista de categoria válidas.
            {list_category_able.split(',')}

            # Formato de saída:
            Produto: Nome do produto
            Categoria: Apresente a categoria do produto.

            # Exemplo
            Produto: Escova eletrica com recarga solar:
            Categoria: Eletônicos verdes
     """;
    llm = genai.GenerativeModel(
    model_name=MODULE_GEMINI,
    system_instruction=prompt_system,
    )
    answer = llm.generate_content(name_product);
    return answer.text


def main():
    lista_categorias_possiveis = "Eletrônicos Verdes,Moda Sustentável,Produtos de Limpeza Ecológicos,Alimentos Orgânicos,Produtos de Higiene Sustentáveis"
    produto = input('Qual produto quer classificar?\n');

    while produto != "":
        print(f'{category_product(produto,lista_categorias_possiveis)}');
        produto = input("Informe o produto que você deseja classificar: ")

if __name__ == '__main__':
    main()
