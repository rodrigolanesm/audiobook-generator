import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from PyPDF2 import PdfReader
import ebooklib
from ebooklib import epub
from docx import Document
# PyMobi is not a standard library and may not be available

class FileSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selecione o arquivo")
        self.geometry("1000x1000")

        self.file_path = None

        self.label = tk.Label(self, text="Selecione o arquivo a ser aberto:")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Selecionar Arquivo", command=self.select_file)
        self.button.pack()

        self.image_label = tk.Label(self)
        self.image_label.pack()

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Arquivos suportados", "*.epub;*.docx;*.pdf;*.mobi")])
        self.preview_image(self.file_path)
        self.preview_text(self.file_path)

    def preview_image(self, file_path):
        try:
            image = Image.open(file_path)
            image.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        except Exception as e:
            print(f"Não foi possível pré-visualizar a imagem: {e}")

    def preview_text(self, file_path):
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                pdf = PdfReader(file)
                page = pdf.getPage(0)
                texto = page.extractText()
                messagebox.showinfo("Texto extraído", texto)
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            texto = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            messagebox.showinfo("Texto extraído", texto)
        elif file_path.endswith('.epub'):
            book = epub.read_epub(file_path)
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                texto = item.get_content()
                messagebox.showinfo("Texto extraído", texto)
                break
        else:
            messagebox.showinfo("Informação", "A leitura de arquivos .mobi não é suportada neste momento.")
