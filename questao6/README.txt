Execução:
Para executar o código da questão 6, siga as instruções abaixo:

Primeiro digite o comando abaixo para que você faca a construção do container do docker a partir da imagem feita:

docker build -t prova_tecnica .

No terminal, digite o seguinte comando, substituindo "Nome_autor" pelo nome do autor que você deseja extrair as informações:

docker run -it prova_tecnica python questao6/questao6.py "Nome_autor"

Exemplo: 

docker run -it prova_tecnica python questao6/questao6.py "J.K. Rowling"


Após a execução, as informações extraídas serão armazenadas em um arquivo chamado citacoes.json na raiz do projeto dentro do container para baixar no local e verificar 
as informações execute os comando abaixo.

docker ps -a 

verifique o ultimo container de docker utilizado e pegue o container ID armazenado.
após isso utilize o comando abaixo substituindo "<container_id>" pelo container ID que você pegou no comando anterior 

docker cp <container_id>:/app/citacoes.json ./citacoes.json

isso fará uma copia do arquivo JSON gerado dentro do container para o diretório atual do seu computador.

Visão Técnica:
Para este código, foi utilizada a biblioteca Python Selenium para navegar na página e extrair as informações necessárias.

A automação de navegação foi realizada com o WebDriver, que permite acessar e interagir com a página para capturar as citações do autor.

O código recebe o nome do autor como argumento e inicia o processo de extração das citações e das respectivas tags associadas a elas.
Durante o processo de extração, na primeira citação encontrada, o código também obtém informações sobre o autor.
Para garantir que a extração do autor ocorra apenas uma vez, foi implementado um tratamento de exceção que limita essa extração à primeira ocorrência.
As informações extraídas são armazenadas em arrays, e ao final do processo, todas as informações são salvas em um arquivo citacoes.json no formato JSON.