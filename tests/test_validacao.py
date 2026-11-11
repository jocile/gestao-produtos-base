"""Gabarito (Aula 2): testes unitários de validar_produto."""
from validacao import validar_produto

CATEGORIAS = {1, 2, 3}


def campos(**mudancas):
    """Campos de um produto válido; cada teste altera só o que quer testar."""
    base = {"nome": "Mouse sem fio", "preco": "89,90", "estoque": "20", "id_categoria": "1"}
    base.update(mudancas)
    return base


def test_produto_valido_aceita_virgula_decimal_e_espacos():
    dados, erros = validar_produto(campos(nome=" Mouse sem fio "), CATEGORIAS)
    assert erros == {}
    assert dados == {"nome": "Mouse sem fio", "preco": 89.9, "estoque": 20, "id_categoria": 1}


def test_preco_negativo_e_recusado():
    dados, erros = validar_produto(campos(preco="-5"), CATEGORIAS)
    assert dados is None
    assert "preco" in erros


def test_preco_zero_e_aceito():
    dados, erros = validar_produto(campos(preco="0"), CATEGORIAS)
    assert erros == {}
    assert dados["preco"] == 0.0


def test_preco_infinito_e_recusado():
    _, erros = validar_produto(campos(preco="inf"), CATEGORIAS)
    assert "preco" in erros


def test_estoque_decimal_e_recusado():
    _, erros = validar_produto(campos(estoque="2.5"), CATEGORIAS)
    assert "estoque" in erros


def test_categoria_inexistente_e_recusada():
    _, erros = validar_produto(campos(id_categoria="99"), CATEGORIAS)
    assert "id_categoria" in erros


def test_nome_vazio_e_recusado():
    _, erros = validar_produto(campos(nome="   "), CATEGORIAS)
    assert "nome" in erros


def test_nome_com_mais_de_100_caracteres_e_recusado():
    _, erros = validar_produto(campos(nome="A" * 101), CATEGORIAS)
    assert "nome" in erros
