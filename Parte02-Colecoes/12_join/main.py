# Separador 

import os

os.system("cls" if os.name == "nt" else "clear")


nomes = ["Juleidy","Lorindinalvety"]

print("Nomes disponiveis:")
print("")
print("------------------")
print("")

# Valor que separa os itens na variável:
separador = " "

# Junta os valores em um único valor:
nomes_junto = separador.join(nomes)

# Exibe na tela
print(nomes_junto)

print("")
print("------------------")
print("")