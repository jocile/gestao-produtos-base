# tests/test_rascunho_banco_real.py   (APAGAR depois da conversa)
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

import dados


def test_venda_maior_que_estoque_nao_altera_nada():
    caminho_bd = str(Path(__file__).parent.parent / "gestao_produtos.db")
    with closing(dados.abrir_conexao(caminho_bd)) as conn:
        conn.execute(
            "INSERT INTO Produto (nome, preco, estoque, id_categoria) "
            "VALUES ('Produto de teste', 10.0, 3, 1);"
        )
        conn.commit()
        id_produto = conn.execute("SELECT MAX(id_produto) FROM Produto;").fetchone()[0]

    with pytest.raises(sqlite3.IntegrityError):
        dados.registrar_venda(caminho_bd, id_produto, 100)
