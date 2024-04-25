"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 24/04/2024
Última Atualização: 24/04/2024 - 17:42:28
Linguagem: Python

Descrição: Interface

"""

import tkinter as tk
from tkinter import filedialog

class FileSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selecione o arquivo")
        self.geometry("400x200")

        self.file_path = None

        self.label = tk.Label(self, text="Selecione o arquivo a ser aberto:")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Selecionar Arquivo", command=self.select_file)
        self.button.pack()

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Arquivos suportados", "*.epub;*.docx;*.pdf;*.mobi")])
        self.destroy()

if __name__ == "__main__":
    app = FileSelector()
    app.mainloop()
