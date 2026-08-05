nomes = [
    "Fulano",
    "Cicrano",
    "Beltrano",
    "João",
    "Maria",
    "José",
    "Esmeralda",
]

nome = input("Informa o nome a ser deltado: ").strip().title()

if nome in nomes:
    indice = nomes.index(nome)

#apaga item da lista
    del(nomes[indice])

# exibe a nova lista sem o item deletado
    for nome in nomes:
        print(nome)
else:
    print("Nome não encontrado.")
