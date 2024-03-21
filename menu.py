"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 21/03/2024 - 17:23:47
Linguagem: Python

Descrição: Menu inicial

"""

from leitor_arquivos import LeitorArquivos

class Menu:

    def exibir_menu(self):
        while True:
            print("Escolha o tipo de arquivo:")
            print("1. EPUB")
            print("2. DOCX")
            print("3. PDF")
            print("4. MOBI")
            print("5. Sair")
            opcao = input("Digite o numero da opcao desejada: ")
            
            if opcao == "1":
                arquivo = input("Digite o nome do arquivo EPUB: ")
                texto = LeitorArquivos.extrair_texto_epub(arquivo, 1000)
                print("Texto extraído do arquivo EPUB:")
                print(texto)
            elif opcao == "2":
                arquivo = input("Digite o nome do arquivo DOCX: ")
                texto = LeitorArquivos.extrair_texto_docx(arquivo, 1000)
                print("Texto extraído do arquivo DOCX:")
                print(texto)
            elif opcao == "3":
                arquivo = input("Digite o nome do arquivo PDF: ")
                texto = LeitorArquivos.extrair_texto_pdf(arquivo, 1000)
                print("Texto extraído do arquivo PDF:")
                print(texto)
            elif opcao == "4":
                arquivo = input("Digite o nome do arquivo MOBI: ")
                texto = LeitorArquivos.extrair_texto_mobi(arquivo, 1000)
                print("Texto extraído do arquivo MOBI:")
                print(texto)
            elif opcao == "5":
                print("Saindo do programa...")
                break
            else:
                print("Opção inválida. Por favor, escolha uma das opções disponíveis.")

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
