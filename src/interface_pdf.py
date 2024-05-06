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
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.extensao = "pdf"
    
    def exibir_pdf(self):
        startnum = simpledialog.askstring("Input", "Qual é o número da primeira página?  ")
        endnum = simpledialog.askstring("Input", "Qual é o número da última página?  ")

        try:
            start_page = int(startnum) - 1
            end_page = int(endnum)

            output_filename = simpledialog.askstring("Input", "Digite o nome do arquivo de saída, sem a extensão .pdf: ")

            texto = self.extrair_texto_pdf(self.arquivo, start_page, end_page)  


            output_filename = output_filename + '.pdf'
            
            # Converta as páginas selecionadas do PDF em imagens
            images = convert_from_path(self.arquivo, first_page=start_page+1, last_page=end_page)

            # Crie uma nova janela para exibir as imagens
            image_window = tk.Toplevel(self)
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
        tts = gTTS(text=texto, lang='pt-br', slow=False)
        audio_filename = f'{self.output_filename}' + '|' + f'{self.start.page}' + '.mp3'
        tts.save("data/audiobooks/"+audio_filename)
        os.system("start data/audiobooks/"+ audio_filename)
        #os.remove(audio_filename)