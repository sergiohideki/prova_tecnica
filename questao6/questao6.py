import argparse
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options

# Configurar o Chrome para rodar em modo "headless" (sem interface gráfica)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Rodar o Chrome no modo headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")  # Simular tamanho de tela

# Configuração do WebDriver utilizando o WebDriverManager para gerenciar o ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

"""
    Função responsável por navegar no site e extrair todas as citações e tags de um autor específico.
    Além disso, extrai informações da página "About" do autor na primeira citação encontrada.

    Parâmetros:
        nome_autor (str): Nome do autor cujas citações serão extraídas.

    Retorna:
        citacoes (list): Lista contendo as citações e tags do autor.
        info_autor (dict): Dicionário contendo as informações do autor (nome, data de nascimento, local e descrição).
"""
def extrair_citacoes_e_tags(nome_autor):
   
    url = "http://quotes.toscrape.com/"
    driver.get(url)

    citacoes = []
    about_extracted = False  # Flag para garantir que o "About" do autor seja extraído apenas uma vez
    info_autor = {}

    while True:
        # Buscar todas as citações na página atual
        citacoes_elementos = driver.find_elements(By.CSS_SELECTOR, '.quote')

        for citacao_elemento in citacoes_elementos:
            autor = citacao_elemento.find_element(By.CSS_SELECTOR, '.author').text
            if autor == nome_autor:
                # Extrair a citação e as tags associadas
                texto_citacao = citacao_elemento.find_element(By.CSS_SELECTOR, '.text').text
                tags = [tag.text for tag in citacao_elemento.find_elements(By.CSS_SELECTOR, '.tags .tag')]
                citacoes.append({'texto': texto_citacao, 'tags': tags})

                # Extrair informações do autor (apenas na primeira citação encontrada)
                if not about_extracted:
                    try:
                        # Clicar no link "About" do autor
                        autor_link = citacao_elemento.find_element(By.XPATH, ".//following-sibling::span/a")
                        autor_link.click()

                        # Preencher as informações do autor
                        info_autor['name'] = nome_autor
                        try:
                            info_autor['birth_date'] = driver.find_element(By.CSS_SELECTOR, '.author-born-date').text
                            info_autor['birth_location'] = driver.find_element(By.CSS_SELECTOR, '.author-born-location').text
                        except:
                            info_autor['birth_date'] = "Data de nascimento não disponível"
                            info_autor['birth_location'] = "Local de nascimento não disponível"

                        info_autor['description'] = driver.find_element(By.CSS_SELECTOR, '.author-description').text

                        print(f"Informações sobre {nome_autor} extraídas.")
                        about_extracted = True  # Garantir que não extrairemos o "About" novamente

                        # Voltar para a página de citações
                        driver.back()
                        time.sleep(2)

                    except Exception as e:
                        print(f"Erro ao clicar no 'About' de {nome_autor}: {e}")
        
        # Verificar se há uma página seguinte, caso contrário, encerrar o loop
        try:
            proxima_pagina = driver.find_element(By.CSS_SELECTOR, '.next a')
            proxima_pagina.click()
            time.sleep(2)
        except:
            break  # Se não houver mais páginas, sair do loop

    return citacoes, info_autor

"""
    Função que salva as citações e as informações do autor em um arquivo JSON.

    Parâmetros:
        citacoes (list): Lista de citações extraídas.
        info_autor (dict): Dicionário com as informações do autor.
"""
def salvar_citacoes_em_json(citacoes, info_autor):

    nome_arquivo = 'citacoes.json'
    dados = {
        'author': {
            'name': info_autor.get('name', 'Nome não disponível'),
            'birth_date': info_autor.get('birth_date', 'Data de nascimento não disponível'),
            'birth_location': info_autor.get('birth_location', 'Local de nascimento não disponível'),
            'description': info_autor.get('description', 'Descrição não disponível')
        },
        'citacoes': citacoes
    }

    # Salvar dados no arquivo JSON
    with open(nome_arquivo, 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)
    
    print(f"Citações e informações sobre o autor salvas no arquivo: {nome_arquivo}")


"""
Função principal que captura os argumentos da linha de comando e chama as funções
para extrair citações e salvar as informações em um arquivo JSON.
"""
def main():

    parser = argparse.ArgumentParser(description='Extrair citações e informações do autor.')
    parser.add_argument('nome_autor', type=str, help='Nome do autor para extrair citações e informações')

    args = parser.parse_args()
    nome_autor = args.nome_autor

    # Extrair citações e informações do autor
    citacoes, info_autor = extrair_citacoes_e_tags(nome_autor)

    # Salvar as citações e as informações do autor em um arquivo JSON
    salvar_citacoes_em_json(citacoes, info_autor)

    # Fechar o WebDriver
    driver.quit()

if __name__ == '__main__':
    main()
