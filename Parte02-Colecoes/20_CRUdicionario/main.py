import os

# Criar a lista
usuarios = []

# Limpar a tela
os.system("cls" if os.name == "nt" else "clear")

while True:

    # Menu
    print(f"{'-'*20} CRUDicionário {'-'*20}")
    print("")
    print("1 - Cadastrar novo usuário")
    print("2 - Listar todos os usuários")
    print("3 - Alterar dados de um usuário")
    print("4 - Deletar usuário")
    print("")
    print("5 - Sair do programa")
    print("")
    print(f"{'-'*40}")
    print("")

    opcao = input("Informe a opção desejada: ").strip()
    os.system("cls" if os.name == "nt" else "clear")

    match opcao:
        case "1":
            # cria novo dicionário:
            usuario = {}
            usuario['nome'] = input("Informe o nome: ").strip().title()
            usuario['cpf'] = input("Informe o CPF: ").strip()
            usuario['email'] = input("Informe o email: ").strip().lower()

            # Adiciona dicionário na lista
            usuarios.append(usuario)

            os.system("cls" if os.name == "nt" else "clear")
            continue

        case "2":
            for usuarios in usuarios:
                for chave, valor in usuario.items():
                    print(" ")
                    print(f"{chave.capitalize()}: {valor}")
                    print(" ")
    
            continue

        case "3":
            nome = input("Informe o nome do Usuário a ser pesquisado: ").strip().title()
            print(f"{'-'*40}")

            for usuario in usuarios:
                if nome in usuario['nome']:
                    # 2° menu
                    print(" ")
                    print("- Nome")
                    print("- CPF")
                    print("- Email")
                    print("- Cancelar")
                    print(" ")
                    print(f"{'-'*40}")
                    alterar = input("O que deseja alterar? ").strip().lower()

                    if alterar in usuario:
                        os.system("cls" if os.name == "nt" else "clear")
                        usuario[alterar] = input ("Você deseja alterar para: ").strip()
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Informação Alterada com sucesso!")
                        print(" ")

                else:
                    print(" ")
                    print("Usuário não encontrado.")
                    print(" ")
                    continue
        case "4":
            print(" ")
            nome= input("Informe o nome a ser deletado: ").strip().title()
            print(" ")
            for usuario in usuarios:
                if nome in usuario['nome']:
                    usuario.remove(usuario)
                    os.system("cls" if os.name == "nt" else "clear")
                    print(" ")
                    print("Usuário deletado com sucesso!")
                    print(" ")
                else:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(" ")
                    print("Usuário não encontrado!")
                    print(" ")
            
        case "5":
            os.system("cls" if os.name == "nt" else "clear")
            print("Encerrando o programa...")
            break
        case _:
            print("Opçõao invalida.")
            continue