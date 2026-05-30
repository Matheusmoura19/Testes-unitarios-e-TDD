class Estoque:
    QUANTIDADE_MINIMA = 5

    def __init__(self):
        self._produtos = {}

    def adicionar_produto(self, nome: str, quantidade: int):
        """Adiciona um produto ou aumenta sua quantidade no estoque."""

        if not nome or not isinstance(nome, str):
            raise ValueError("Nome do produto inválido.")
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        if nome in self._produtos:
            self._produtos[nome] += quantidade
        else:
            self._produtos[nome] = quantidade

    def atualizar_quantidade(self, nome: str, quantidade: int):
        """Atualiza a quantidade de um produto existente."""

        if nome not in self._produtos:
            raise KeyError(f"Produto '{nome}' não encontrado no estoque.")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
        self._produtos[nome] = quantidade

    def remover_produto(self, nome: str, quantidade: int):
        """Remove (dá saída) uma quantidade do produto."""

        if nome not in self._produtos:
            raise KeyError(f"Produto '{nome}' não encontrado no estoque.")
        if quantidade <= 0:
            raise ValueError("Quantidade a remover deve ser positiva.")
        if quantidade > self._produtos[nome]:
            raise ValueError("Estoque insuficiente para remoção.")
        self._produtos[nome] -= quantidade

    def consultar_estoque(self, nome: str) -> int:
        """Retorna a quantidade disponível de um produto."""

        if nome not in self._produtos:
            raise KeyError(f"Produto '{nome}' não encontrado no estoque.")
        return self._produtos[nome]

    def verificar_alerta(self, nome: str) -> bool:
        """Retorna True se a quantidade estiver abaixo do mínimo."""

        return self.consultar_estoque(nome) < self.QUANTIDADE_MINIMA

    def listar_produtos(self) -> dict:
        """Retorna cópia do dicionário de produtos."""

        return dict(self._produtos)
