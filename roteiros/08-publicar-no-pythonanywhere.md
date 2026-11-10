# Roteiro 8: publicar o sistema no PythonAnywhere (Aula 8)

**Pré-requisitos:** conta gratuita no PythonAnywhere, repositório do sistema no GitHub (Aula 7) e `requirements.txt` criado e enviado.

> [!warning] Antes de começar
> Confira a página de ajuda do PythonAnywhere sobre Flask (*Setting up Flask applications on PythonAnywhere*): os nomes de menus e as versões do Python disponíveis podem mudar.

## 1. Clonar o repositório

No PythonAnywhere, abra **Consoles > Bash** e execute (troque `SEU-USUARIO` e `SEU-REPOSITORIO`):

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git gestao-produtos
cd gestao-produtos
```

## 2. Criar o ambiente virtual e instalar as dependências

Use a **mesma versão do Python** que você escolherá no passo 4 (exemplo com 3.10):

```bash
mkvirtualenv --python=/usr/bin/python3.10 gestao-venv
pip install -r requirements.txt
```

## 3. Criar o banco e o usuário

```bash
python criar_banco.py
python criar_usuario.py
```

> [!note] O banco não veio do GitHub
> O arquivo `.db` está no `.gitignore`: o banco de produção é criado aqui e **não** se mistura com o do seu computador.

## 4. Criar o aplicativo web

1. Abra a aba **Web** e clique em **Add a new web app**.
2. Escolha **Manual configuration** (não escolha o assistente "Flask") e a mesma versão do Python do passo 2.
3. Em **Virtualenv**, informe `/home/SEU-USUARIO/.virtualenvs/gestao-venv`.
4. Em **Code > Source code**, informe `/home/SEU-USUARIO/gestao-produtos`.

## 5. Configurar o arquivo WSGI

Na seção **Code**, abra o **WSGI configuration file**, apague o conteúdo e use:

```python
import os
import sys

pasta = "/home/SEU-USUARIO/gestao-produtos"
if pasta not in sys.path:
    sys.path.append(pasta)

# Segredo da aplicação: um texto longo e aleatório, só seu. Nunca vai para o GitHub.
os.environ["APP_SECRET"] = "COLE-AQUI-UM-SEGREDO-LONGO-E-ALEATORIO"
os.environ["COOKIE_SECURE"] = "1"   # o site é servido por HTTPS

from app import app as application
```

Para gerar o segredo, no console Bash: `python -c "import secrets; print(secrets.token_hex(32))"`.

## 6. Recarregar e testar

1. Na aba **Web**, clique no botão verde **Reload**.
2. Abra `https://SEU-USUARIO.pythonanywhere.com`.
3. Se aparecer erro, abra o **Error log** (link na aba Web) e leia as últimas linhas.

## 7. Registrar os testes no ambiente publicado

No endereço publicado, execute os casos manuais essenciais e registre-os em `docs/resultados-de-teste.md` com **versão = v1.0.0** e **ambiente = produção**:

- [ ] Login com usuário e senha corretos
- [ ] Login com senha errada é recusado
- [ ] `/produtos/novo` sem login leva ao login
- [ ] Cadastro de um produto válido aparece na lista

## 8. Atualizar depois de uma correção (Aula 9)

No console Bash:

```bash
cd ~/gestao-produtos
git pull
```

Depois, clique em **Reload** na aba **Web** e repita o teste no ar.

## Problemas comuns

| Sintoma | Causa provável | Como corrigir |
| --- | --- | --- |
| `ModuleNotFoundError` no Error log | Virtualenv não configurado na aba Web, ou `requirements.txt` incompleto | Confira o caminho do Virtualenv e rode `pip install -r requirements.txt` |
| `Banco de dados não encontrado` | `criar_banco.py` não foi executado no servidor | Execute o passo 3 |
| Login recusado só às vezes | `APP_SECRET` não definido no arquivo WSGI | Defina o segredo e dê Reload |
| Mudança no código não aparece | Faltou o Reload | Clique em **Reload** |
| Página de erro genérica | Erro no WSGI ou na importação | Leia o **Error log** |
