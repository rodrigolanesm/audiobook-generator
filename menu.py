"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 24/03/2024 - 16:52:31
Linguagem: Python

Descrição: Menu inicial

"""

import pyttsx3
from leitor_arquivos import LeitorArquivos

class Menu:
    def __init__(self):
        self.engine = pyttsx3.init()

    def falar(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()

    def exibir_menu(self):
        while True:
            print("Escolha o tipo de arquivo:")
            print("1. EPUB")
            print("2. DOCX")
            print("3. PDF")
            print("4. MOBI")
            print("5. Sair")
            opcao = input("Digite o número da opção desejada: ")
            
            if opcao == "5":
                print("Saindo do programa...")
                break
            
            if opcao not in ["1", "2", "3", "4"]:
                print("Opção inválida. Por favor, escolha uma das opções disponíveis.")
                continue
            
            tipo_arquivo = LeitorArquivos.extensoes[int(opcao) - 1]
            arquivo = input(f"Digite o nome do arquivo ({tipo_arquivo}): ")

            if opcao == "1":
                texto = LeitorArquivos.extrair_texto_epub(arquivo, 1000)
                print("Texto extraído do arquivo EPUB:")
                print(texto)
                self.falar(texto)
            elif opcao == "2":
                texto = LeitorArquivos.extrair_texto_docx(arquivo, 1000)
                print("Texto extraído do arquivo DOCX:")
                print(texto)
                self.falar(texto)
            elif opcao == "3":
                texto = LeitorArquivos.extrair_texto_pdf(arquivo, 1000)
                print("Texto extraído do arquivo PDF:")
                print(texto)
                self.falar(texto)
            elif opcao == "4":
                texto = LeitorArquivos.extrair_texto_mobi(arquivo, 1000)
                print("Texto extraído do arquivo MOBI:")
                print(texto)
                self.falar(texto)

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
