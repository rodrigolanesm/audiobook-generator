import pyttsx3
from leitor_arquivos import LeitorArquivos
from interface import FileSelector
import tkinter as tk
from tkinter import messagebox

class Menu:
    def __init__(self):
        self.engine = pyttsx3.init()

    def falar(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()

    def exibir_menu(self):
        root = tk.Tk()
        root.title("Audiobook Generator")
        
        label = tk.Label(root, text="Escolha o tipo de ação:")
        label.pack()

        button1 = tk.Button(root, text="Ler arquivo", command=self.ler_arquivo)
        button1.pack()

        button2 = tk.Button(root, text="Limpar histórico de um arquivo específico", command=self.limpar_historico_arquivo)
        button2.pack()

        button3 = tk.Button(root, text="Limpar histórico de todos os arquivos", command=self.limpar_historico_todos)
        button3.pack()

        button4 = tk.Button(root, text="Sair", command=root.quit)
        button4.pack()

        root.mainloop()

    def ler_arquivo(self):
        file_selector = FileSelector()
        file_selector.mainloop()
        arquivo_selecionado = file_selector.file_path

        if not arquivo_selecionado:
            messagebox.showinfo("Audiobook Generator", "Nenhum arquivo selecionado.")
            return

        tipo_arquivo = LeitorArquivos.get_tipo_arquivo(arquivo_selecionado)
        if tipo_arquivo is None:
            messagebox.showinfo("Audiobook Generator", "Tipo de arquivo não suportado.")
            return

        posicao_leitura = 0
        # Estimativa média da quantidade de palavras por página do arquivo 275
        limite_palavras = 20

        historico = self.carregar_historico()
        if arquivo_selecionado in historico:
            posicao_leitura = historico[arquivo_selecionado]
            messagebox.showinfo("Audiobook Generator", f"Retomando leitura do arquivo {arquivo_selecionado} na posição {posicao_leitura}.")

        while True:
            texto = LeitorArquivos.extrair_texto(arquivo_selecionado, limite_palavras, posicao_leitura)

            messagebox.showinfo("Audiobook Generator", "Texto extraído:\n" + texto)
            self.falar(texto)

            continuar = messagebox.askyesno("Audiobook Generator", "Deseja continuar a leitura deste arquivo?")
            if not continuar:
                break
            else:
                opcao_continuar = messagebox.askquestion("Audiobook Generator", "Deseja:\n1. Ir para a página anterior\n2. Repetir a página\n3. Ir para a próxima página")
                if opcao_continuar == "yes" and posicao_leitura >= limite_palavras:
                    posicao_leitura -= limite_palavras
                elif opcao_continuar == "no":
                    continue
                elif opcao_continuar == "cancel":
                    posicao_leitura += limite_palavras
                else:
                    messagebox.showinfo("Audiobook Generator", "Opção inválida. Voltando para o menu inicial.")
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
            messagebox.showinfo("Audiobook Generator", f"Histórico do arquivo {arquivo} limpo com sucesso.")
        else:
            messagebox.showinfo("Audiobook Generator", f"Nenhum histórico encontrado para o arquivo {arquivo}.")

    def limpar_historico_todos(self):
        try:
            open("historico.txt", "w").close()
            messagebox.showinfo("Audiobook Generator", "Histórico de todos os arquivos limpo com sucesso.")
        except Exception as e:
            messagebox.showinfo("Audiobook Generator", "Erro ao limpar o histórico de todos os arquivos:", e)

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
