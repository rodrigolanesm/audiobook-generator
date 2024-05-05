import pyttsx3
from leitor_arquivos import LeitorArquivos
from interface import FileSelector
import tkinter as tk
from leitor_arquivos import LeitorArquivos
from interface import FileSelector
from PyPDF2 import PdfReader, PdfWriter
import ebooklib
from ebooklib import epub
from docx import Document
# PyMobi is not a standard library and may not be available

import fitz

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from gtts import gTTS
from playsound import playsound
import os
from leitor_arquivos import LeitorArquivos

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.geometry("400x200")

        self.button1 = tk.Button(self, text="Ler arquivo", command=self.ler_arquivo)
        self.button1.pack(pady=10)

        self.button2 = tk.Button(self, text="Limpar histórico de um arquivo específico", command=self.limpar_historico_arquivo)
        self.button2.pack(pady=10)

        self.button3 = tk.Button(self, text="Limpar histórico de todos os arquivos", command=self.limpar_historico_todos)
        self.button3.pack(pady=10)

        self.button4 = tk.Button(self, text="Sair", command=self.quit)
        self.button4.pack(pady=10)

    def ler_arquivo(self):
        arquivo = self.selecionar_arquivo()
        if not arquivo:
            messagebox.showinfo("Informação", "Nenhum arquivo selecionado.")
            return

        tipo_arquivo = arquivo.split('.')[-1]
        if tipo_arquivo not in ('pdf', 'docx', 'epub'):
            messagebox.showinfo("Informação", "Tipo de arquivo não suportado.")
            return

        if tipo_arquivo == 'pdf':
            self.ler_pdf(arquivo)
        elif tipo_arquivo == 'docx':
            self.ler_docx(arquivo)
        elif tipo_arquivo == 'epub':
            self.ler_epub(arquivo)

    def selecionar_arquivo(self):
        return filedialog.askopenfilename()

    def ler_pdf(self, arquivo):
        startnum = simpledialog.askstring("Input", "Qual é o número da primeira página?  ")
        endnum = simpledialog.askstring("Input", "Qual é o número da última página?  ")

        try:
            start_page = int(startnum) - 1
            end_page = int(endnum)

            output_filename = simpledialog.askstring("Input", "Digite o nome do arquivo de saída, sem a extensão .pdf: ")

            texto = LeitorArquivos.extrair_texto_pdf(arquivo, start_page, end_page)  

            self.falar(texto)

            output_filename = output_filename + '.pdf'
            messagebox.showinfo("Informação", f'O arquivo {output_filename} foi criado com sucesso.')
        except (ValueError, RuntimeError) as e:
            messagebox.showinfo("Erro", f"Erro ao processar o arquivo PDF: {e}")

    def falar(self, texto):
        tts = gTTS(text=texto, lang='pt-br', slow=False)
        filename = 'audio.mp3'
        tts.save(filename)
        playsound(filename)
        os.remove(filename)

    def ler_docx(self, arquivo):
        doc = Document(arquivo)
        for paragraph in doc.paragraphs:
            messagebox.showinfo("Texto extraído", paragraph.text)

    def ler_epub(self, arquivo):
        book = epub.read_epub(arquivo)
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            messagebox.showinfo("Texto extraído", item.get_content())

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
        arquivo = simpledialog.askstring("Input", "Digite o nome do arquivo para limpar o histórico: ")
        historico = self.carregar_historico()
        if arquivo in historico:
            del historico[arquivo]
            with open("historico.txt", "w") as file:
                for arquivo_historico, posicao_leitura in historico.items():
                    file.write(f"{arquivo_historico}|{posicao_leitura}\n")
            messagebox.showinfo("Informação", f"Histórico do arquivo {arquivo} limpo com sucesso.")
        else:
            messagebox.showinfo("Informação", f"Nenhum histórico encontrado para o arquivo {arquivo}.")

    def limpar_historico_todos(self):
        try:
            open("historico.txt", "w").close()
            messagebox.showinfo("Informação", "Histórico de todos os arquivos limpo com sucesso.")
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao limpar o histórico de todos os arquivos: {e}")

