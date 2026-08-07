# Dicionário:
usuario = {
    'nome': "Fulano de tal",
    'idade': 35,
    'email': "fulanodetal@gmail.com",
    'cpf': "123,456,789-12",
    }

# Exibir os dados do dicionário:
print(f"Nome: {usuario['nome']}")
print(f"Idade: {usuario['idade']}")
print(f"Email: {usuario['email']}")
print(f"CPF: {usuario['cpf']}")

# Forma 2:
print(f"Nome: {usuario.get('nome')}")
print(f"Idade: {usuario.get('idade')}")
print(f"Email: {usuario.get('email')}")
print(f"CPF: {usuario.get('cpf')}")

# Forma 3:
for chave in usuario:
    print(f"{chave.capitalize()}:{usuario.get(chave)}")