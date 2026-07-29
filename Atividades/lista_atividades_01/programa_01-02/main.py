# TODO: atividade 02 """Crie um programa que receba uma vez o nome e a idade do usuário, e e, seguida mostre os filmes em idade do usuário, e em seguida mostre os filmes em cartaz em 5 salas de cinema:
# - A volta dos Que não Foram (Livre)
# - A doda Quadra (12 anos)
# - As Tranças do Rei Careca (14 anos)
# - Poreira em Alto Mar (16 anos)
# - AVingança do Frango Assado (18 anos)
# O usuário irá escolher a sla onde o filme desejado está passando. Caso o usuário não tenha idade, o programa impede sua entrada e re-exibe a listapar que o mesmo possa escolher outro filme.
# Caso o usuário tenha a idade minima, o prgrama grama em arquivo o bilhete do filme e encerra o progrma.

# TODO: atividade 02

nome = input("Digite seu nome: ")
idade = int(input("Digite sua idade: "))

while True:
    print("f\nFILMES EM CARTAZ")
    print("1 - A Volta dos Que Não Foram (Livre)")
    print("2 - A Doda Quadra (12 anos)")
    print("3 - As Tranças do Rei Careca (14 anos)")
    print("4 - Poeira em Alto Mar (16 anos)")
    print("5 - A Vingança do Frango Assado (18 anos)")

    sala = int(input("Escolha uma sala: "))

    if sala == 1:
        filme = "A Volta dos Que Não Foram"
        classificacao = 0

    elif sala == 2:
        filme = "A Doda Quadra"
        classificacao = 12

    elif sala == 3:
        filme = "As Tranças do Rei Careca"
        classificacao = 14

    elif sala == 4:
        filme = "Poeira em Alto Mar"
        classificacao = 16

    elif sala == 5:
        filme = "A Vingança do Frango Assado"
        classificacao = 18

    else:
        print("Sala inválida.")
        continue

    if idade >= classificacao:
        print("Entrada permitida!")

        arquivo = open("bilhete_" + nome + ".txt", "w")

        arquivo.write("BILHETE\n")
        arquivo.write("Nome: " + nome + "\n")
        arquivo.write("Filme: " + filme + "\n")
        arquivo.write("Sala: " + str(sala) + "\n")

        arquivo.close()

        print("Bilhete criado!")
        break

    else:
        print("Você não tem idade para esse filme.")
        print("Escolha outro.")