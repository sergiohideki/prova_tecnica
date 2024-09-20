import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math


cnpj = '04.502.445/0001-20'
senha = '85243140'

lista_produtos = []

# Configuração do WebDriver utilizando o WebDriverManager para gerenciar o ChromeDriver
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)

# Acessar a página inicial
url_home = 'https://www.compra-agora.com'
navegador.get(url_home)

# Maximize a janela do navegador
navegador.maximize_window()

# Aguardar a página carregar completamente
time.sleep(10)

# Localizar e clicar no botão de login
botao_login = navegador.find_element(By.ID, 'login-text')
botao_login.click()

# Aguardar o modal abrir completamente
time.sleep(2)

# Preencher os campos de CNPJ e senha
campo_cnpj = navegador.find_element(By.ID, 'usuarioCnpj')
campo_cnpj.send_keys(cnpj)

time.sleep(2)

campo_senha = navegador.find_element(By.ID, 'usuarioSenhaCA')
campo_senha.send_keys(senha)

#fazer o CAPTCHA manualmente
time.sleep(15)

# Clicar no botão de login
botao_entrar = navegador.find_element(By.ID, 'realizar-login')  
botao_entrar.click()

time.sleep(5)

# Aguardar até que o botão esteja clicável
WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'menu-text')))
botao_categoria = navegador.find_element(By.CLASS_NAME, 'menu-text')
botao_categoria.click()


time.sleep(4)

# Localizar todos os itens de menu pela classe ou outro seletor
menu_itens = navegador.find_elements(By.CLASS_NAME, 'lista-menu-itens')

# Iterar sobre todos os itens do menu e clicar
for item_menu_index in range(len(menu_itens)):
    # Recarregar os itens de menu a cada iteração para evitar StaleElementReferenceException
    menu_itens = navegador.find_elements(By.CLASS_NAME, 'lista-menu-itens')

    # Aguardar até que o item esteja visível e clicável
    time.sleep(1)

    # Tentar clicar no item do menu
    try:
        menu_itens[item_menu_index].click()
    except Exception as e:
        print(f"Erro ao clicar no item do menu: {e}")
        continue

    # Aguardar um pouco após o clique
    time.sleep(10)

    # Tentar localizar o número total de produtos
    try:
        qtd_produtos_element = navegador.find_element(By.CLASS_NAME, 'qtd-produtos')
        qtd_produtos_texto = qtd_produtos_element.text.strip()  # Ex: "731 produtos"
        qtd_produtos = int(qtd_produtos_texto.split()[0])  # Extrai o número de produtos (ex: "731")

        # Verificar se não há produtos na categoria, e passar para a próxima
        if qtd_produtos == 0:
            print("Categoria vazia, passando para a próxima.")
            continue

        # Calcular o número de páginas necessárias
        produtos_por_pagina = 24
        paginas_totais = math.ceil(qtd_produtos / produtos_por_pagina)

        print(f"Número total de produtos: {qtd_produtos}")
        print(f"Será necessário carregar {paginas_totais} páginas.")

        # Continuar clicando no botão "Ver mais produtos" até carregar todas as páginas
        while True:
            try:
                # Localizar a div "DadosPaginacao" e extrair o valor de data-p (página atual)
                dados_paginacao = navegador.find_element(By.ID, 'DadosPaginacao')
                pagina_atual = int(dados_paginacao.get_attribute('data-p'))

                print(f"Página atual: {pagina_atual} de {paginas_totais}")

                # Continuar clicando enquanto a página atual for menor que o total de páginas
                while pagina_atual < paginas_totais:
                    try:
                        # Localizar o botão "Ver mais produtos" e rolar até ele
                        ver_mais_botao = WebDriverWait(navegador, 10).until(
                            EC.element_to_be_clickable((By.ID, 'btnCarregarMais'))
                        )

                        # Rolando a página até o botão "Ver mais produtos" ficar no meio da tela
                        navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", ver_mais_botao)

                        # Clicar no botão "Ver mais produtos"
                        ver_mais_botao.click()
                        print("Clicou no botão 'Ver mais produtos'.")

                        # Aguardar o carregamento de novos produtos
                        time.sleep(5)

                        # Atualizar o valor da página atual após o clique
                        dados_paginacao = navegador.find_element(By.ID, 'DadosPaginacao')
                        pagina_atual = int(dados_paginacao.get_attribute('data-p'))

                    except Exception as e:
                        print(f"Erro ao clicar no botão 'Ver mais produtos': {e}")
                        break

                # Verificar se todas as páginas foram carregadas
                if pagina_atual >= paginas_totais:
                    print(f"Todas as {paginas_totais} páginas foram carregadas.")
                    break

            except Exception as e:
                print(f"Erro ao verificar a página atual: {e}")
                break

        # Coletar todos os produtos da página
        produtos = navegador.find_elements(By.CSS_SELECTOR, 'ul.shelf-content-items li')

        # Iterar sobre todos os produtos e extrair as informações
        for produto in produtos:
            try:
                # Extrair o URL da imagem
                imagem = produto.find_element(By.CLASS_NAME, 'img-fluid')
                url_imagem = imagem.get_attribute('src')

                # Extrair o nome do fabricante
                fabricante = produto.find_element(By.XPATH, ".//a[contains(@class, 'produto-marca') and contains(@class, 'mb-1')]")
                nome_fabricante = fabricante.text.strip()

                # Extrair a descrição do produto
                descricao_produto = produto.find_element(By.XPATH, ".//a[contains(@class, 'produto-nome') and contains(@class, 'mb-1')]")
                descricao = descricao_produto.text.strip()

                # Criar um dicionário com os dados do produto
                dados_produto = {
                    'url_imagem': url_imagem,
                    'nome_fabricante': nome_fabricante,
                    'descricao': descricao
                }

                # Adicionar os dados do produto à lista de produtos
                lista_produtos.append(dados_produto)

            except Exception as e:
                print(f"Erro ao processar produto: {e}")

    except Exception as e:
        print(f"Erro ao processar a categoria: {e}")
        continue  # Pular para a próxima categoria se houver erro

    # Voltar ao menu de categorias
    botao_categoria = navegador.find_element(By.CLASS_NAME, 'menu-text')
    botao_categoria.click()

    time.sleep(2)

# Fechar o navegador
navegador.quit()

# Salvar os dados extraídos em um arquivo JSON
with open('produtos.json', 'w', encoding='utf-8') as f:
    json.dump(lista_produtos, f, ensure_ascii=False, indent=4)

print("Dados dos produtos foram salvos no arquivo 'produtos.json'.")
