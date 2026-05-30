import pytest
from estoque import Estoque

# ==============================================================
# CICLO TDD — RED → GREEN → REFACTOR
#
# Cada bloco abaixo representa uma funcionalidade desenvolvida
# seguindo o ciclo TDD:
#
#   RED      → Teste escrito ANTES da implementação (falha).
#   GREEN    → Código mínimo implementado para o teste passar.
#   REFACTOR → Código reorganizado/melhorado sem quebrar testes.
# ==============================================================


class TestAdicionarProduto:
    """
    RED: Escrevi os testes abaixo esperando que Estoque tenha
         o método adicionar_produto — que ainda não existia.
    GREEN: Implementei adicionar_produto em estoque.py.
    REFACTOR: Extrai a lógica de validação para mensagens claras.
    """

    def test_adicionar_produto_novo(self):
        estoque = Estoque()
        estoque.adicionar_produto("Caneta", 10)
        assert estoque.consultar_estoque("Caneta") == 10

    def test_adicionar_produto_existente_acumula_quantidade(self):
        estoque = Estoque()
        estoque.adicionar_produto("Caneta", 10)
        estoque.adicionar_produto("Caneta", 5)
        assert estoque.consultar_estoque("Caneta") == 15

    def test_adicionar_quantidade_zero_levanta_erro(self):
        estoque = Estoque()
        with pytest.raises(ValueError):
            estoque.adicionar_produto("Caneta", 0)

    def test_adicionar_quantidade_negativa_levanta_erro(self):
        estoque = Estoque()
        with pytest.raises(ValueError):
            estoque.adicionar_produto("Caneta", -3)

    def test_adicionar_nome_vazio_levanta_erro(self):
        estoque = Estoque()
        with pytest.raises(ValueError):
            estoque.adicionar_produto("", 5)


class TestRemoverProduto:
    """
    RED: Testes escritos antes de remover_produto existir.
    GREEN: Implementei a lógica de remoção com validação de saldo.
    REFACTOR: Unifiquei a verificação de existência do produto
              em um único ponto (KeyError).
    """

    def test_remover_produto_reduz_quantidade(self):
        estoque = Estoque()
        estoque.adicionar_produto("Papel", 20)
        estoque.remover_produto("Papel", 8)
        assert estoque.consultar_estoque("Papel") == 12

    def test_remover_mais_que_disponivel_levanta_erro(self):
        estoque = Estoque()
        estoque.adicionar_produto("Papel", 5)
        with pytest.raises(ValueError):
            estoque.remover_produto("Papel", 10)

    def test_remover_produto_inexistente_levanta_erro(self):
        estoque = Estoque()
        with pytest.raises(KeyError):
            estoque.remover_produto("Borracha", 1)

    def test_remover_quantidade_zero_levanta_erro(self):
        estoque = Estoque()
        estoque.adicionar_produto("Papel", 10)
        with pytest.raises(ValueError):
            estoque.remover_produto("Papel", 0)

    def test_remover_toda_quantidade_zera_estoque(self):
        estoque = Estoque()
        estoque.adicionar_produto("Papel", 5)
        estoque.remover_produto("Papel", 5)
        assert estoque.consultar_estoque("Papel") == 0


class TestAtualizarQuantidade:
    """
    RED: Testes escritos antes de atualizar_quantidade existir.
    GREEN: Implementei a atualização direta de quantidade.
    REFACTOR: Reutilizei a validação de existência já presente
              em outros métodos.
    """

    def test_atualizar_quantidade_valida(self):
        estoque = Estoque()
        estoque.adicionar_produto("Lápis", 10)
        estoque.atualizar_quantidade("Lápis", 25)
        assert estoque.consultar_estoque("Lápis") == 25

    def test_atualizar_para_zero_permitido(self):
        estoque = Estoque()
        estoque.adicionar_produto("Lápis", 10)
        estoque.atualizar_quantidade("Lápis", 0)
        assert estoque.consultar_estoque("Lápis") == 0

    def test_atualizar_quantidade_negativa_levanta_erro(self):
        estoque = Estoque()
        estoque.adicionar_produto("Lápis", 10)
        with pytest.raises(ValueError):
            estoque.atualizar_quantidade("Lápis", -1)

    def test_atualizar_produto_inexistente_levanta_erro(self):
        estoque = Estoque()
        with pytest.raises(KeyError):
            estoque.atualizar_quantidade("Fantasma", 5)


class TestConsultarEstoque:
    """
    RED: Testes escritos antes de consultar_estoque existir.
    GREEN: Retorna a quantidade do dicionário interno.
    REFACTOR: Sem alterações necessárias — método já era simples.
    """

    def test_consultar_produto_existente(self):
        estoque = Estoque()
        estoque.adicionar_produto("Régua", 7)
        assert estoque.consultar_estoque("Régua") == 7

    def test_consultar_produto_inexistente_levanta_erro(self):
        estoque = Estoque()
        with pytest.raises(KeyError):
            estoque.consultar_estoque("Inexistente")


class TestAlertaEstoqueMinimo:
    """
    RED: Testes escritos antes de verificar_alerta existir.
    GREEN: Comparei com a constante QUANTIDADE_MINIMA (5).
    REFACTOR: Movi a constante para atributo de classe,
              facilitando eventual configuração futura.
    """

    def test_alerta_quando_abaixo_do_minimo(self):
        estoque = Estoque()
        estoque.adicionar_produto("Clips", 3)
        assert estoque.verificar_alerta("Clips") is True

    def test_sem_alerta_quando_acima_do_minimo(self):
        estoque = Estoque()
        estoque.adicionar_produto("Clips", 10)
        assert estoque.verificar_alerta("Clips") is False

    def test_sem_alerta_exatamente_no_minimo(self):
        estoque = Estoque()
        estoque.adicionar_produto("Clips", 5)
        assert estoque.verificar_alerta("Clips") is False

    def test_alerta_apos_remocao(self):
        estoque = Estoque()
        estoque.adicionar_produto("Clips", 6)
        estoque.remover_produto("Clips", 3) 
        assert estoque.verificar_alerta("Clips") is True


class TestListarProdutos:
    """
    RED: Testes escritos antes de listar_produtos existir.
    GREEN: Retorna a cópia do dicionário interno.
    REFACTOR: Garanti que é uma cópia (não referência direta).
    """

    def test_listar_retorna_todos_os_produtos(self):
        estoque = Estoque()
        estoque.adicionar_produto("Caneta", 10)
        estoque.adicionar_produto("Lápis", 5)
        produtos = estoque.listar_produtos()
        assert "Caneta" in produtos
        assert "Lápis" in produtos

    def test_listar_estoque_vazio_retorna_dict_vazio(self):
        estoque = Estoque()
        assert estoque.listar_produtos() == {}

    def test_listar_retorna_copia_nao_referencia(self):
        estoque = Estoque()
        estoque.adicionar_produto("Caneta", 10)
        copia = estoque.listar_produtos()
        copia["Caneta"] = 999  
        assert estoque.consultar_estoque("Caneta") == 10
