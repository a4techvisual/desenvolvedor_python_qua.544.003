# TODO: atividade 04
# Utilizando o conceito de módulo, crie um módulo com funções que façam as seguintes ações:
# - limpa o terminal.
# - Calcula a potência de um número informado pelo usuário elevado
#  a outro número informado pelo usuário.
# - Calcula a raíz quadrada de um número informado pelo usuário.
# - Calcula o volume de um recipiente paralelepípidico.
# - Calcula o volume de um recipiente cilíndrico.
# Em seguida, faça um programa que o usuário escolha executar uma dessas funções ou sair do programa.


import math
import os


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def potencia(base, expoente):
    return base ** expoente


def raiz_quadrada(numero):
    return math.sqrt(numero)


def volume_paralelepipedo(comprimento, largura, altura):
    return comprimento * largura * altura


def volume_cilindro(raio, altura):
    return math.pi * (raio ** 2) * altura


# Algoritmo principal
limpar()

while True:
    print("1 - Calcular potência")
    print("2 - Calcular raiz quadrada")
    print("3 - Calcular volume do paralelepípedo")
    print("4 - Calcular volume do cilindro")
    print("5 - Sair do programa")

    opcao = input("Informe a opção desejada: ").strip()

    limpar()

    match opcao:
        case "1":
            base = float(input("Informe a base: ").replace(",", "."))
            expoente = float(input("Informe o expoente: ").replace(",", "."))

            print(f"Resultado: {potencia(base, expoente)}")

        case "2":
            numero = float(input("Informe o número: ").replace(",", "."))

            if numero < 0:
                print("Não é possível calcular a raiz de um número negativo.")
            else:
                print(f"Resultado: {raiz_quadrada(numero)}")

        case "3":
            comprimento = float(
                input("Informe o comprimento: ").replace(",", ".")
            )
            largura = float(
                input("Informe a largura: ").replace(",", ".")
            )
            altura = float(
                input("Informe a altura: ").replace(",", ".")
            )

            print(
                f"Volume do paralelepípedo: "
                f"{volume_paralelepipedo(comprimento, largura, altura)}"
            )

        case "4":
            raio = float(input("Informe o raio: ").replace(",", "."))
            altura = float(input("Informe a altura: ").replace(",", "."))

            print(
                f"Volume do cilindro: "
                f"{volume_cilindro(raio, altura):.2f}"
            )

        case "5":
            print("Programa encerrado.")
            break

        case _:
            print("Opção inválida.")

    if opcao != "5":
        input("\nPressione ENTER para continuar...")
        limpar()