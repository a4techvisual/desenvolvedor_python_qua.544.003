# Git Poltergeist v2.0

## Como abrir sem CMD

Use **executar.vbs** para abrir o programa sem janela preta do CMD.
Se o EXE já tiver sido gerado em `dist`, o VBS abre o EXE. Se não houver EXE, ele tenta abrir `main.pyw` usando `pythonw.exe`, também sem console.

Para gerar o EXE definitivo no Windows, execute `build_exe.bat` uma vez. Depois use `dist\Git Poltergeist v2.0.exe` ou `executar.vbs`.

## Funcionamento
- Ao abrir, carrega a pasta salva e executa o Auto Commit automaticamente.
- O botão **▶ Executar Commit** permite repetir o processo manualmente quando quiser.
- O botão do GitHub verifica a autenticação já existente nesta máquina.
- Quando conectado, ele mostra a conta e oferece **Trocar conta** e **Deslogar**.
- Git e Git Credential Manager são executados sem abrir janelas de console.

## Importante
O login do GitHub é por computador. Em outro PC, é necessário autenticar a conta naquele PC.
