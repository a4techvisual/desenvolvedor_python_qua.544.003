import os

from models import Pessoa


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    usuario = Pessoa(nome="", idade=0, altura=0.0)

    usuario.nome = input("Digite seu nome: ")
    usuario.idade = int(input("Digite sua idade: "))
    usuario.altura = float(input("Digite sua altura: ").replace(",", "."))

    limpar()

    print(f"Nome: {usuario.nome}")
    print(f"Idade: {usuario.idade} anos")
    print(f"Altura: {usuario.altura} metros")

    del usuario


if __name__ == "__main__":
    main()


