from questao5.node import Node

class Tree:
    def __init__(self, raiz=None):
        """
        Inicializa a árvore com uma raiz opcional.
        
        Parâmetros:
        raiz (Node): O nó raiz da árvore. Se não fornecido, será None.
        """
        self.raiz = raiz  # Define o nó raiz da árvore, que pode ser None

    def buscar(self, valor):
        """
        Busca um nó com o valor especificado na árvore.
        
        Parâmetros:
        valor (any): O valor a ser buscado na árvore.
        
        Retorna:
        Node ou None: O nó com o valor correspondente, ou None se não for encontrado.
        """
        if self.raiz is None:
            return None  # Se a árvore não tem raiz, retorna None
        return self._buscar_recursivo(self.raiz, valor)  # Inicia a busca a partir da raiz

    def _buscar_recursivo(self, node, valor):
        """
        Função auxiliar recursiva para buscar um valor a partir de um nó específico.
        
        Parâmetros:
        node (Node): O nó a partir do qual a busca será realizada.
        valor (any): O valor a ser buscado.
        
        Retorna:
        Node ou None: O nó com o valor correspondente, ou None se não for encontrado.
        """
        if node.valor == valor:
            return node  # Se o valor do nó atual é o valor buscado, retorna o nó

        # Itera sobre os filhos do nó atual e continua a busca recursivamente
        for filho in node.filhos:
            resultado = self._buscar_recursivo(filho, valor)  # Busca nos filhos
            if resultado:
                return resultado  # Se encontrar o valor em um dos filhos, retorna o resultado
        return None  # Retorna None se o valor não foi encontrado

    def percurso_pre_ordem(self, node=None):
        """
        Realiza um percurso em pré-ordem na árvore, imprimindo o valor de cada nó.
        
        Pré-ordem: Visita o nó atual antes de seus filhos.
        
        Parâmetros:
        node (Node): O nó inicial para o percurso. Se None, começa pela raiz.
        """
        if node is None:
            node = self.raiz  # Se nenhum nó for fornecido, começa pela raiz

        print(node.valor)  # Imprime o valor do nó atual
        for filho in node.filhos:
            self.percurso_pre_ordem(filho)  # Chama recursivamente para cada filho

    def inserir(self, valor_pai, valor_filho):
        """
        Insere um novo nó filho a um nó pai especificado.
        
        Parâmetros:
        valor_pai (any): O valor do nó pai onde o novo filho será inserido.
        valor_filho (any): O valor do novo nó filho a ser inserido.
        """
        pai = self.buscar(valor_pai)  # Busca o nó pai pelo valor
        if pai is None:
            print(f"Nó pai com valor {valor_pai} não encontrado.")  # Se não encontrado, imprime erro
        else:
            pai.adicionar_filho(Node(valor_filho))  # Adiciona o novo nó filho ao pai encontrado
