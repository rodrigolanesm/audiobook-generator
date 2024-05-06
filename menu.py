from leitor_arquivos import LeitorArquivos
import tkinter as tk
from interface import FileSelector
from PyPDF2 import PdfReader, PdfWriter
import ebooklib
from ebooklib import epub
from tkinter import Canvas, Scrollbar, Frame
from docx import Document
from pdf2image import convert_from_path
import tkinter as tk
from PIL import ImageTk, Image
import threading
from tkinter import simpledialog, messagebox, filedialog
from gtts import gTTS
from playsound import playsound
import html2text
import shutil

import os


class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.geometry("400x200")

        self.button1 = tk.Button(self, text="Ler arquivo", command=self.ler_arquivo)
        self.button1.pack(pady=10)
        
        self.button5 = tk.Button(self, text="Salvar leitura", command=self.salvar_leitura)
        self.button5.pack(pady=10)

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
    
    def falar(self, texto, arquivo, start, end):
        tts = gTTS(text=texto, lang='pt-br', slow=False)
        filename = f'{arquivo}_{start}-{end}.mp3'
        tts.save(filename)
        playsound(filename)

        # Crie a pasta 'livros' se ela não existir
        if not os.path.exists('livros'):
            os.makedirs('livros')

        # Extraia apenas o nome base do arquivo (sem o caminho e sem a extensão)
        nome_base = os.path.basename(arquivo).split('.')[0]

        # Crie a pasta com o nome base do arquivo dentro da pasta 'livros' se ela não existir
        pasta = f'livros/{nome_base}'
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        # Extraia apenas o nome do arquivo (sem o caminho)
        nome_arquivo = os.path.basename(filename)

        # Mova o arquivo de áudio para a pasta do livro dentro da pasta 'livros'
        shutil.move(filename, f'{pasta}/{nome_arquivo}')






    def ler_pdf(self, arquivo):
        startnum = simpledialog.askstring("Input", "Qual é o número da primeira página?  ")
        endnum = simpledialog.askstring("Input", "Qual é o número da última página?  ")

        try:
            start_page = int(startnum) - 1
            end_page = int(endnum)

            output_filename = simpledialog.askstring("Input", "Digite o nome do arquivo de saída, sem a extensão .pdf: ")

            texto = LeitorArquivos.extrair_texto_pdf(arquivo, start_page, end_page)  


            output_filename = output_filename + '.pdf'
            
            # Converta as páginas selecionadas do PDF em imagens
            images = convert_from_path(arquivo, first_page=start_page+1, last_page=end_page)

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
            threading.Thread(target=self.falar, args=(texto, arquivo, start_page, end_page)).start()
            
        except (ValueError, RuntimeError) as e:
            messagebox.showinfo("Erro", f"Erro ao processar o arquivo PDF: {e}")
        
                   

    def ler_docx(self, arquivo):
        # Leia o arquivo DOCX
        doc = Document(arquivo)

        # Peça ao usuário para especificar o intervalo de parágrafos
        startnum = simpledialog.askstring("Input", "Qual é o número do primeiro parágrafo?  ")
        endnum = simpledialog.askstring("Input", "Qual é o número do último parágrafo?  ")

        try:
            start_paragraph = int(startnum) - 1
            end_paragraph = int(endnum)

            # Extraia o texto do intervalo especificado de parágrafos
            texto = "\n".join([p.text for p in doc.paragraphs[start_paragraph:end_paragraph]])

            # Crie uma nova janela para exibir o texto
            text_window = tk.Toplevel(self)
            text_window.title(arquivo)

            # Crie um Text widget para exibir o texto
            text_widget = tk.Text(text_window, wrap='word')
            text_widget.insert('1.0', texto)
            text_widget.pack(expand=True, fill='both')

            # Inicie a reprodução do áudio depois que o texto for carregado
            threading.Thread(target=self.falar, args=(texto, arquivo, start_paragraph, end_paragraph)).start()
            messagebox.showinfo("Informação", f'O arquivo {arquivo} foi aberto com sucesso.')
            
        except (ValueError, RuntimeError) as e:
            messagebox.showinfo("Erro", f"Erro ao processar o arquivo DOCX: {e}")


    def ler_epub(self, arquivo):
        # Leia o arquivo EPUB
        book = epub.read_epub(arquivo)

        # Peça ao usuário para especificar o intervalo de itens
        startnum = simpledialog.askstring("Input", "Qual é o número do primeiro item?  ")
        endnum = simpledialog.askstring("Input", "Qual é o número do último item?  ")

        try:
            start_item = int(startnum) - 1
            end_item = int(endnum)

            # Extraia o texto do intervalo especificado de itens
            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            texto = ""
            for item in list(book.get_items())[start_item:end_item]:
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    texto += text_maker.handle(item.get_content().decode('utf-8'))

            # Crie uma nova janela para exibir o texto
            text_window = tk.Toplevel(self)
            text_window.title(arquivo)

            # Crie um Text widget para exibir o texto
            text_widget = tk.Text(text_window, wrap='word')
            text_widget.insert('1.0', texto)
            text_widget.pack(expand=True, fill='both')

            # Inicie a reprodução do áudio depois que o texto for carregado
            threading.Thread(target=self.falar, args=(texto,)).start()

            messagebox.showinfo("Informação", f'O arquivo {arquivo} foi aberto com sucesso.')
            
        except (ValueError, RuntimeError) as e:
            messagebox.showinfo("Erro", f"Erro ao processar o arquivo EPUB: {e}")

    
    def salvar_historico(self, arquivo, intervalo):
        # Crie o diretório "historico" se ele não existir
        os.makedirs("historico", exist_ok=True)

        # Use o nome do arquivo para criar um nome de arquivo de histórico
        filename = f"historico/{arquivo}.txt"

        # Adicione o novo intervalo ao final do arquivo de histórico
        with open(filename, "a") as file:
            file.write(f"{arquivo}|{intervalo[0]}-{intervalo[1]}\n")

    def salvar_leitura(self):
        # Peça ao usuário para especificar o arquivo e o intervalo de páginas ou parágrafos
        arquivo = simpledialog.askstring("Input", "Digite o nome do arquivo: ")
        startnum = simpledialog.askstring("Input", "Qual é o número da primeira página ou parágrafo?  ")
        endnum = simpledialog.askstring("Input", "Qual é o número da última página ou parágrafo?  ")

        try:
            # Converta os números de início e fim em inteiros
            start = int(startnum)
            end = int(endnum)

            # Salve o intervalo de páginas ou parágrafos no histórico
            self.salvar_historico(arquivo, (start, end))

            messagebox.showinfo("Informação", f'Leitura do arquivo {arquivo} salva com sucesso.')
            
        except (ValueError, RuntimeError) as e:
            messagebox.showinfo("Erro", f"Erro ao salvar a leitura: {e}")


    def limpar_historico_arquivo(self):
        arquivo = simpledialog.askstring("Input", "Digite o nome do arquivo para limpar o histórico: ")
        filename = f"historico/{arquivo}.txt"
        if os.path.exists(filename):
            os.remove(filename)
            messagebox.showinfo("Informação", f"Histórico do arquivo {arquivo} limpo com sucesso.")
        else:
            messagebox.showinfo("Informação", f"Nenhum histórico encontrado para o arquivo {arquivo}.")

    def limpar_historico_todos(self):
        try:
            # Remova todos os arquivos na pasta "historico"
            for filename in os.listdir("historico"):
                if filename.endswith(".txt"):
                    os.remove(f"historico/{filename}")
            messagebox.showinfo("Informação", "Histórico de todos os arquivos limpo com sucesso.")
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao limpar o histórico de todos os arquivos: {e}")

