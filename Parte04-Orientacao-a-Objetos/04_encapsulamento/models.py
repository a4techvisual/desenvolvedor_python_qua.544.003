class Pessoa:
    
    def __init__(self,nome,cpf,email,telefone):
    # atributos
        self.__nome = nome # public
        self.__cpf = cpf # protected
        self.__email = email # private
        self.__telefone = telefone # public

    # métodos de acesso

    # GET e SET do nome
        @property
        def nome(self):
            return self.__nome
    
        @nome.setter
        def nome(self, nome):
            self.__nome = nome

    # GET e SET do CPF
        @property
        def cpf(self):
            return self.__cpf

        @cpf.setter
        def cpf(self, cpf):
            self.__cpf = cpf

    # GET e SET do email
        @property
        def email(self):
            return self.__email

        @email.setter
        def email(self, email):
            self.__email = email

    # GET e SET do telefone
        @property
        def telefone(self):
            return self.__telefone

        @telefone.setter
        def telefone(self, telefone):
            self.__telefone = telefone

            
class Pessoa:

    def __init__(self, nome, cpf, email, telefone):

        # atributos privados
        self.__nome = nome
        self.__cpf = cpf
        self.__email = email
        self.__telefone = telefone

  

