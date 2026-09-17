# Git Poltergeist v2.0

Aplicativo de Auto Commit com a mesma interface do projeto.

## GitHub

Use o botão **🔐 Entrar no GitHub** dentro do programa para autenticar a conta pelo Git Credential Manager. O login é feito pelo navegador e a credencial é armazenada pelo sistema operacional; o aplicativo não salva a senha/token em `config.json`.

Em cada PC é necessário fazer o login daquela máquina uma vez. A pasta do projeto também pode ser escolhida/salva em cada PC.

O Git para Windows deve estar instalado e disponível no PATH. O Git Credential Manager é o componente usado para a autenticação do GitHub. O push continua sendo feito pelo Git normal.

## Gerar EXE

Execute `build_exe.bat` uma vez. O executável será criado em `dist` com `--windowed`, sem janela CMD.
