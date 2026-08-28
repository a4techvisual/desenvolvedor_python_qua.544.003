import os

from models import Pedido


def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    pedido = Pedido(valor1=0.0, valor2=0.0)

    limpar()
    valor1 = float(input("Digite o primeiro valor 1: ").replace(",", "."))
    pedido.valor1 = valor1

    valor2 = float(input("Digite o segundo valor 2: ").replace(",", "."))
    pedido.valor2 = valor2 

    limpar()

    print("1 - Somar")
    print("2 - Subtrair")
    print("3 - Multiplicar")
    print("4 - Dividir")
    operador = input("Digite o número da operação desejada: ")

    resultado = pedido.calcular_total(operador)
    print(f"\nO resultado da operação é: {resultado}")



if __name__ == "__main__":
    main()
