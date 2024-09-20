EXECUÇÃO:
Para executar os testes da árvore, siga as instruções abaixo:

Primeiro digite o comando abaixo para que você faca a construção do container do docker a partir da imagem feita:

docker build -t prova_tecnica .

No terminal, digite o seguinte comando para rodar o código de testes unitários:
    
docker run -it prova_tecnica python -m unittest questao5/test_tree.py

Após a execução, o sistema retornará o resultado dos testes diretamente no terminal, mostrando o número de testes executados e se todos passaram ou se algum falhou.



VISÃO TECNICA:

Passos para a construção da estrutura de dados "Árvore" em Python:

A construção de uma árvore, seja em Python ou em outra linguagem, envolve dois componentes principais:

    Nó (Node): Representa cada unidade da árvore, contendo um valor e referências para seus nós filhos. Cada nó pode ter múltiplos filhos, 
    formando uma hierarquia que, em conjunto, é chamada de árvore.

    Árvore (Tree): A árvore é responsável por gerenciar os nós a partir do nó raiz. Ela fornece operações como inserção, busca e percursos, 
    além de organizar a estrutura hierárquica.

Classes Utilizadas:

Classe Node (Nó da Árvore):
    O nó é a unidade básica da árvore. Ele contém:
        Um valor (que pode ser qualquer tipo de dado).
        ma lista de filhos (outros nós conectados a ele).

Classe Tree (Árvore):
    A classe Tree gerencia a estrutura da árvore.
    Contém uma referência ao nó raiz.
    Fornece métodos para operações comuns, como:
        Inserir: Adiciona nós filhos a partir de um nó existente.
        Buscar: Encontra um nó específico na árvore.
        Percorrer: Realiza percursos nos nós da árvore (ex: pré-ordem, pós-ordem).

Classe TestArvore (Testes Unitários):
    Os testes unitários garantem que a árvore funciona conforme esperado.
    Utilizamos a biblioteca unittest do Python para automatizar esses testes.

Os principais métodos de teste são:
    test_busca_no_existente: Verifica se a busca por um nó existente (ex: D) retorna corretamente o nó esperado.
    test_busca_no_inexistente: Testa se a busca por um nó inexistente (ex: Z) retorna None, como esperado.
    test_inserir: Testa a inserção de um novo nó (ex: G como filho de C) e verifica se ele foi inserido corretamente.
    test_percurso_pre_ordem: Verifica se o percurso em pré-ordem da árvore retorna os nós na ordem correta.

Explicação dos Testes:
No método setUp, é configurada uma árvore de exemplo antes de cada teste, com a seguinte estrutura:

      A
     / \
    B   C
   / \   \
  D   E   F

Os testes fazem as seguintes verificações:
1. test_busca_no_existente: Testa se o nó D é encontrado corretamente.
2. test_busca_no_inexistente: Verifica se a busca por um nó inexistente (ex: Z) retorna None.
3. test_inserir: Tenta inserir um novo nó G como filho de C e verifica se a inserção foi bem-sucedida.
4. test_percurso_pre_ordem: Testa se o percurso em pré-ordem da árvore segue a ordem correta de visitação dos nós.
Ao final da execução, o output mostrará se todos os testes passaram ou se ocorreram falhas, com os detalhes de cada teste.