# Plano de teste: sistema Gestão de Produtos

**Versão testada:** _____ · **Ambiente:** (local ou produção) · **Responsáveis:** _____ · **Data:** _____

## 1. Objetivo

Realizar testes iniciais do sistema

## 2. Escopo

- **Será testado:** Acesso ao login e ao cadastro de produtos
- **Não será testado:** Código fonte

## 3. Tipos de teste previstos

| Tipo | Para que funcionalidades | Manual ou automatizado |
| --- | --- | --- |
| Manual | Acessar o cadastro | Manual |

## 4. Casos de teste

| ID | Objetivo | Pré-condição | Passos | Resultado esperado | Resultado obtido | Status | Automatizado? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-01 | Validação do cadastro | fazer login | preencher produto com Preço negativo | erro não cadastrar | erro | passou | manual |
| CT-02 | Acesso restrito | sem login | Abrir /produtos/novo sem login | acesso restrito | erro=restrito | passou | manual |
| CT-03 | Conferir senha | Cadastrar o usuário | Acessar a tela de login | senha inválida | senha inválida | passou | manual |
| CT-04 | Proteção do formulário (CSRF) | Fazer login | Acessar formulário de produto e teclar f12 e apagar o token do formulário | erro | Requisição inválida | passou | manual |
| CT-05 | Exibição de texto | Fazer login | Acessar formulário de produto e cadastrar Produto chamado `<b>teste</b>` | escape html | o html foi exibido | passou | manual |
| CT-06 | Cadastro válido | Fazer login | Acessar formulário de produto e cadastrar Produto Smartv | produto exibido em produtos | o produto foi exibido | passou | manual |

> **Status:** Passou, Falhou ou Bloqueado. **Passos:** escreva de forma que outra pessoa consiga repetir sem perguntar nada.
