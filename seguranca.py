"""Segurança de senhas: hash com salt (PBKDF2) e comparação em tempo constante."""
import hashlib
import hmac
import os

ITERACOES = 600_000


def gerar_hash_senha(senha: str) -> tuple[str, str]:
    """Gera um salt aleatório e devolve (hash_hex, salt_hex)."""
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, ITERACOES)
    return hash_bytes.hex(), salt.hex()


def verificar_senha(senha: str, hash_salvo: str, salt_salvo: str) -> bool:
    """Recalcula o hash com o salt salvo e compara com o hash armazenado."""
    hash_calculado = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), bytes.fromhex(salt_salvo), ITERACOES
    )
    # compare_digest compara em tempo constante e evita ataques de temporização
    return hmac.compare_digest(hash_calculado.hex(), hash_salvo)
