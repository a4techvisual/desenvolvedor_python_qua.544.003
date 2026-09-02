import os
import pyjokes
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound


def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')


def gerar_piada():
    tradutor = GoogleTranslator(source='en', target='pt')
    piada = pyjokes.get_joke(language='en', category='all')

    try:
        return tradutor.translate(piada)
    except TranslationNotFound:
        return piada


def main():
    limpar()

    while True:
        print("0 - Sair do programa")
        print("1 - Gerar uma piada")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Saindo do programa...")
            break

        elif opcao == "1":
            nova_piada = gerar_piada()
            print("\n" + nova_piada + "\n")

        else:
            print("Opção inválida, tente novamente.\n")


if __name__ == "__main__":
    main()
