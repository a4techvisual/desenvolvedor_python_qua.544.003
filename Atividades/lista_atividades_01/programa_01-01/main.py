# TODO: atividade 01
"""
Crie um programa que receba o nome, peso e altura do usuário e informe na tela o seu IMC o seu siagnóstico com base no valor do IMC.
"""
# Entrada de dados
nome = input("Digite seu nome: ")
peso = float(input("Digite seu peso (kg): ").replace(",", "."))
altura = float(input("Digite sua altura (m): ").replace(",", "."))

# Cálculo do IMC
imc = peso / (altura ** 2)

# Diagnóstico
if imc < 18.5:
    diagnostico = "Abaixo do peso"
elif imc < 25:
    diagnostico = "Peso normal"
elif imc < 30:
    diagnostico = "Sobrepeso"
elif imc < 35:
    diagnostico = "Obesidade Grau I"
elif imc < 40:
    diagnostico = "Obesidade Grau II"
else:
    diagnostico = "Obesidade Grau III"

# Saída de dados
print("\n===== RESULTADO =====")
print(f"Nome: {nome}")
print(f"IMC: {imc:.2f}")
print(f"Diagnóstico: {diagnostico}")
