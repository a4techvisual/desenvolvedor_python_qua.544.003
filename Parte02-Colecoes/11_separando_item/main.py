# Separando itens e salvando eles em uma variavel:
import os

os.system("cls" if os.name == "nt" else "clear")

nomes = ["Fulano","Alex","Eduardo","Cicrano","Beltrano","Lorindinalvety"]

print("Nomes disponiveis:")
print("")
print("------------------")
print("")

for nome in nomes:
    print(nome)

print("")
print("------------------")
print("")


nome = input("Informe o nome a ser separado: ").strip().title()

if nome in nomes: # Esse comando serve para se o nome está na lista nomes, vai retornar a lista de indice.
    indice = nomes.index(nome)

    # separar o nome da lista:

    nome_separado = nomes.pop(indice)
    os.system("cls" if os.name == "nt" else "clear")

    # exibe a lista:

    print("Lista atualizada:")
    print("")
    print("------------------")
    print("")

    for nome in nomes:
        print(nome)

    print("")
    print("------------------")
    print("")
    
    print(f"O nome ({nome_separado}) foi separado da lista.")

else:
    print("Nome não encontrado.")