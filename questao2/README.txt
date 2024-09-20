Execução:
Para executar o código da questão 6, siga as instruções abaixo:

Primeiro digite o comando abaixo para que você faca a construção do container do docker a partir da imagem feita:

docker build -t prova_tecnica .

No terminal, digite o seguinte comando, substituindo "N° do pedido" pelo número do pedido que você deseja extrair as informações:

docker run -it prova_tecnica python questao2/questao2.py "N° do pedido"

Exemplo: 

docker run -it prova_tecnica python questao2/questao2.py 511082


Após a execução, as informações extraídas serão armazenadas em um arquivo chamado pedido_"N° do pedido".json (onde o "N° de pedido" é número que você digitou 
no argumento da execução do código) na raiz do projeto dentro do container.

Para baixar o arquivo JSON gerado e verificá-lo no seu computador, siga os passos abaixo:
Execute o seguinte comando para listar os containers:

docker ps -a 

Verifique o último container utilizado e anote o Container ID.
Depois, execute o comando abaixo, substituindo <container_id> pelo Container ID anotado anteriormente e "N° do pedido" pelo número do pedido:

docker cp <container_id>:/app/pedido_"N° do pedido".json ./pedido_"N° do pedido".json

Esse comando fará uma cópia do arquivo JSON gerado dentro do container para o diretório atual no seu computador.


Visão Técnica:
Este código utiliza a biblioteca Python Selenium para navegar na página e extrair as informações necessárias.

A automação de navegação é realizada com o WebDriver, que permite acessar e interagir com a página para capturar as informações referentes ao número do pedido.

Funcionamento:

1. O código recebe o número do pedido como argumento e inicia o processo de login no sistema.
2. Após o login, o script procura pelo número do pedido fornecido.
3. Se o pedido for encontrado, o código extrai as seguintes informações:
   Motivo da rejeição (se houver),
   Itens do pedido: código do produto, descrição e quantidade faturada.
4. O código também inclui um tratamento de exceção para o caso de o pedido não ser encontrado, retornando uma mensagem apropriada.
5. As informações extraídas são armazenadas em arrays e, ao final do processo, todas são salvas em um arquivo pedido_"N° do pedido".json no formato JSON.