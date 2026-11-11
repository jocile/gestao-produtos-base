import sqlite3

import pytest
from conftest import SENHA_TESTE, USUARIO_TESTE

import dados


def test_venda_com_estoque_suficiente_baixa_estoque_e_registra_venda(
    banco_temporario, banco
):
    # Executar: registrar_venda recebe o caminho do banco
    dados.registrar_venda(banco_temporario, 1, 3)

    # Verificar
    estoque = banco.execute(
        "SELECT estoque FROM Produto WHERE id_produto = 1;"
    ).fetchone()["estoque"]
    vendas = banco.execute(
        "SELECT COUNT(*) AS total, SUM(quantidade) AS unidades "
        "FROM Vendas WHERE id_produto = 1;"
    ).fetchone()

    assert estoque == 7
    assert vendas["total"] == 1
    assert vendas["unidades"] == 3


def test_venda_com_estoque_insuficiente_nao_altera_nada(banco_temporario, banco):
    with pytest.raises(sqlite3.IntegrityError):
        dados.registrar_venda(banco_temporario, 3, 100)

    estoque = banco.execute(
        "SELECT estoque FROM Produto WHERE id_produto = 3;"
    ).fetchone()["estoque"]
    total_vendas = banco.execute("SELECT COUNT(*) FROM Vendas;").fetchone()[0]

    assert estoque == 3
    assert total_vendas == 0


def test_pagina_de_novo_produto_sem_login_redireciona_para_o_login(cliente):
    resposta = cliente.get("/produtos/novo")

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_login_valido_libera_a_lista_de_produtos(cliente):
    # Executar o login
    login = cliente.post(
        "/login", data={"usuario": USUARIO_TESTE, "senha": SENHA_TESTE}
    )
    assert login.status_code == 302

    # Verificar que a lista agora abre
    lista = cliente.get("/produtos")

    assert lista.status_code == 200
    assert "Smartphone" in lista.get_data(as_text=True)


# ---- Desafios opcionais ----


def test_envio_sem_token_csrf_retorna_403(cliente_logado, banco):
    resposta = cliente_logado.post(
        "/produtos",
        data={
            "nome": "Teste CSRF",
            "preco": "10,00",
            "estoque": "1",
            "id_categoria": "1",
        },
    )

    assert resposta.status_code == 403
    assert banco.execute("SELECT COUNT(*) FROM Produto;").fetchone()[0] == 5


def test_dados_invalidos_retornam_400(cliente_logado, obter_token_csrf, banco):
    resposta = cliente_logado.post(
        "/produtos",
        data={
            "csrf_token": obter_token_csrf(),
            "nome": "Teste",
            "preco": "-10",
            "estoque": "1",
            "id_categoria": "1",
        },
    )

    assert resposta.status_code == 400
    assert "Informe um preço válido" in resposta.get_data(as_text=True)
    assert banco.execute("SELECT COUNT(*) FROM Produto;").fetchone()[0] == 5
