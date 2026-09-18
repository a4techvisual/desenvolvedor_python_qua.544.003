# Git Poltergeist v2.0 — versão corrigida

## O que foi corrigido

- Login do GitHub corrigido para usar o Git Credential Manager atual.
- Logout corrigido: versões atuais do GCM exigem o nome da conta.
- Seleção de conta do GitHub quando existem várias contas autenticadas.
- A conta escolhida fica salva e pode ser aplicada ao repositório atual.
- Login usa o navegador (`--browser`) em vez de depender de prompt no CMD.
- Interface reorganizada com `grid` para evitar texto cortado/sobreposto ao redimensionar.
- Botão **⚙ Configurações** adicionado.
- O **Commit programado** que já existia fica pré-selecionado.
- É possível trocar para tipos de commit como `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci` e `revert`.
- O histórico real dos últimos 100 commits do repositório pode ser consultado dentro do programa.
- As configurações ficam salvas em `%APPDATA%\GitPoltergeist\config.json`.
- O programa continua sem abrir janelas de CMD durante Git/GCM.

## Login do GitHub

O aplicativo usa o Git Credential Manager (GCM), que é o mecanismo recomendado para autenticação do Git no Windows. O GCM atual possui os comandos `github list`, `github login` e `github logout <conta>`.

Para o login funcionar no computador, mantenha o Git for Windows atualizado e com o Git Credential Manager instalado/configurado.

## Como usar

1. Execute `CRIAR_EXE.vbs` para gerar um novo EXE.
2. Depois abra `dist\Git Poltergeist v2.0.exe`.
3. Se o GitHub aparecer como **não conectado**, clique em **Entrar no GitHub**.
4. Faça login no navegador.
5. Abra **⚙ Configurações** se quiser mudar o tipo de commit.
6. Clique em **Executar Commit**.

## Tipos de commit disponíveis

- **Commit programado** — padrão que já existia no seu projeto.
- **feat** — nova funcionalidade.
- **fix** — correção de bug.
- **docs** — documentação.
- **style** — formatação/estilo.
- **refactor** — refatoração.
- **test** — testes.
- **chore** — manutenção.
- **perf** — desempenho.
- **build** — build/dependências.
- **ci** — integração contínua.
- **revert** — reversão.

A tela de configurações usa marcação visual de uma opção por vez para evitar que dois tipos diferentes sejam usados no mesmo commit.

## Importante sobre o EXE

O arquivo ZIP enviado anteriormente continha um EXE antigo. Como o ambiente desta conversa não tem PyInstaller instalado, eu validei e corrigi o código-fonte, mas não consigo afirmar que um novo EXE foi compilado aqui.

No seu PC, execute `CRIAR_EXE.vbs` para gerar o EXE atualizado.
