class Node:
    def __init__(self, valor):
        """
        Inicializa um novo nó com um valor e uma lista de filhos.
        
        Parâmetros:
        valor (any): O valor armazenado neste nó.
        """
        self.valor = valor  # Armazena o valor do nó
        self.filhos = []    # Inicializa a lista de filhos do nó como vazia

    def adicionar_filho(self, filho):
        """
        Adiciona um novo nó filho a este nó.
        
        Parâmetros:
        filho (Node): O nó filho que será adicionado.
        """
        self.filhos.append(filho)  # Adiciona o filho à lista de filhos

    def __repr__(self):
        """
        Representação do nó para depuração. Mostra o valor do nó.

        Retorna:
        str: Representação do nó com seu valor.
        """
        return f"Node({self.valor})"  # Retorna a representação do nó com seu valor
