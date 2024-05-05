import tkinter as tk
from tkinter import messagebox
from leitor_arquivos import LeitorArquivos

class Menu:
    def __init__(self):
        #janela principal 600x600
        self.root = tk.Tk()
        self.root.title("Gerador de Audiobooks")
        
        self.root.geometry("600x600")
        
        self.create_menu()
        
    def create_menu(self):
        #exibe o título do programa destacado em negrito e com fonte maior
        title = tk.Label(self.root, text="Gerador de Audiobooks", font=("Helvetica", 16, "bold"))
        title.pack()
        
        #guia de opções
        label = tk.Label(self.root, text="Selecione uma opção:")
        label.pack()
        
        #botões para as opções
        button1 = tk.Button(self.root, text="1) Ler Arquivo", command=self.ler_arquivo)
        button1.pack()
        
        button2 = tk.Button(self.root, text="2) Visualizar histórico", command=self.visualizar_historico)
        button2.pack()
        
        button3 = tk.Button(self.root, text="3) Sair", command=self.sair)
        button3.pack()
        
    def ler_arquivo(self):
        #instancia um objeto da classe LeitorArquivos
        leitor_arquivo = LeitorArquivos()
        
    def visualizar_historico(self):
        # Lógica para visualizar o histórico
        messagebox.showinfo("Visualizar Histórico", "Opção Visualizar Histórico selecionada")
        
    def sair(self):
        self.root.destroy()

    def exibir_menu(self):
        self.root.mainloop()

if __name__ == "__main__":
    menu = Menu()
    menu.exibir_menu()
