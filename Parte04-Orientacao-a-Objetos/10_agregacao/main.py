import os

from models import Departamento, Empresa

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
   departamento = Departamento(nome="")
   empresa = Empresa(nome="", departamento=departamento)

   limpar()

   empresa.nome = input("Digite o nome da empresa: ")
   empresa.departamento.nome = input("Digite o nome do departamento: ")

   limpar()
   print(empresa.detalhes())
   


if __name__ == "__main__":
    main()