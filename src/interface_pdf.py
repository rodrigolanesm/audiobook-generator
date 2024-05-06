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

class Interface_PDF:
    def __init__(self, arquivo, start_page, end_page):
        self.arquivo = arquivo
        self.extensao = "pdf"
        self.texto = ""
        self.start_page = start_page
        self.end_page = end_page
    
    @staticmethod
    def extrair_texto_pdf(arquivo_pdf, start_page, end_page, limite_palavras=1000, posicao_leitura=0):
        start_page = start_page
        end_page = end_page    
    
        texto_completo = ''
        doc = fitz.open(arquivo_pdf)
        for page_num in range(start_page, end_page):
            texto_pagina = doc[page_num].get_text()
            texto_completo += texto_pagina
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[posicao_leitura:limite_palavras + posicao_leitura])
            
    def exibir_pdf(self, texto):
        try:
            output_filename = simpledialog.askstring("Input", "Digite o nome do arquivo de saída, sem a extensão .pdf: ")

            texto = self.extrair_texto_pdf(self.arquivo, self.start_page, self.end_page)  

            output_filename = output_filename + '.pdf'
            
            # Converta as páginas selecionadas do PDF em imagens
            images = convert_from_path(self.arquivo, first_page=self.start_page+1, last_page=self.end_page)

            # Crie uma nova janela para exibir as imagens
            image_window = tk.Toplevel()
            image_window.title(output_filename)

            # Crie um Canvas e uma barra de rolagem
            canvas = Canvas(image_window)
            scrollbar = Scrollbar(image_window, command=canvas.yview)
            canvas.config(yscrollcommand=scrollbar.set)

            # Crie um Frame para conter as imagens e adicione-o ao Canvas
            frame = Frame(canvas)
            frame_id = canvas.create_window((0,0), window=frame, anchor='nw')

            for i, img in enumerate(images):
                # Converta a imagem PIL em uma imagem Tkinter
                tk_image = ImageTk.PhotoImage(img)
                label = tk.Label(frame, image=tk_image)
                label.image = tk_image  # Mantenha uma referência à imagem
                label.pack()

                # Atualize o scrollregion após a configuração do conteúdo do frame
                canvas.itemconfig(frame_id, width=img.width, height=(i+1)*img.height)
                canvas.config(scrollregion=canvas.bbox('all'))

            # Empacote o Canvas e a barra de rolagem
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            

            messagebox.showinfo("Informação", f'O arquivo {output_filename} foi aberto com sucesso.')
            
            #self.after(1000, self.falar, texto)
            threading.Thread(target=self.falar, args=(texto,)).start()
            
            
        except (ValueError, RuntimeError) as e:
            messagebox.showinfo("Erro", f"Erro ao processar o arquivo PDF: {e}")
            
    def falar(self, texto):
        tts = gTTS(text=self.texto, lang='pt-br', slow=False)
        audio_filename = f'{self.output_filename}' + '|' + f'{self.start.page}' + '.mp3'
        tts.save("data/audiobooks/"+audio_filename)
        os.system("start data/audiobooks/"+ audio_filename)
        #os.remove(audio_filename)