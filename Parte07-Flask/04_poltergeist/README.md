# Git Poltergeist v2.0 — ZERO CMD

Esta versão foi preparada para o uso normal **sem nenhuma janela CMD**.

## Como usar

1. Na primeira vez, execute `CRIAR_EXE.vbs` para gerar o executável.
2. Depois abra diretamente:
   `dist\Git Poltergeist v2.0.exe`
3. Para uso diário, crie um atalho desse `.exe` na Área de Trabalho e coloque o ícone `image\image.ico` no atalho.
4. Não use `executar.bat`: ele foi removido desta versão justamente para evitar a abertura do CMD.

Também é possível abrir `executar.vbs`; ele inicia o EXE de forma oculta, sem console.

## Comportamento

- Ao abrir o programa, o Auto Commit é executado automaticamente.
- O botão `▶ Executar Commit` permite executar novamente quando você quiser.
- A pasta do projeto fica salva.
- O GitHub é verificado automaticamente.
- Se já houver uma conta autenticada nesta máquina, ela é identificada.
- O botão do GitHub fica dinâmico: entrar, trocar conta ou deslogar.
- Git, Git Credential Manager e o navegador são chamados sem janela de console.
- O link do remote do GitHub aparece dentro da interface.

## Importante sobre o EXE

O executável final é criado com PyInstaller em modo `--windowed/--noconsole`. Esse é o modo próprio para aplicações gráficas do Windows sem console.

Para usar o programa em outro PC, gere/leve o EXE e tenha o Git para Windows instalado. A autenticação do GitHub precisa ser feita separadamente em cada PC.
