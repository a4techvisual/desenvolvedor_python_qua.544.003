class Pessoa:
    # Construtor
    def __init__(self, nome, idade, altura):
        self.nome = nome
        self.idade = idade
        self.altura = altura

    def __str__(self):
        return f"Olá meu nome é {self.nome}, tenho {len(self)} anos e minha altura é {float(self)}metros."

    def __len__(self):
        return self.idade

    def float(self):
        return self.altura

    