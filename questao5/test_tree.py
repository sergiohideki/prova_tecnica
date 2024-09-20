import unittest
from questao5.node import Node
from questao5.tree import Tree

class TestArvore(unittest.TestCase):
    """
    Classe de teste que verifica o funcionamento da árvore.
    Utiliza a biblioteca unittest para realizar testes unitários.
    """

    def setUp(self):
        """
        Configura uma árvore para ser usada em todos os testes.
        Estrutura da árvore:
                A
               / \
              B   C
             / \   \
            D   E   F
        """
        self.raiz = Node('A')  # Cria o nó raiz 'A'
        self.arvore = Tree(self.raiz)  # Cria uma árvore com o nó raiz 'A'
        self.arvore.inserir('A', 'B')
        self.arvore.inserir('A', 'C')
        self.arvore.inserir('B', 'D')
        self.arvore.inserir('B', 'E')
        self.arvore.inserir('C', 'F')

    def test_busca_no_existente(self):
        """
        Testa se a busca retorna corretamente um nó existente na árvore.
        Verifica se o nó 'D' pode ser encontrado.
        """
        no = self.arvore.buscar('D')
        self.assertIsNotNone(no)  # Verifica que o nó não é None (ou seja, foi encontrado)
        self.assertEqual(no.valor, 'D')  # Verifica que o valor do nó encontrado é 'D'

    def test_busca_no_inexistente(self):
        """
        Testa se a busca retorna None quando o nó não existe na árvore.
        Verifica se o nó 'Z' não pode ser encontrado.
        """
        no = self.arvore.buscar('Z')
        self.assertIsNone(no)  # Verifica que o nó é None (ou seja, não foi encontrado)

    def test_inserir(self):
        """
        Testa se a inserção de um novo nó filho funciona corretamente.
        Insere o nó 'G' como filho de 'C' e verifica se foi inserido corretamente.
        """
        self.arvore.inserir('C', 'G')  # Insere 'G' como filho de 'C'
        no_g = self.arvore.buscar('G')  # Busca o nó 'G'
        self.assertIsNotNone(no_g)  # Verifica que o nó 'G' foi encontrado
        self.assertEqual(no_g.valor, 'G')  # Verifica que o valor do nó é 'G'

    def test_percurso_pre_ordem(self):
        """
        Testa o percurso em pré-ordem na árvore.
        Verifica se a ordem de visitação dos nós está correta.
        """
        valores_esperados = ['A', 'B', 'D', 'E', 'C', 'F']  # Ordem esperada de visitação em pré-ordem
        valores_percorridos = []

        def percurso_customizado(node):
            valores_percorridos.append(node.valor)  # Adicion
