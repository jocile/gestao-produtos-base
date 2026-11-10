"""Acesso ao banco de dados SQLite do sistema Gestão de Produtos."""
import sqlite3
from contextlib import closing
from pathlib import Path

import seguranca

DB_PADRAO = Path(__file__).resolve().parent / "gestao_produtos.db"

ESTRUTURA = """
CREATE TABLE IF NOT EXISTS Categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL CHECK(preco >= 0.0),
    estoque INTEGER NOT NULL CHECK(estoque >= 0),
    id_categoria INTEGER,
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);

CREATE TABLE IF NOT EXISTS Vendas (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    data_venda TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto)
);

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    salt TEXT NOT NULL
);
"""


def abrir_conexao(caminho) -> sqlite3.Connection:
    """Abre o banco com chaves estrangeiras ativas e linhas acessíveis por nome."""
    caminho = Path(caminho)
    if not caminho.exists():
        # Sem esta checagem, o SQLite criaria um banco vazio em silêncio
        raise FileNotFoundError(f"Banco de dados não encontrado: {caminho}")
    conn = sqlite3.connect(caminho)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------------------------------------------- preparação
def criar_estrutura(caminho) -> None:
    """Cria o arquivo do banco e as tabelas (se ainda não existirem)."""
    with closing(sqlite3.connect(caminho)) as conn:
        conn.executescript(ESTRUTURA)


def popular_exemplo(caminho) -> None:
    """Insere 3 categorias e 5 produtos de exemplo, se o banco ainda estiver vazio."""
    with closing(abrir_conexao(caminho)) as conn:
        with conn:
            if conn.execute("SELECT COUNT(*) FROM Categoria;").fetchone()[0] > 0:
                return
            conn.executemany(
                "INSERT INTO Categoria (nome_categoria) VALUES (?);",
                [("Eletrônicos",), ("Móveis",), ("Vestuário",)],
            )
            conn.executemany(
                "INSERT INTO Produto (nome, preco, estoque, id_categoria) VALUES (?, ?, ?, ?);",
                [
                    ("Smartphone", 1600.00, 10, 1),
                    ("Notebook", 3500.00, 5, 1),
                    ("Sofá", 800.00, 3, 2),
                    ("Cadeira de Escritório", 350.00, 12, 2),
                    ("Camisa Polo", 80.00, 25, 3),
                ],
            )


# ------------------------------------------------------------------- usuários
def cadastrar_usuario(caminho, login: str, senha: str) -> None:
    """Cadastra um usuário guardando apenas o hash e o salt da senha."""
    senha_hash, salt = seguranca.gerar_hash_senha(senha)
    with closing(abrir_conexao(caminho)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO Usuario (login, senha_hash, salt) VALUES (?, ?, ?);",
                (login, senha_hash, salt),
            )


def buscar_usuario(caminho, login: str):
    """Devolve a linha do usuário (ou None se não existir)."""
    with closing(abrir_conexao(caminho)) as conn:
        return conn.execute(
            "SELECT login, senha_hash, salt FROM Usuario WHERE login = ?;",
            (login,),
        ).fetchone()


# ------------------------------------------------------------------- produtos
def listar_categorias(caminho) -> list[dict]:
    """Categorias em ordem alfabética, para preencher a lista do formulário."""
    with closing(abrir_conexao(caminho)) as conn:
        return [
            dict(linha)
            for linha in conn.execute(
                "SELECT id_categoria, nome_categoria FROM Categoria ORDER BY nome_categoria;"
            )
        ]


def listar_produtos(caminho) -> list[dict]:
    """Produtos com o nome da categoria, do mais recente para o mais antigo."""
    with closing(abrir_conexao(caminho)) as conn:
        return [
            dict(linha)
            for linha in conn.execute("""
                SELECT p.id_produto, p.nome, p.preco, p.estoque, c.nome_categoria
                FROM Produto p
                LEFT JOIN Categoria c ON p.id_categoria = c.id_categoria
                ORDER BY p.id_produto DESC;
            """)
        ]


def buscar_produto(caminho, id_produto: int):
    """Devolve o produto como dicionário (ou None se não existir)."""
    with closing(abrir_conexao(caminho)) as conn:
        linha = conn.execute(
            "SELECT id_produto, nome, preco, estoque, id_categoria FROM Produto WHERE id_produto = ?;",
            (id_produto,),
        ).fetchone()
        return dict(linha) if linha else None


def inserir_produto(caminho, nome: str, preco: float, estoque: int, id_categoria: int) -> int:
    """Insere um produto e devolve o id gerado."""
    with closing(abrir_conexao(caminho)) as conn:
        with conn:  # commit automático; rollback em caso de erro
            cursor = conn.execute(
                "INSERT INTO Produto (nome, preco, estoque, id_categoria) VALUES (?, ?, ?, ?);",
                (nome, preco, estoque, id_categoria),
            )
            return cursor.lastrowid


# --------------------------------------------------------------------- vendas
def registrar_venda(caminho, id_produto: int, quantidade: int) -> int:
    """
    Baixa o estoque e registra a venda na MESMA transação (tudo ou nada).
    Se faltar estoque (ou o produto não existir), levanta sqlite3.IntegrityError
    e nada é gravado.
    """
    with closing(abrir_conexao(caminho)) as conn:
        with conn:  # commit se der certo; rollback se der erro
            conn.execute(
                "UPDATE Produto SET estoque = estoque - ? WHERE id_produto = ?;",
                (quantidade, id_produto),
            )
            cursor = conn.execute(
                "INSERT INTO Vendas (id_produto, quantidade) VALUES (?, ?);",
                (id_produto, quantidade),
            )
            return cursor.lastrowid


def listar_vendas(caminho) -> list[dict]:
    """Todas as vendas registradas."""
    with closing(abrir_conexao(caminho)) as conn:
        return [dict(l) for l in conn.execute("SELECT * FROM Vendas ORDER BY id_venda;")]
