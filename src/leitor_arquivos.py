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
        
        #janela principal 600x600
        self.root = tk.Tk()
        self.root.title("Leitor de Arquivos")
        
        self.root.geometry("600x600")
        
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
    
        button2 = tk.Button(self.root, text="2) Identificar tipo ", command=self.identificar_tipo_arquivo)
        button2.pack(pady=10)
        
        button3 = tk.Button(self.root, text="3) Ler", command=lambda: self.ler(self.arquivo))
        button3.pack(pady=10)
        
        button4 = tk.Button(self.root, text="4) Sair", command=self.sair)
        button4.pack(pady=10)
    
    def sair(self):
        self.root.destroy()
    
    #tarefa 1: selecionar um arquivo para leitura
    def selecionar_arquivo(self):
        seletor_arquivo_obj = SeletorArquivos()
        arquivo_selecionado = seletor_arquivo_obj.file_path
        if arquivo_selecionado is not None:
            self.arquivo = arquivo_selecionado
            
    #tarefa 2: identificar o tipo do arquivo pela extensão
    def identificar_tipo_arquivo(self):
        print("*********************************** C H E G O U       A Q U I *******************************************" )
        extensao = self.arquivo.lower().split(".")[-1]
        if extensao == "epub":
            return "EPUB"
        elif extensao == "docx":
            return "DOCX"
        elif extensao == "pdf":
            return "PDF"
        elif extensao == "mobi":
            return "MOBI"
        else:
            return None

    #tarefa 3: extrair o texto do arquivo
    @staticmethod
    def extrair_texto(arquivo, limite_palavras, posicao_leitura):
        tipo_arquivo = LeitorArquivos.identificar_tipo_arquivo(arquivo)
        if tipo_arquivo is None:
            print("Tipo de arquivo não suportado.")
            return ""

        texto_completo = ''
        if tipo_arquivo == "EPUB":
            texto_completo = LeitorArquivos.extrair_texto_epub(arquivo, limite_palavras, posicao_leitura)
        elif tipo_arquivo == "DOCX":
            texto_completo = LeitorArquivos.extrair_texto_docx(arquivo, limite_palavras, posicao_leitura)
        elif tipo_arquivo == "PDF":
            texto_completo = LeitorArquivos.extrair_texto_pdf(arquivo, limite_palavras, posicao_leitura)
        elif tipo_arquivo == "MOBI":
            texto_completo = LeitorArquivos.extrair_texto_mobi(arquivo, limite_palavras, posicao_leitura)

        return texto_completo 
    
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
    def extrair_texto_pdf(arquivo_pdf, limite_palavras, posicao_leitura):
        texto_completo = ''
        doc = fitz.open(arquivo_pdf)
        for page_num in range(len(doc)):
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

    #tarefa 4: exibir o texto extraído em uma janela com PDFViewer
    def ler(self, arquivo):
        startnum = simpledialog.askstring("Input", "Ler a partir de qual página?  ")
        #endnum = simpledialog.askstring("Input", "Qual é o número da última página?  ")

        try:
            start_page = int(startnum) - 1
            end_page = int(startnum)        #pagina seguinte ao start_page

            output_filename = arquivo.split('/')[-1].split('.')[0]+'|pags'+str(start_page+1)+'-'+str(end_page)

            if self.extensao == "pdf":
                texto = LeitorArquivos.extrair_texto_pdf(arquivo, start_page, end_page)  
            if self.extensao == "epub":
                texto = LeitorArquivos.extrair_texto_epub(arquivo, start_page, end_page)
            if self.extensao == "docx":
                texto = LeitorArquivos.extrair_texto_docx(arquivo, start_page, end_page)
            if self.extensao == "mobi":
                texto = LeitorArquivos.extrair_texto_mobi(arquivo, start_page, end_page)

            output_filename = output_filename + '.pdf'
            
            # Converta as páginas selecionadas do PDF em imagens
            images = convert_from_path(arquivo, first_page=start_page+1, last_page=end_page)
            #images = convert_from_path(arquivo, first_page=start_page+1, last_page=end_page + 1)
            
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
            
            # Mensagem de confirmação de sucesso
            #messagebox.showinfo("Informação", f'O arquivo {output_filename} foi aberto com sucesso.')
            
            #self.after(1000, self.falar, texto)
            threading.Thread(target=self.falar, args=(texto,)).start()
            
            #registra as páginas lidas no histórico
            self.historico.salvar_leitura(output_filename, texto)
            
        except (ValueError, RuntimeError) as e:
            messagebox.showinfo("Erro", f"Erro ao processar o arquivo PDF: {e}")

    def falar(self, texto):
        tts = gTTS(text=texto, lang='pt-br', slow=False)
        filename = 'audio.mp3'
        tts.save("data/audiobooks/"+filename)
        os.system("start data/audiobooks/"+ filename)
        #os.remove(filename)
