"""Cadastra um usuário. A senha é pedida no terminal, sem aparecer na tela."""
import getpass
import sqlite3

from dados import DB_PADRAO, cadastrar_usuario


def main() -> None:
    login = input("Novo usuário: ").strip()
    senha = getpass.getpass("Senha (mínimo 8 caracteres): ")
    confirmacao = getpass.getpass("Repita a senha: ")

    if not login:
        raise SystemExit("O nome de usuário não pode ficar vazio.")
    if len(senha) < 8:
        raise SystemExit("A senha deve ter pelo menos 8 caracteres.")
    if senha != confirmacao:
        raise SystemExit("As senhas não conferem.")

    try:
        cadastrar_usuario(DB_PADRAO, login, senha)
    except sqlite3.IntegrityError:
        raise SystemExit(f"O usuário '{login}' já existe.")
    print(f"Usuário '{login}' criado com sucesso.")


if __name__ == "__main__":
    main()
