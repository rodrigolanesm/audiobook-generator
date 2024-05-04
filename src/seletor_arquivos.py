import tkinter as tk
from tkinter import filedialog

class SeletorArquivos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selecione o arquivo")
        self.geometry("400x200")

        self.file_path = None

        self.label = tk.Label(self, text="Selecione o arquivo a ser aberto:")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.button.pack()

    def selecionar_arquivo(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Arquivos suportados", "*.epub;*.docx;*.pdf;*.mobi")])
        self.destroy()

if __name__ == "__main__":
    app = SeletorArquivos()
    app.mainloop()
