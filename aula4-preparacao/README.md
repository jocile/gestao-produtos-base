# Alterações para a Aula 4

## Passos para executar os testes

1. Cópia limpa. Em uma pasta separada, junte o app.py, o dados.py e o validacao.py, com os testes da SA1 passando.
2. Rode o script nessa pasta:

   ```powershell
   python gerar_versao_0_9.py
   ```

   Esperado: ok: validacao.py, ok: dados.py, ok: app.py e Versão 0.9 gerada em ....

3. Confira o validacao.py gerado contra o arquivo da v0.9 que você enviou antes (ajuste o caminho do segundo arquivo):

   ```powershell
   fc versao-0.9\validacao.py C:\caminho\do\validacao-antigo.py
   ```

Esperado: FC: nenhuma diferença encontrada.

4. Valide a suíte. Copie os 3 arquivos de versao-0.9/ para uma cópia do projeto (sem o test_rascunho_banco_real.py) e rode pytest -v --tb=short. Esperado: 17 testes, 13 passam e 4 falham, como no gabarito. Se a sua contagem for diferente, cole a saída aqui.
5. Entregue aos alunos só a pasta versao-0.9/, sem o script.

O que cada alteração faz no seu código:

| Defeito | Arquivo | Efeito observável |
| --------- | --------- | ------------------- |
| 1. Preço negativo | validacao.py | A validação deixa passar. O banco ainda recusa por causa do CHECK(preco >= 0.0). O app captura o IntegrityError e devolve 400 com “O banco de dados recusou os dados informados.”, e não a mensagem de preço inválido. Nada inválido é gravado |
| 2. Venda sem baixa | dados.py | registrar_venda não levanta erro, grava a venda e deixa o estoque igual |
| 3. Sem login | app.py | GET /produtos/novo devolve 200 sem sessão. O POST /produtos continua protegido por login_required e CSRF |

A linha do defeito 1 vem da nota produtos-06, e não vi o seu validacao.py. Se o seu código estiver diferente, o script para com trecho encontrado 0 vez(es). Nesse caso, cole aqui o validacao.py e eu ajusto a troca.

Antes de entregar a pasta, copie os 3 arquivos para uma cópia do projeto e rode pytest -v. Os números do gabarito da Aula 4 (3 falhas em 13) continuam valendo só para a suíte básica. No seu repositório há também o rascunho e os testes opcionais, então as contagens serão diferentes.
