import os
import datetime
from datetime import date

from models import Pessoa, Conta


def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def hoje():
    return date.today().strftime("%d/%m/%Y")

def agora():
    return datetime.datetime.now().strftime("%H:%M:%S")

def main():
    titular = Pessoa(nome="",cpf="")
    cc = Conta(titular=titular,agencia="1234-5",n_conta="10123-4",saldo=0.0)

    limpar()

    cc.titular.nome = input("Informe o nome do titular da conta: ").strip().title()
    cc.titular.cpf = input("Informe o CPF do titular da conta: ").strip()

    limpar()
    print(f"Conta criada no dia {hoje()} às {agora()}.")

    while True:
        print("0 - Sair do programa")
        print("1 - Consultar dados da conta")
        print("2 - Fazer depósito")
        print("3 - Fazer saque")
        print("4 - Gerar extrato")
        opcao = input("Informe a opção desejada: ").strip()
        limpar()
        match opcao:
            case "0":
                print("Programa encerrado.")
                break
            case "1":
                print(f"Data da consulta: {hoje()}")
                print(f"Hora da consulta: {agora()}")
                cc.consultar_dados()
                continue
            case "2":
                valor = float(input("Informe o valor a ser depositado: R$ ").replace(",","."))
                if valor >= 0:
                    print(f"Depósito efetuado com sucesso, às {agora()} do dia {hoje()}.")
                    print(f"Saldo atual: R$ {cc.depositar(valor):.2f}")
                else:
                    print("Depósito não pôde ser efetuado.")
                continue
            case "3":
                valor = float(input("Informe o valor do saque: R$ ").replace(",","."))
                if valor >= 0:
                    if valor <= cc.saldo:
                        print(f"Saque efetuado com sucesso às {agora()} do dia {hoje()}.")
                        print(f"Saldo atual: R$ {cc.sacar(valor):.2f}")
                    else:
                        print("Saldo insuficiente.")
                else:
                    print("Valor não pode ser sacado.")
                continue
            case "4":
                cc.gerar_extrato()
                print(f"Extrato gerado com sucesso no arquivo extrato.txt, às {agora()} do dia {hoje()}.")
                continue
            case _:
                print("Opção inválida.")
                continue


if __name__ == "__main__":
    main()
