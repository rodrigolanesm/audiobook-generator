"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 31/03/2024 - 18:02:43
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
            arquivo = input(f"Digite o nome do arquivo ({tipo_arquivo}) | (ex:. nome_arq.tipo_arq) : ")
            posicao_leitura = 0

            # Estimativa média da quantidade de palavras por página do arquivo 275
            limite_palavras = 20

            historico = self.carregar_historico()
            if arquivo in historico:
                posicao_leitura = historico[arquivo]
                print(f"Retomando leitura do arquivo {arquivo} na posição {posicao_leitura}.")

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
                    opcao_continuar = input("Deseja:\n1. Ir para a página anterior\n2. Repetir a página\n3. Ir para a próxima página\nDigite o número da opção desejada: ")
                    if opcao_continuar == "1" and posicao_leitura >= limite_palavras:
                        posicao_leitura -= limite_palavras
                    elif opcao_continuar == "2":
                        continue
                    elif opcao_continuar == "3":
                        posicao_leitura += limite_palavras
                    else:
                        print("Opção inválida. Voltando para o menu inicial.")
                        break

            # Salvar informações de leitura no histórico
            self.salvar_historico(arquivo, posicao_leitura)

    def carregar_historico(self):
        historico = {}
        try:
            with open("historico.txt", "r") as file:
                for line in file:
                    arquivo, posicao_leitura = line.strip().split("|")
                    historico[arquivo] = int(posicao_leitura)
        except FileNotFoundError:
            pass
        return historico

    def salvar_historico(self, arquivo, posicao_leitura):
        historico = self.carregar_historico()
        historico[arquivo] = posicao_leitura
        with open("historico.txt", "w") as file:
            for arquivo, posicao_leitura in historico.items():
                file.write(f"{arquivo}|{posicao_leitura}\n")

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
