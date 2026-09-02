from deep_translator import GoogleTranslator

import os

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def traduzir_texto(texto): 
        tradutor = GoogleTranslator(source='auto', target='pt')
        return tradutor.translate(texto)

def main():
    limpar()
    while True:
         print("0 - Sair")
         print("1 - Traduzir texto para português")
         opçao = input("Escolha uma opção: ").strip()
         limpar()

         if opçao == "0":
          break
         elif opçao == "1":
          texto = input("Digite o texto a ser traduzido: ")
          limpar()
          print(traduzir_texto(texto))
          continue
         else:
           print("Opção inválida. Tente novamente.")
           continue


if __name__ == "__main__":
    main()