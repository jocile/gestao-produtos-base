"""Sistema Gestão de Produtos (Flask): login, lista e cadastro de produtos."""
import functools
import hmac
import os
import secrets
import sqlite3
from datetime import timedelta

from flask import Flask, abort, redirect, render_template, request, session, url_for

import dados
from seguranca import verificar_senha
from validacao import validar_produto

# A URL carrega apenas um código; a mensagem real fica no servidor
MENSAGENS = {
    "restrito": "Acesso restrito. Faça login para continuar.",
    "invalido": "Usuário ou senha incorretos.",
    "saiu": "Sessão encerrada.",
}
AVISOS = {"cadastrado": "Produto cadastrado com sucesso."}
CAMPOS_PRODUTO = ("nome", "preco", "estoque", "id_categoria")


def login_required(view):
    """Bloqueia a rota se não houver usuário na sessão."""
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("exibir_login", erro="restrito"))
        return view(*args, **kwargs)
    return wrapper


def emitir_token_csrf() -> str:
    """Gera um token aleatório, guarda na sessão e devolve para o formulário."""
    token = secrets.token_hex(16)
    session["csrf"] = token
    return token


def token_csrf_valido() -> bool:
    """Confere se o token do campo oculto é igual ao da sessão."""
    esperado = session.get("csrf")
    recebido = request.form.get("csrf_token", "")
    if not esperado:
        return False
    return hmac.compare_digest(esperado.encode("utf-8"), recebido.encode("utf-8"))


def create_app(config: dict | None = None) -> Flask:
    """Cria a aplicação. Os testes passam uma 'config' própria (banco temporário)."""
    app = Flask(__name__)
    app.config.update(
        # Sem APP_SECRET, usa-se um segredo temporário (sessões caem a cada reinício)
        SECRET_KEY=os.environ.get("APP_SECRET") or secrets.token_hex(32),
        DB_PATH=os.environ.get("DB_PATH") or dados.DB_PADRAO,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE") == "1",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
    )
    if config:
        app.config.update(config)

    def banco():
        return app.config["DB_PATH"]

    # ------------------------------------------------------------ autenticação
    @app.get("/login")
    def exibir_login():
        mensagem = MENSAGENS.get(request.args.get("erro", ""), "")
        return render_template("login.html", mensagem=mensagem)

    @app.post("/login")
    def processar_login():
        login = (request.form.get("usuario") or "").strip()
        senha = request.form.get("senha") or ""  # senha nunca recebe strip()

        registro = dados.buscar_usuario(banco(), login)
        if registro and verificar_senha(senha, registro["senha_hash"], registro["salt"]):
            session.clear()
            session["usuario"] = registro["login"]
            session.permanent = True
            return redirect(url_for("listar"))
        return redirect(url_for("exibir_login", erro="invalido"))

    @app.get("/logout")
    def logout():
        session.clear()
        return redirect(url_for("exibir_login", erro="saiu"))

    # ---------------------------------------------------------------- produtos
    @app.get("/")
    def inicio():
        return redirect(url_for("listar"))

    @app.get("/produtos")
    @login_required
    def listar():
        aviso = AVISOS.get(request.args.get("ok", ""), "")
        return render_template("produtos.html", produtos=dados.listar_produtos(banco()), aviso=aviso)

    @app.get("/produtos/novo")
    @login_required
    def exibir_formulario():
        return render_template(
            "produto_form.html",
            valores={}, erros={},
            categorias=dados.listar_categorias(banco()),
            csrf_token=emitir_token_csrf(),
        )

    @app.post("/produtos")
    @login_required
    def cadastrar_produto():
        if not token_csrf_valido():
            abort(403, "Requisição inválida. Recarregue o formulário e tente novamente.")

        campos = {c: request.form.get(c, "") for c in CAMPOS_PRODUTO}
        categorias = dados.listar_categorias(banco())
        ids_validos = {c["id_categoria"] for c in categorias}

        dados_produto, erros = validar_produto(campos, ids_validos)

        if not erros:
            try:
                dados.inserir_produto(banco(), **dados_produto)
            except sqlite3.IntegrityError:
                erros["geral"] = "O banco de dados recusou os dados informados."

        if erros:
            pagina = render_template(
                "produto_form.html",
                valores=campos, erros=erros, categorias=categorias,
                csrf_token=emitir_token_csrf(),
            )
            return pagina, 400

        return redirect(url_for("listar", ok="cadastrado"))

    return app


app = create_app()

if __name__ == "__main__":
    # debug só em desenvolvimento: DEBUG=1 python app.py
    app.run(debug=os.environ.get("DEBUG") == "1")
