class Departamento:
    def __init__(self, nome):
        self.nome = nome

    @property
    def nome(self):
        return self.__nome


    @nome.setter
    def nome(self, nome):
        self.__nome = nome

class Empresa   :
    def __init__(self, nome, departamento):
        self.nome = nome
        self.departamento = departamento

        @property
        def nome(self):
            return self.__nome


        @nome.setter
        def nome(self, nome):
            self.__nome = nome

        @property
        def departamento(self):
            return self.__departamento

        @departamento.setter
        def departamento(self, departamento):
            self.__departamento = departamento

        def detalhes(self):
            return f"Nome: {self.nome}\nDepartamento: {self.departamento.nome}"