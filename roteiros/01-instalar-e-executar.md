# Roteiro 1: instalar e executar o sistema (Aula 1)

**Tempo estimado:** 40 minutos · **Em duplas** · **Resultado:** sistema rodando em `http://127.0.0.1:5000`

## 1. Preparar a pasta

1. Extraia o arquivo `gestao-produtos-base.zip` em uma pasta sua (evite pastas com espaços ou acentos no caminho).
2. Abra a pasta no VS Code (**File > Open Folder**) e abra o terminal integrado (**Terminal > New Terminal**).
3. Confirme que está na pasta certa: o comando `python --version` deve mostrar o Python 3.10 ou superior e a pasta deve conter `app.py`.

## 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente:

| Sistema | Comando |
| --- | --- |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Linux e macOS | `source .venv/bin/activate` |

O terminal passa a mostrar `(.venv)` no início da linha.

## 3. Instalar as dependências

```bash
pip install flask pytest pytest-cov
```

## 4. Criar o banco e o usuário

```bash
python criar_banco.py
python criar_usuario.py
```

O segundo comando pede o nome do usuário e a senha (mínimo de 8 caracteres). A senha não aparece enquanto você digita.

## 5. (Recomendado) Definir o segredo da aplicação

O segredo assina o cookie de sessão. Sem ele, o sistema usa um valor temporário e **você será deslogado toda vez que o servidor reiniciar**.

| Sistema | Comando |
| --- | --- |
| Windows (PowerShell) | `$env:APP_SECRET = "troque-por-um-texto-longo-e-aleatorio"` |
| Linux e macOS | `export APP_SECRET="troque-por-um-texto-longo-e-aleatorio"` |

## 6. Executar

```bash
flask --app app run --debug
```

Abra `http://127.0.0.1:5000` no navegador e entre com o usuário criado. Para parar o servidor, use `Ctrl + C`.

## 7. Conferir

- [ ] A tela de login abriu
- [ ] O login funciona e a lista mostra 5 produtos
- [ ] `pytest` roda sem erro (ainda não há testes: a mensagem esperada é `no tests ran`)

## Problemas comuns

| Sintoma | Causa provável | Como corrigir |
| --- | --- | --- |
| `python` não é reconhecido | Python fora do PATH | Tente `py` (Windows) ou `python3` |
| `No module named flask` | Ambiente virtual não ativado | Ative o `.venv` e rode o `pip install` |
| `Banco de dados não encontrado` | `criar_banco.py` não foi executado | Execute o passo 4 |
| Login sempre recusado | Usuário não criado ou senha diferente | Rode `criar_usuario.py` com outro nome |
| Deslogado a cada alteração no código | `APP_SECRET` não definido | Execute o passo 5 |
| Erro de permissão ao ativar o ambiente (PowerShell) | Política de execução | Use o terminal **Command Prompt** ou peça ajuda ao docente |
