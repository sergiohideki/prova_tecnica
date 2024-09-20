Execução:

Infelizmente não será possível executar esse código pelo docker, pois ele tem uma verificação de CAPTCHE que eu não consegui
automatizar sendo assim para executar o código você precisará executar no ambiente local para que seja possível você vizualizar
o site e dessa forma fazer o CAPTCHE manualmente.

para isso você precisará instalar as bibliotecas a seguir em sua maquína:

Selenium:
pip install selenium

WebDriver:
pip install WebDriver

após a intalação de ambos em sua máquina basta executar o arquivo questao1.py utilizando o comando:

python questao1.py 

ao executar o código ele vai abrir o site e clicar no login após a abertura do pop-up de login você terá 15 segundos para 
fazer o CAPTCHE manualmente após fazer o CAPTCHE é só esperar que o código fará todo o resto sozinho, ao finalizar o código ele
irá gerar um arquivo JSON chamado produtos.json onde terá todos os dados solicitados de todos os produtos de todas categorias.

ps: o código demora aproximadamente 12 minutos para extrair todas as informações, essa demora é um virtude de uma das categorias
a de cuidados pessoais com mais de 700 produtos onde acaba causando uma grande lentidão no código, inclusive se você achar que a
execução travou na categoria de cuidados pessoais não se preocupe pois quando o codigo chega ao fim ele extrai os dados de todos os 
produtos e como são mais de 700 demora um tempo consideravel é só esperar.

visão tecnica:

Este script utiliza a biblioteca Selenium para automatizar a extração de informações de produtos. 

O código navega pelas categorias de produtos no site, extrai informações relevantes de cada produto e 
salva os dados em um arquivo JSON.

Navegação Automatizada:
    O Selenium WebDriver é usado para simular interações humanas com o site. O código é configurado para navegar até o 
    site Compra Agora, preencher o CNPJ e a Senha, e realizar o login.
    A navegação nas categorias é realizada automaticamente após o login, usando seletores CSS e XPath para localizar e 
    clicar nos elementos corretos do menu.

Resolução de CAPTCHA:
    Um tempo de espera de 15 segundos é inserido para permitir que o CAPTCHA seja resolvido manualmente, 
    já que o site utiliza um CAPTCHA de verificação para evitar automações.
    Houve uma tentativa sem sucesso de utilizar a API externa AntiCaptcha. O CAPTCHA poderia ser resolvido por essa API, 
    porém, após muitas tentativas, não foi possível utilizar a API para este site em específico.

Extração de Produtos:
    O código percorre todas as categorias de produtos e extrai informações como:
        URL da imagem
        Nome do fabricante
        Descrição do produto
    Esses dados são armazenados em uma lista de dicionários e, ao final do processo, são salvos em um arquivo JSON no formato
    adequado para futuras análises.

Paginação:
    O código lida com a paginação da lista de produtos em cada categoria. Para cada categoria, o número de produtos
    é contado e o número de páginas necessário é calculado. O código então clica no botão "Ver mais produtos" até que todas
    as páginas de produtos tenham sido carregadas.

Trabalho com Exceções:
    O código foi projetado para ser robusto, lidando com erros comuns de automação de forma eficiente. Quando ocorre uma exceção, 
    o script tenta continuar a execução, processando a próxima categoria ou produto, sem parar a execução inteira.

Bibliotecas e Ferramentas Utilizadas:
    Selenium WebDriver: Usado para automação de navegação na web e extração de dados.
    WebDriverManager: Facilita o gerenciamento do ChromeDriver para garantir compatibilidade com a versão do navegador.
    AntiCaptcha (opcional): Para resolver CAPTCHA automaticamente (não implementado neste exemplo, mas pode ser integrado).
    Python JSON: Para manipular e salvar as informações dos produtos no formato JSON.

Considerações Finais:
    Esse script é uma solução eficaz para automatizar a extração de dados de sites com uma grande quantidade de produtos, 
    como o Compra Agora. Embora o CAPTCHA ainda seja um obstáculo manual, a automação de login e navegação pode ser integrada 
    facilmente em sistemas mais complexos, que exijam a coleta periódica de dados do site.