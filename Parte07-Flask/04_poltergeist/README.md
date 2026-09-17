# Git Poltergeist v2.0

Aplicativo de Auto Commit mantendo a interface e a estrutura do projeto.

## O que mudou

- O programa **não executa o commit automaticamente ao abrir**.
- O commit só acontece quando você aperta **▶ Executar Commit**.
- O botão **🔐 Entrar no GitHub** continua disponível.
- Ao abrir o programa, ele verifica se já existe autenticação do GitHub nesta máquina.
- O status mostra **✓ conectado** ou **⚠ não conectado**.
- A autenticação usa o Git Credential Manager e não salva senha/token no `config.json`.
- Os processos do Git/GCM são executados sem janela CMD.
- O EXE deve ser gerado com `--windowed`, portanto não abre uma janela de console.

## GitHub já conectado

Se o Git Credential Manager já tiver uma conta do GitHub autenticada nesta máquina, o programa identifica isso ao abrir. Não é necessário fazer login novamente.

## Gerar EXE sem CMD

Execute `build_exe.bat` uma vez. O executável será criado em `dist` com `--windowed`.

Para uso normal, abra **Git Poltergeist v2.0.exe**. O `executar.bat` usa `pythonw.exe` para iniciar o programa sem manter um console aberto.
