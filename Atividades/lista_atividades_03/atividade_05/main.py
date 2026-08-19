# TODO: atividade 05
# Usando recursividade, crie um programa onde o usuário informa um número inteiro e o programa calcula a sequência de Fibonacci até o número informado.

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


numero = int(input("Informe um número inteiro: "))

print("Sequência de Fibonacci:")

for i in range(numero):
    print(fibonacci(i), end=" ")