"""Gabarito (Aula 2): testes unitários de seguranca.py."""
from seguranca import gerar_hash_senha, verificar_senha


def test_mesma_senha_gera_hashes_diferentes_por_causa_do_salt():
    hash1, salt1 = gerar_hash_senha("minha-senha")
    hash2, salt2 = gerar_hash_senha("minha-senha")
    assert salt1 != salt2
    assert hash1 != hash2


def test_senha_correta_e_aceita():
    hash_salvo, salt = gerar_hash_senha("minha-senha")
    assert verificar_senha("minha-senha", hash_salvo, salt) is True


def test_senha_errada_e_recusada():
    hash_salvo, salt = gerar_hash_senha("minha-senha")
    assert verificar_senha("outra-senha", hash_salvo, salt) is False
