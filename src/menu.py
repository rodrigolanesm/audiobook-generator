import tkinter as tk
from tkinter import messagebox
from leitor_arquivos import LeitorArquivos
from historico import Historico

class Menu:
    def __init__(self):
        #janela principal 600x600
        self.root = tk.Tk()
        self.root.title("Gerador de Audiobooks")
        
        self.root.geometry("600x280")
        
        self.criar_menu()
        
    def criar_menu(self):
        #exibe o título do programa destacado em negrito e com fonte maior
        title = tk.Label(self.root, text="Gerador de Audiobooks", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)
        
        #guia de opções
        label = tk.Label(self.root, text="Selecione uma opção:")
        label.pack(pady=10)
        
        #botões para as opções
        button1 = tk.Button(self.root, text="1) Ler Arquivo", command=self.ler_arquivo)
        button1.pack(pady=10)
    
        button2 = tk.Button(self.root, text="2) Histórico", command=self.menu_historico)
        button2.pack(pady=10)
        
        button3 = tk.Button(self.root, text="3) Sair", command=self.sair)
        button3.pack(pady=10)
        
    def ler_arquivo(self):
        #instancia um objeto da classe LeitorArquivos
        leitor_arquivo = LeitorArquivos()
        
    def menu_historico(self):
        #instancia um objeto da classe Historico
        historico = Historico()
        
    def sair(self):
        self.root.destroy()

    def exibir_menu(self):
        self.root.mainloop()

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
