import tkinter as tk

class Historico:
    def __init__(self):
        self.arquivos = []
    
        #exibe janela tk opções de histórico
        self.root = tk.Tk()
        self.root.title("Histórico")

        self.root.geometry("600x600")
    
        self.exibir_menu()
    
    def exibir_menu(self):
        #exibe o título do programa destacado em negrito e com fonte maior
        title = tk.Label(self.root, text="Histórico", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)
        
        #guia de opções
        label = tk.Label(self.root, text="Selecione uma opção:")
        label.pack(pady=10)
        
        #botões para as opções
        button3 = tk.Button(self.root, text="1) Visualizar histórico", command=self.salvar_leitura)
        button3.pack(pady=10)
        
        button4 = tk.Button(self.root, text="2) Salvar leitura", command=self.salvar_leitura)
        button4.pack(pady=10)
    
        button5 = tk.Button(self.root, text="3) Limpar histórico de arquivo único", command=self.limpar_historico_arquivo)
        button5.pack(pady=10)
        
        button6 = tk.Button(self.root, text="4) Limpar histórico de todos os arquivos", command=self.limpar_historico_todos_arquivos)
        button6.pack(pady=10)
        
        button7 = tk.Button(self.root, text="5) Sair", command=self.sair)
        button7.pack(pady=10)
                    
    def visualizar_historico(self):
        pass
        # criar janela tk que exibe o arquivo "historico.txt", localizado na pasta data/historico
        """  
        self.textbox = tk.Text(self.root)
        self.textbox.pack(pady=10)
        
        with open("data/historico/historico.txt", "r") as file:
            content = file.read()
            self.textbox.insert(tk.END, content) 
        """
        

    def salvar_leitura(self, arquivo, leitura):
        # Peça ao usuário para especificar o arquivo e o intervalo de páginas ou parágrafos
        pass

    def limpar_historico_arquivo(self, arquivo):
        pass

    def limpar_historico_todos_arquivos(self):
        pass
    
    def sair(self):
        self.root.destroy()
    
if __name__ == "__main__":
    historico = Historico()
    historico.exibir_menu()