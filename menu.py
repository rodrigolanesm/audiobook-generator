"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 26/03/2024 - 19:33:55
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
            posicao_leitura = 0
            limite_palavras = 25

            while True:
                texto = None
                if opcao == "1":
                    texto = LeitorArquivos.extrair_texto_epub(arquivo, limite_palavras, posicao_leitura)
                elif opcao == "2":
                    texto = LeitorArquivos.extrair_texto_docx(arquivo, limite_palavras, posicao_leitura)
                elif opcao == "3":
                    texto = LeitorArquivos.extrair_texto_pdf(arquivo, limite_palavras, posicao_leitura)
                elif opcao == "4":
                    texto = LeitorArquivos.extrair_texto_mobi(arquivo, limite_palavras, posicao_leitura)

                print("Texto extraído:")
                print(texto)
                self.falar(texto)

                continuar = input("Deseja continuar a leitura deste arquivo? (s/n): ").lower()
                if continuar == "n":
                    break
                elif continuar == "s":
                    opcao_continuar = input("Deseja:\n1. Voltar para a leitura anterior\n2. Repetir a leitura\n3. Prosseguir com a leitura\nDigite o número da opção desejada: ")
                    if opcao_continuar == "1" and posicao_leitura >= limite_palavras:
                        posicao_leitura -= limite_palavras
                    elif opcao_continuar == "2":
                        continue
                    elif opcao_continuar == "3":
                        posicao_leitura += limite_palavras
                    else:
                        print("Opção inválida. Voltando para o menu inicial.")
                        break

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
