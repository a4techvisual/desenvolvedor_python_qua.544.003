# Alterar chave:

usuario = {
    'nome': "Fulano de tal",
    'idade': 35,
    'email': "fulanodetal@gmail.com",
    'cpf': "123,456,789-12",
    }

# Alterando a chave escolhida pelo usuario:
chave = input("Informe o nome da chave: ").strip().lower()

if chave in usuario:
    #usuário informa o novo valor para a chave
    usuario[chave] = input(f"Informe o novo valor para {chave}: ").strip()
else:

    # exibe o dicionário com o novo valor  da chave escolhida
    for chav, valor in usuario.items():
        print(f"{chave.capitalize()}: {valor}")
    else:
        print("Chave não encotrada.")
