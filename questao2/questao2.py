import argparse
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar o Chrome para rodar em modo "headless" (sem interface gráfica)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Rodar o Chrome no modo headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Configuração do WebDriver utilizando o WebDriverManager para gerenciar o ChromeDriver
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=chrome_options)


# Acessar a página inicial do sistema
url_home = 'https://pedidoeletronico.servimed.com.br/'
navegador.get(url_home)

# Configurar o parser de argumentos
parser = argparse.ArgumentParser(description='Processar o número do pedido')
parser.add_argument('pedido', type=str, help='Número do pedido a ser processado')
args = parser.parse_args()

# Credenciais do usuário
usuario = 'juliano@farmaprevonline.com.br'
senha = 'a007299A'
codigo = args.pedido  # Código do pedido a ser processado

# Inicializar a lista de produtos
lista_produtos = []
pedido_encontrado = False  # Inicializar a variável para verificar se o pedido foi encontrado



# Aguardar a página carregar completamente
time.sleep(3)

# Preencher os campos de login (usuário e senha)
campo_usuario = navegador.find_element(By.NAME, 'username')
campo_usuario.send_keys(usuario)

time.sleep(2)

campo_senha = navegador.find_element(By.NAME, 'password')
campo_senha.send_keys(senha)

WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-block.btn-success'))).click()
botao_entrar = navegador.find_element(By.CSS_SELECTOR, 'button.btn.btn-block.btn-success')  
botao_entrar.click()

# Aguardar o login ser concluído
time.sleep(3)


# Acessar a seção de "Meus Pedidos"
botao_pedidos = WebDriverWait(navegador, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.nav-link[aria-haspopup="true"]'))
)
botao_pedidos.click()

time.sleep(1)

# Clicar na opção "Meus Pedidos"
botao_meuspedidos = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.dropdown-item[href="/pedidos"]'))
)
botao_meuspedidos.click()

# Aguardar a página de pedidos carregar
WebDriverWait(navegador, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input.form-control[placeholder="Digite o código do pedido, razão social ou CNPJ"]'))
)

# Preencher o campo do código do pedido
input_codigo = WebDriverWait(navegador, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input.form-control[placeholder="Digite o código do pedido, razão social ou CNPJ"]'))
)
input_codigo.send_keys(codigo)

# Clicar no botão "Pesquisar"
botao_pesquisar = WebDriverWait(navegador, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary'))
)
botao_pesquisar.click()

# Verificar se o botão de descrição (informações do pedido) está presente
try:
    botao_descricao = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-icon'))
    )
    botao_descricao.click()

    # Aguardar o pop-up de informações do pedido ser exibido completamente
    WebDriverWait(navegador, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-body'))
    )

    # Tentar localizar o motivo da rejeição dentro do pop-up
    try:
        motivo_elemento = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Motivo da Rejeição')]/following-sibling::input[@class='form-control'][@disabled]"))
        )
        motivo = motivo_elemento.get_attribute('value').strip()
    except Exception as e:
        motivo = "Motivo não encontrado"
        print(f"Erro ao extrair motivo: {e}")

    # Selecionar a tabela correta dentro do modal/pop-up
    try:
        tabela = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-body table.table'))
        )
        linhas = tabela.find_elements(By.CSS_SELECTOR, 'tbody tr')

        # Iterar sobre as linhas e extrair os dados de cada produto
        for linha in linhas:
            codigo_produto = linha.find_elements(By.TAG_NAME, 'td')[0].text.strip()
            descricao = linha.find_elements(By.TAG_NAME, 'td')[1].text.strip()
            quantidade_faturada = linha.find_elements(By.TAG_NAME, 'td')[7].text.strip()

            # Adicionar o produto à lista
            lista_produtos.append({
                'codigo_produto': codigo_produto,
                'descricao': descricao,
                'quantidade_faturada': quantidade_faturada
            })

        pedido_encontrado = True  # Pedido encontrado com sucesso

    except Exception as e:
        print(f"Erro ao extrair dados da tabela: {e}")
        pedido_encontrado = False

except Exception as e:
    print(f"Erro: Pedido com código {codigo} não encontrado.")
    pedido_encontrado = False

# Verificar se o pedido foi encontrado e salvar os dados no arquivo JSON
if pedido_encontrado:
    # Montar o dicionário final com motivo e produtos
    dados_faturamento = {
        "motivo": motivo,
        "itens": lista_produtos
    }

    # Armazenar os dados extraídos em um arquivo JSON
    with open(f'pedido_{codigo}.json', 'w', encoding='utf-8') as f:
        json.dump(dados_faturamento, f, ensure_ascii=False, indent=4)

    print(f"Dados do pedido {codigo} salvos no arquivo 'pedido_{codigo}.json'.")
else:
    print(f"Erro: Pedido com código {codigo} não encontrado.")

# Fechar o navegador
navegador.quit()