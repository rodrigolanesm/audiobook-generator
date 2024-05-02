"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 24/04/2024 - 22:37:45
Linguagem: Python

Descrição: Menu inicial

"""

import pyttsx3
from leitor_arquivos import LeitorArquivos
from interface import FileSelector

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
        file_selector = FileSelector()
        file_selector.mainloop()
        arquivo_selecionado = file_selector.file_path

        if not arquivo_selecionado:
            print("Nenhum arquivo selecionado.")
            return

        tipo_arquivo = LeitorArquivos.get_tipo_arquivo(arquivo_selecionado)
        if tipo_arquivo is None:
            print("Tipo de arquivo não suportado.")
            return

        posicao_leitura = 0
        # Estimativa média da quantidade de palavras por página do arquivo 275
        limite_palavras = 20

        historico = self.carregar_historico()
        if arquivo_selecionado in historico:
            posicao_leitura = historico[arquivo_selecionado]
            print(f"Retomando leitura do arquivo {arquivo_selecionado} na posição {posicao_leitura}.")

        while True:
            texto = LeitorArquivos.extrair_texto(arquivo_selecionado, limite_palavras, posicao_leitura)

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
        self.salvar_historico(arquivo_selecionado, posicao_leitura)

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
