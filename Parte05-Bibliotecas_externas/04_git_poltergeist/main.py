import pyautogui as auto
import pyperclip
from datetime import date


def hoje():
    return date.today().strftime("%d/%m/%Y")


def digitar(texto):
    pyperclip.copy(texto)
    auto.hotkey("ctrl", "v")


def main():
    auto.PAUSE = 0.75

    # Abre o Git Bash
    auto.press("win")
    auto.write("git bash")
    auto.press("enter")
    auto.sleep(10)

    # Volta para /c/Users
    auto.write("cd ..")
    auto.press("enter")
    auto.sleep(1)

    # Entra na pasta do projeto
    digitar('cd "/c/Users/ALUNO/Rômulo Delalíbera Júnior/desenvolvedor_python_qua.544.003"')
    auto.press("enter")
    auto.sleep(2)

    # Adiciona os arquivos
    auto.write("git add .")
    auto.press("enter")
    auto.sleep(2)

    # Faz o commit
    digitar(f'git commit -m "Commit {hoje()}"')
    auto.press("enter")
    auto.sleep(2)


if __name__ == "__main__":
    main()
