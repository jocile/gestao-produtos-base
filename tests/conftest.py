"""Fixtures compartilhadas pelos testes (entregue pelo docente).

Uma fixture é um cenário preparado antes de cada teste e descartado depois.
Aqui, cada teste recebe um banco de dados temporário novo, com 5 produtos e
1 usuário ('tester' / 'senha-de-teste'), sem tocar no banco real do sistema.
"""
import pytest

import dados
import seguranca
from app import create_app


@pytest.fixture(autouse=True)
def hash_rapido(monkeypatch):
    """Reduz as iterações do PBKDF2 nos testes para que a suíte rode rápido."""
    monkeypatch.setattr(seguranca, "ITERACOES", 1_000)


@pytest.fixture
def banco(tmp_path):
    """Caminho de um banco temporário já preparado."""
    caminho = tmp_path / "teste.db"
    dados.criar_estrutura(caminho)
    dados.popular_exemplo(caminho)
    dados.cadastrar_usuario(caminho, "tester", "senha-de-teste")
    return caminho


@pytest.fixture
def app(banco):
    """Aplicação Flask configurada para usar o banco temporário."""
    return create_app({"TESTING": True, "DB_PATH": banco, "SECRET_KEY": "chave-de-teste"})


@pytest.fixture
def cliente(app):
    """Cliente de teste: simula um navegador sem abrir o servidor."""
    return app.test_client()


@pytest.fixture
def cliente_logado(cliente):
    """Cliente que já fez login com o usuário de teste."""
    cliente.post("/login", data={"usuario": "tester", "senha": "senha-de-teste"})
    return cliente
