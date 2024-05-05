import tkinter as tk
from tkinter import messagebox
from leitor_arquivos import LeitorArquivos

class Menu:
    def _init_(self):
        self.root = tk.Tk()
        self.root.title("Gerador de Audiobooks")
        self.root.geometry("600x600")
        self.create_menu()

    def create_menu(self):
        title = tk.Label(self.root, text="Gerador de Audiobooks", font=("Helvetica", 16, "bold"))
        title.pack()

        label = tk.Label(self.root, text="Selecione uma opção:")
        label.pack()

        button1 = tk.Button(self.root, text="1) Ler Arquivo", command=self.ler_arquivo)
        button1.pack()

        button2 = tk.Button(self.root, text="2) Visualizar histórico", command=self.visualizar_historico)
        button2.pack()

        button3 = tk.Button(self.root, text="3) Limpar histórico do arquivo", command=self.limpar_historico_arquivo)
        button3.pack()

        button4 = tk.Button(self.root, text="4) Limpar histórico de todos os arquivos", command=self.limpar_historico_todos)
        button4.pack()

        button5 = tk.Button(self.root, text="5) Sair", command=self.sair)
        button5.pack()

    def ler_arquivo(self):
        leitor_arquivo = LeitorArquivos()
        arquivo_selecionado = input("Digite o nome do arquivo a ser lido: ")
        historico = self.carregar_historico()
        if arquivo_selecionado in historico:
            posicao_leitura = historico[arquivo_selecionado]
            limite_palavras = 20
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

            self.salvar_historico(arquivo_selecionado, posicao_leitura)
        else:
            print(f"Arquivo {arquivo_selecionado} não encontrado no histórico.")

    def visualizar_historico(self):
        historico = self.carregar_historico()
        if historico:
            print("Histórico:")
            for arquivo, posicao_leitura in historico.items():
                print(f"Arquivo: {arquivo}, Posição de Leitura: {posicao_leitura}")
        else:
            print("Nenhum histórico encontrado.")

    def sair(self):
        self.root.destroy()

    def exibir_menu(self):
        self.root.mainloop()

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