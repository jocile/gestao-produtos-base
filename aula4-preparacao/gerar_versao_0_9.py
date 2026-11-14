"""Gera a pasta versao-0.9/ com os 3 arquivos alterados (uso do docente).

Rode sobre a versão CORRETA do sistema. Os originais não são modificados.
"""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SAIDA = RAIZ / "versao-0.9"

VENDA_ORIGINAL = """            conn.execute(
                "UPDATE Produto SET estoque = estoque - ? WHERE id_produto = ?;",
                (quantidade, id_produto),
            )
            cursor = conn.execute(
                "INSERT INTO Vendas (id_produto, quantidade) VALUES (?, ?);",
                (id_produto, quantidade),
            )
            return cursor.lastrowid
"""

VENDA_V09 = """            linha = conn.execute(
                "SELECT estoque FROM Produto WHERE id_produto = ?;", (id_produto,)
            ).fetchone()
            cursor = conn.execute(
                "INSERT INTO Vendas (id_produto, quantidade) VALUES (?, ?);",
                (id_produto, quantidade),
            )
            if linha is not None and linha["estoque"] >= quantidade:
                conn.execute(
                    "UPDATE Produto SET estoque = estoque - ? WHERE id_produto = ?;",
                    (quantidade, id_produto),
                )
            return cursor.lastrowid
"""

ALTERACOES = {
    # Defeito 1: preço negativo passa pela validação
    "validacao.py": [
        (
            "if not math.isfinite(preco) or preco < 0:",
            "if not math.isfinite(preco):",
        ),
    ],
    # Defeito 2: venda registrada sem baixa, e sem erro, quando falta estoque
    "dados.py": [(VENDA_ORIGINAL, VENDA_V09)],
    # Defeito 3: formulário de novo produto abre sem login
    "app.py": [
        (
            '    @app.get("/produtos/novo")\n    @login_required\n    def exibir_formulario():',
            '    @app.get("/produtos/novo")\n    def exibir_formulario():',
        ),
    ],
}

SAIDA.mkdir(exist_ok=True)
for nome, trocas in ALTERACOES.items():
    texto = (RAIZ / nome).read_text(encoding="utf-8")
    for antigo, novo in trocas:
        achados = texto.count(antigo)
        assert achados == 1, f"{nome}: trecho encontrado {achados} vez(es); esperado 1"
        texto = texto.replace(antigo, novo)
    (SAIDA / nome).write_text(texto, encoding="utf-8")
    print(f"ok: {nome}")

print(f"Versão 0.9 gerada em {SAIDA}")
