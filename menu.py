"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 09/04/2024 - 17:42:28
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
            print("Escolha o tipo de ação:")
            print("1. Ler arquivo")
            print("2. Limpar histórico de um arquivo específico")
            print("3. Limpar histórico de todos os arquivos")
            print("4. Sair")
            opcao = input("Digite o número da opção desejada: ")
            
            if opcao == "4":
                print("Saindo do programa...")
                break
            
            if opcao not in ["1", "2", "3"]:
                print("Opção inválida. Por favor, escolha uma das opções disponíveis.")
                continue
            
            if opcao == "1":
                self.ler_arquivo()
            elif opcao == "2":
                self.limpar_historico_arquivo()
            elif opcao == "3":
                self.limpar_historico_todos()

    def ler_arquivo(self):
        while True:
            print("Escolha o tipo de arquivo:")
            print("1. EPUB")
            print("2. DOCX")
            print("3. PDF")
            print("4. MOBI")
            print("5. Voltar")
            opcao = input("Digite o número da opção desejada: ")
            
            if opcao == "5":
                print("Voltando ao menu principal...")
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

    def limpar_historico_arquivo(self):
        arquivo = input("Digite o nome do arquivo para limpar o histórico: ")
        historico = self.carregar_historico()
        if arquivo in historico:
            del historico[arquivo]
            with open("historico.txt", "w") as file:
                for arquivo_historico, posicao_leitura in historico.items():
                    file.write(f"{arquivo_historico}|{posicao_leitura}\n")
            print(f"Histórico do arquivo {arquivo} limpo com sucesso.")
        else:
            print(f"Nenhum histórico encontrado para o arquivo {arquivo}.")

    def limpar_historico_todos(self):
        try:
            open("historico.txt", "w").close()
            print("Histórico de todos os arquivos limpo com sucesso.")
        except Exception as e:
            print("Erro ao limpar o histórico de todos os arquivos:", e)

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
