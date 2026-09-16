# Git Poltergeist v2.0 — Auto Commit

Agora o programa memoriza a pasta do projeto.

## Como funciona

**Primeira execução:**
1. Clique no ícone.
2. Se a pasta padrão não existir, selecione a pasta do projeto uma vez.
3. A pasta é salva automaticamente.

**Próximas execuções:**
- Basta clicar no ícone.
- O programa abre e executa automaticamente:
  - `git add .`
  - `git commit -m "Commit DD/MM/AAAA"`
  - `git push origin <branch>`

Não é necessário selecionar a pasta novamente.

## Mudar a pasta

A qualquer momento, use o botão **📁 Mudar pasta**.
A nova pasta passa a ser a pasta salva para as próximas execuções.

## Link do GitHub

O programa lê automaticamente o `origin` do repositório e mostra o link real do GitHub no rodapé e no console. O link também pode ser clicado para abrir no navegador.

## EXE

Execute `build_exe.bat` para gerar o executável com o ícone de `image/image.ico`.

A autenticação do GitHub continua sendo feita pelo Git instalado no Windows.
