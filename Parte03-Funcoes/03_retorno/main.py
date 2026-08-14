def  boas_vindas(nome):
    return f"Seja bem vindo {nome}."


# algorítimo principal
nome = input("Informe seu nome: ").strip().title()
print(boas_vindas(nome))
