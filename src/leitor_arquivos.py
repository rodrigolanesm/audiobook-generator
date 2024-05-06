import tkinter as tk
from tkinter import messagebox, Canvas, simpledialog, filedialog, Scrollbar, Frame
from pdf2image import convert_from_path
from ebooklib import epub
from docx import Document
import fitz, ebooklib, re
from seletor_arquivos import SeletorArquivos
from PIL import ImageTk, Image
import threading
import os
from gtts import gTTS
from interface_pdf import Interface_PDF

class LeitorArquivos:
    #O leitor de arquivos deve realizar 5 tarefas:
    #1. selecionar um arquivo para leitura
    #2. identificar o tipo do arquivo pela extensão
    #3. extrair o texto do arquivo
    #4. exibir o texto extraído em uma janela de texto
    #5. executar em áudio o texto extraído
    
    #Observação: as tarefas 4 e 5 devem ser executadas simultaneamente
    
    
    def __init__(self):
        self.arquivo = None
        self.extensao = None
        
        #janela principal 600x600
        self.root = tk.Tk()
        self.root.title("Leitor de Arquivos")
        
        self.root.geometry("400x400")
        
        self.criar_menu()
        
    def criar_menu(self):
        #exibe o título do programa destacado em negrito e com fonte maior
        title = tk.Label(self.root, text="Leitor de arquivos", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)
        
        #guia de opções
        label = tk.Label(self.root, text="Siga o passo a passo:")
        label.pack(pady=10)
        
        #botões para as opções
        button1 = tk.Button(self.root, text="1) Selecionar Arquivo", command=self.selecionar_arquivo)
        button1.pack(pady=10)
        
        button2 = tk.Button(self.root, text="2) Ler", command= self.ler)
        button2.pack(pady=10)
        
        button3 = tk.Button(self.root, text="3) Sair", command=self.sair)
        button3.pack(pady=10)
    
    def sair(self):
        self.root.destroy()
    
    #tarefa 1: selecionar um arquivo para leitura
    def selecionar_arquivo(self):
        seletor_arquivo_obj = SeletorArquivos()
        arquivo_selecionado = seletor_arquivo_obj.file_path
        print("[OK] arquivo_selecionado: " + arquivo_selecionado)
        if arquivo_selecionado is not None:
            self.arquivo = arquivo_selecionado
            
    #tarefa 2: identificar o tipo do arquivo pela extensão
    def identificar_tipo_arquivo(self):
        arquivo = self.arquivo
        
        extensao = arquivo.split(".")[-1]
        if extensao == "epub" or extensao == "EPUB":
            return "epub"
        elif extensao == "docx" or extensao == "DOCX":
            return "docx"
        elif extensao == "pdf" or extensao == "PDF":
            return "pdf"
        elif extensao == "mobi" or extensao == "MOBI":
            return "mobi"
        else:
            return None

    #tarefa 3: extrair o texto do arquivo
    """ @staticmethod
    def extrair_texto(arquivo, limite_palavras, posicao_leitura):
        tipo_arquivo = LeitorArquivos.identificar_tipo_arquivo(arquivo)
        if tipo_arquivo is None:
            print("Tipo de arquivo não suportado.")
            return ""

        texto_completo = ''
        if tipo_arquivo == "EPUB" or tipo_arquivo == "epub":
            texto_completo = LeitorArquivos.extrair_texto_epub(arquivo, limite_palavras, posicao_leitura)
        elif tipo_arquivo == "DOCX" or tipo_arquivo == "docx":
            texto_completo = LeitorArquivos.extrair_texto_docx(arquivo, limite_palavras, posicao_leitura)
        elif tipo_arquivo == "PDF" or tipo_arquivo == "pdf":
            texto_completo = LeitorArquivos.extrair_texto_pdf(arquivo, limite_palavras, posicao_leitura)
        elif tipo_arquivo == "MOBI" or tipo_arquivo == "mobi":
            texto_completo = LeitorArquivos.extrair_texto_mobi(arquivo, limite_palavras, posicao_leitura)

        return texto_completo 
     """
    @staticmethod
    def extrair_texto_epub(arquivo_epub, limite_palavras, posicao_leitura):
        livro = epub.read_epub(arquivo_epub)
        texto_completo = ''
        for item in livro.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                texto = item.get_body_content().decode('utf-8')
                texto_sem_tags = re.sub('<[^<]+?>', '', texto)
                texto_completo += texto_sem_tags
                palavras = texto_completo.split()
                if len(palavras) >= limite_palavras:
                    break
        return ' '.join(palavras[posicao_leitura:limite_palavras + posicao_leitura])

    @staticmethod
    def extrair_texto_docx(arquivo_docx, limite_palavras, posicao_leitura):
        doc = Document(arquivo_docx)
        texto_completo = ''
        for paragraph in doc.paragraphs:
            texto_completo += paragraph.text + ' '
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[posicao_leitura:limite_palavras + posicao_leitura])

    @staticmethod
    def extrair_texto_pdf(arquivo_pdf, start_page, end_page, limite_palavras=1000, posicao_leitura=0):
        texto_completo = ''
        doc = fitz.open(arquivo_pdf)
        for page_num in range(start_page, end_page):
            texto_pagina = doc[page_num].get_text()
            texto_completo += texto_pagina
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[posicao_leitura:limite_palavras + posicao_leitura])

    @staticmethod
    def extrair_texto_mobi(arquivo_mobi, limite_palavras, posicao_leitura):
        texto_completo = ''
        doc = fitz.open(arquivo_mobi)
        for page_num in range(len(doc)):
            texto_pagina = doc[page_num].get_text()
            texto_completo += texto_pagina
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[posicao_leitura:limite_palavras + posicao_leitura])

    #tarefa 4: exibir o texto extraído em uma janela com PDF2image
    def ler(self):
        arquivo = self.arquivo
        self.extensao = self.identificar_tipo_arquivo()
        print("[OK] Identificou o arquivo e extensão: " + arquivo + " - " + self.extensao)
        
        if self.extensao == "pdf":
            self.ler_pdf(self.arquivo)  
        if self.extensao == "epub":
            #texto = LeitorArquivos.extrair_texto_epub(arquivo, start_page, end_page)
            pass
        if self.extensao == "docx":
            #texto = LeitorArquivos.extrair_texto_docx(arquivo, start_page, end_page)
            pass
        if self.extensao == "mobi":
            #texto = LeitorArquivos.extrair_texto_mobi(arquivo, start_page, end_page)
            pass

    def ler_pdf(self, arquivo):
        start_page = int(simpledialog.askstring("Input", "Qual é o número da primeira página?  ")) - 1
        end_page = int(simpledialog.askstring("Input", "Qual é o número da última página?  "))
        
        interface_pdf = Interface_PDF(arquivo, start_page, end_page)
        interface_pdf.exibir_pdf(interface_pdf.extrair_texto_pdf())
        
    def falar(self, texto):
        tts = gTTS(text=texto, lang='pt-br', slow=False)
        audio_filename = f'{self.output_filename}' + '|' + f'{self.start.page}' + '.mp3'
        tts.save("data/audiobooks/"+audio_filename)
        os.system("start data/audiobooks/"+ audio_filename)
        #os.remove(audio_filename)

if __name__ == "__main__":
    leitor = LeitorArquivos()
    leitor.root.mainloop()