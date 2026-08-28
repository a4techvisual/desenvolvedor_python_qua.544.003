from models import Carro

def main():
    carro = Carro(modelo="", potencia="")

    carro.modelo = input("Informe o modelo do carro: ").strip().title()
    carro.motor.potencia = input("Informe a potência do motor: ").strip()
    print(carro.detalhes())

    if __name__ == "__main__":
        main()