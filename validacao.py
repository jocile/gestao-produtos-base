"""Regras de validação do cadastro de produto (sem dependência do Flask)."""
import math


def validar_produto(campos: dict, ids_categoria_validos: set[int]):
    """
    Valida os campos recebidos do formulário (todos como texto).
    Devolve (dados, erros): se houver erros, 'dados' é None.
    """
    erros = {}

    nome = campos["nome"].strip()
    if not nome:
        erros["nome"] = "Informe o nome do produto."
    elif len(nome) > 100:
        erros["nome"] = "O nome deve ter no máximo 100 caracteres."

    preco = None
    try:
        preco = float(campos["preco"].strip().replace(",", "."))
        if not math.isfinite(preco) or preco < 0:
            raise ValueError
    except ValueError:
        erros["preco"] = "Informe um preço válido, igual ou maior que zero (ex.: 49,90)."

    estoque = None
    try:
        estoque = int(campos["estoque"].strip())
        if estoque < 0:
            raise ValueError
    except ValueError:
        erros["estoque"] = "Informe o estoque como um número inteiro, igual ou maior que zero."

    id_categoria = None
    try:
        id_categoria = int(campos["id_categoria"])
        if id_categoria not in ids_categoria_validos:
            raise ValueError
    except ValueError:
        erros["id_categoria"] = "Selecione uma categoria da lista."

    if erros:
        return None, erros

    return {
        "nome": nome,
        "preco": round(preco, 2),
        "estoque": estoque,
        "id_categoria": id_categoria,
    }, {}
