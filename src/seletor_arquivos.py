import tkinter as tk
from tkinter import filedialog

class SeletorArquivos(tk.Tk):
    def __init__(self):
        self.file_path = None
        self.selecionar_arquivo()

    def selecionar_arquivo(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Arquivos suportados", "*.epub;*.docx;*.pdf;*.mobi")])


if __name__ == "__main__":
    app = SeletorArquivos()
    app.mainloop()
