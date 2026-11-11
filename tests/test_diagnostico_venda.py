# tests/test_diagnostico_venda.py   (apagar depois; só funciona de verdade na v0.9)
import dados


def test_diagnostico_venda(banco_temporario, banco):
    dados.registrar_venda(banco_temporario, 3, 100)

    estoque = banco.execute(
        "SELECT estoque FROM Produto WHERE id_produto = 3;"
    ).fetchone()[0]
    vendas = banco.execute("SELECT COUNT(*) FROM Vendas;").fetchone()[0]
    print("estoque:", estoque, "| vendas:", vendas)
