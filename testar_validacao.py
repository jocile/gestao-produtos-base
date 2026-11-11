from validacao import validar_produto

CATEGORIAS = {1, 2, 3}

# Caso válido
dados, erros = validar_produto(
    {"nome": "Mouse sem fio", "preco": "89,90", "estoque": "20", "id_categoria": "1"},
    CATEGORIAS,
)
assert erros == {}
assert dados == {
    "nome": "Mouse sem fio",
    "preco": 89.9,
    "estoque": 20,
    "id_categoria": 1,
}

# Preço negativo
dados, erros = validar_produto(
    {"nome": "Mouse", "preco": "-5", "estoque": "2", "id_categoria": "1"},
    CATEGORIAS,
)
assert dados is None
assert "preco" in erros

# Nome vazio
dados, erros = validar_produto(
    {"nome": "", "preco": "10", "estoque": "2", "id_categoria": "1"},
    CATEGORIAS,
)
assert dados is None
assert "nome" in erros

print("Todas as verificações passaram.")
