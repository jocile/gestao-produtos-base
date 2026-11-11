"""
Fixtures compartilhadas pelos testes.

O pytest carrega este arquivo sozinho. Qualquer teste pode "pedir" uma
fixture escrevendo o nome dela como parâmetro.
"""

import os
import re
import sqlite3

import dados

# O segredo precisa existir ANTES de importar o app
os.environ.setdefault("APP_SECRET", "segredo-somente-para-testes")

import pytest

from app import app as aplicacao
from seguranca import gerar_hash_senha

USUARIO_TESTE = "tester"
SENHA_TESTE = "SenhaTeste123"

ESQUEMA = """
CREATE TABLE Categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT NOT NULL
);
CREATE TABLE Produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL CHECK(preco >= 0.0),
    estoque INTEGER NOT NULL CHECK(estoque >= 0),
    id_categoria INTEGER,
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);
CREATE TABLE Vendas (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    data_venda TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto)
);
CREATE TABLE Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    salt TEXT NOT NULL
);
"""

CATEGORIAS = [("Eletrônicos",), ("Móveis",), ("Vestuário",)]

# (nome, preço, estoque, id_categoria)
PRODUTOS = [
    ("Smartphone", 1600.00, 10, 1),
    ("Notebook", 3500.00, 5, 1),
    ("Sofá", 800.00, 3, 2),
    ("Cadeira de Escritório", 350.00, 12, 2),
    ("Camisa Polo", 80.00, 25, 3),
]


@pytest.fixture(scope="session")
def credenciais_hash():
    """Gera o hash da senha UMA vez por execução (o hash é lento de propósito)."""
    return gerar_hash_senha(SENHA_TESTE)


@pytest.fixture
def banco_temporario(tmp_path, monkeypatch, credenciais_hash):
    """Cria um banco novo para cada teste e faz o sistema usá-lo.

    O arquivo fica numa pasta temporária que o pytest apaga depois,
    então o banco real do sistema nunca é tocado.
    """
    caminho = tmp_path / "banco_de_teste.db"

    conn = sqlite3.connect(caminho)
    conn.executescript(ESQUEMA)
    conn.executemany("INSERT INTO Categoria (nome_categoria) VALUES (?);", CATEGORIAS)
    conn.executemany(
        "INSERT INTO Produto (nome, preco, estoque, id_categoria) VALUES (?, ?, ?, ?);",
        PRODUTOS,
    )
    senha_hash, salt = credenciais_hash
    conn.execute(
        "INSERT INTO Usuario (login, senha_hash, salt) VALUES (?, ?, ?);",
        (USUARIO_TESTE, senha_hash, salt),
    )
    conn.commit()
    conn.close()

    # Redireciona QUALQUER chamada a dados.abrir_conexao para o banco temporário,
    # seja qual for o caminho que o app.py passar.
    abrir_original = dados.abrir_conexao

    def abrir_conexao_de_teste(_caminho=None):
        return abrir_original(caminho)

    monkeypatch.setattr(dados, "abrir_conexao", abrir_conexao_de_teste)

    return caminho


@pytest.fixture
def banco(banco_temporario):
    """Conexão para o teste consultar o banco temporário."""
    conn = sqlite3.connect(banco_temporario)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture
def cliente(banco_temporario):
    """Test client do Flask: simula o navegador sem abrir o servidor."""
    aplicacao.config.update(TESTING=True)
    with aplicacao.test_client() as c:
        yield c


@pytest.fixture
def cliente_logado(cliente):
    """O mesmo cliente, já autenticado com o usuário de teste."""
    resposta = cliente.post(
        "/login", data={"usuario": USUARIO_TESTE, "senha": SENHA_TESTE}
    )
    assert resposta.status_code == 302, "O login de teste falhou"
    return cliente


@pytest.fixture
def obter_token_csrf(cliente_logado):
    """Devolve uma função que lê o token CSRF do formulário de novo produto."""

    def _obter():
        pagina = cliente_logado.get("/produtos/novo").get_data(as_text=True)
        achou = re.search(r'name="csrf_token" value="([^"]+)"', pagina)
        assert achou, "Token CSRF não encontrado no formulário"
        return achou.group(1)

    return _obter
