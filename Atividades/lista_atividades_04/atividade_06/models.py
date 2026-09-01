import datetime
from datetime import date

from abc import ABC, abstractmethod


class IConta(ABC):
    @abstractmethod
    def consultar_dados():
        pass

    @abstractmethod
    def gerar_extrato():
        pass

    @abstractmethod
    def depositar(valor):
        pass

    @abstractmethod
    def sacar(valor):
        pass


class Pessoa:
    def __init__(self,nome,cpf):
        self.__nome = nome
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self,nome):
        self.__nome = nome

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self,cpf):
        self.__cpf = cpf

    # método especial
    def __str__(self):
        return f"{self.__nome}, CPF: {self.__cpf}"


class Conta(IConta):
    def __init__(self,titular,agencia,n_conta,saldo):
        self.__titular = titular
        self.__agencia = agencia
        self.__n_conta = n_conta
        self.__saldo = saldo
        self.__movimentacoes = []

    @property
    def titular(self):
        return self.__titular

    @titular.setter
    def titular(self,titular):
        self.__titular = titular

    @property
    def agencia(self):
        return self.__agencia

    @agencia.setter
    def agencia(self,agencia):
        self.__agencia = agencia

    @property
    def n_conta(self):
        return self.__n_conta

    @n_conta.setter
    def n_conta(self,n_conta):
        self.__n_conta = n_conta

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self,saldo):
        self.__saldo = saldo

    # métodos da interface
    def consultar_dados(self):
        print(f"Titular da conta: {self.__titular}")
        print(f"Agência da conta: {self.__agencia}")
        print(f"Número da conta: {self.__n_conta}")
        print(f"Saldo da conta: R$ {self.__saldo:.2f}")

    def gerar_extrato(self):
        data = date.today().strftime("%d/%m/%Y")
        hora = datetime.datetime.now().strftime("%H:%M:%S")

        with open("extrato.txt","w",encoding="utf-8") as f:
            f.write("EXTRATO DA CONTA\n")
            f.write(f"{'-'*40}\n")
            f.write(f"Titular da conta: {self.__titular}\n")
            f.write(f"Agência da conta: {self.__agencia}\n")
            f.write(f"Número da conta: {self.__n_conta}\n")
            f.write(f"Emitido em {data} às {hora}\n")
            f.write(f"{'-'*40}\n")

            for movimentacao in self.__movimentacoes:
                f.write(f"Data: {movimentacao['data']} às {movimentacao['hora']}\n")
                f.write(f"Tipo: {movimentacao['tipo']}\n")
                f.write(f"Valor: R$ {movimentacao['valor']:.2f}\n")
                f.write(f"Saldo: R$ {movimentacao['saldo']:.2f}\n")
                f.write(f"{'-'*40}\n")

            f.write(f"Saldo atual: R$ {self.__saldo:.2f}\n")

    def depositar(self,valor):
        self.__saldo += valor

        movimentacao = {}
        movimentacao['data'] = date.today().strftime("%d/%m/%Y")
        movimentacao['hora'] = datetime.datetime.now().strftime("%H:%M:%S")
        movimentacao['tipo'] = "Depósito"
        movimentacao['valor'] = valor
        movimentacao['saldo'] = self.__saldo
        self.__movimentacoes.append(movimentacao)

        return self.__saldo

    def sacar(self,valor):
        self.__saldo -= valor

        movimentacao = {}
        movimentacao['data'] = date.today().strftime("%d/%m/%Y")
        movimentacao['hora'] = datetime.datetime.now().strftime("%H:%M:%S")
        movimentacao['tipo'] = "Saque"
        movimentacao['valor'] = valor
        movimentacao['saldo'] = self.__saldo
        self.__movimentacoes.append(movimentacao)

        return self.__saldo
