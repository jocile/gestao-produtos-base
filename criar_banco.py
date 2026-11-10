"""Cria o banco de dados (tabelas e produtos de exemplo). Execute uma vez."""
from dados import DB_PADRAO, criar_estrutura, popular_exemplo


def main() -> None:
    criar_estrutura(DB_PADRAO)
    popular_exemplo(DB_PADRAO)
    print(f"Banco pronto em: {DB_PADRAO}")


if __name__ == "__main__":
    main()
