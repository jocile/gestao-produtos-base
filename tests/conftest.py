"""
Fixtures compartilhadas pelos testes.

O pytest carrega este arquivo sozinho. Qualquer teste pode "pedir" uma
fixture escrevendo o nome dela como parâmetro.
"""

import re
from contextlib import closing

import pytest

import dados
from app import create_app
from seguranca import gerar_hash_senha

USUARIO_TESTE = "tester"
SENHA_TESTE = "SenhaTeste123"


@pytest.fixture(scope="session")
def credenciais_hash():
    """Gera o hash da senha UMA vez por execução (o hash é lento de propósito)."""
    return gerar_hash_senha(SENHA_TESTE)


@pytest.fixture
def banco_temporario(tmp_path, credenciais_hash):
    """Cria um banco novo para cada teste e devolve o CAMINHO dele.

    O arquivo fica numa pasta temporária que o pytest apaga depois,
    então o banco real do sistema nunca é tocado.
    """
    caminho = tmp_path / "banco_de_teste.db"

    dados.criar_estrutura(caminho)  # cria as tabelas
    dados.popular_exemplo(caminho)  # 3 categorias e 5 produtos, sempre os mesmos

    senha_hash, salt = credenciais_hash
    with closing(dados.abrir_conexao(caminho)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO Usuario (login, senha_hash, salt) VALUES (?, ?, ?);",
                (USUARIO_TESTE, senha_hash, salt),
            )
    return caminho


@pytest.fixture
def banco(banco_temporario):
    """Conexão para o teste consultar o banco temporário."""
    conn = dados.abrir_conexao(banco_temporario)
    yield conn
    conn.close()


@pytest.fixture
def aplicacao(banco_temporario):
    """Uma aplicação Flask nova, configurada para usar o banco temporário."""
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "segredo-somente-para-testes",
            "DB_PATH": banco_temporario,
        }
    )


@pytest.fixture
def cliente(aplicacao):
    """Test client do Flask: simula o navegador sem abrir o servidor."""
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
        achou = re.search(r'name="csrf_token"\s+value="([^"]+)"', pagina)
        assert achou, "Token CSRF não encontrado no formulário"
        return achou.group(1)

    return _obter
