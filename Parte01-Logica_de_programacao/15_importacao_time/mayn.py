# importação de bibliotecas
import os
import time

# tratamento de excessão
try:
    # entrada de dados
    n =int(input("Informe um número inteiro: "))

    # limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # contagem
    while n >= 0:
        print(f"{n}...")
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        n -= 1

    print("BOOOOOOOOOOOOOO!!!!! 🧨🧨")

except Exception  as e:
    print(f"Não foi possível iniciar a contagem. {e}.")
