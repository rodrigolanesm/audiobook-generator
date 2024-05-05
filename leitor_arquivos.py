from ebooklib import epub
from docx import Document
import fitz, ebooklib, re
from gtts import gTTS
from playsound import playsound
import os

"""
speak(text): Esta função recebe um texto como entrada e utiliza a biblioteca gTTS 
para converter o texto em fala usando a voz em português do Brasil. Em seguida, 
salva o áudio em um arquivo temporário, reproduz o áudio usando a biblioteca playsound
e remove o arquivo temporário depois que a reprodução é concluída.
"""

def speak(text):
    tts = gTTS(text=text, lang='pt-br', slow=False)
    filename = 'audio.mp3'
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

"""
get_tipo_arquivo(nome_arquivo): determina o tipo de arquivo 
com base em sua extensão. Ele recebe o nome do arquivo como entrada, extrai 
a extensão do nome do arquivo e retorna o tipo de arquivo correspondente 
(EPUB, DOCX, PDF, MOBI) ou None se o tipo de arquivo não for suportado.
"""

class LeitorArquivos:
    @staticmethod
    def get_tipo_arquivo(nome_arquivo):
        extensao = nome_arquivo.lower().split(".")[-1]
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
        
    """
extrair_texto, Esta função extrai o texto de um arquivo de acordo com o tipo de arquivo fornecido. Ela chama
a função apropriada para extrair o texto com base no tipo de arquivo e, em seguida,
converte o texto em fala usando a função speak. Finalmente, retorna o texto extraído.
"""

    @staticmethod
    def extrair_texto(arquivo, limite_palavras, posicao_leitura):
        tipo_arquivo = LeitorArquivos.get_tipo_arquivo(arquivo)
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

        # Chame a função speak aqui
        speak(texto_completo)

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
    
    @staticmethod
    def listar_arquivos(diretorio):
        for nome in os.listdir(diretorio):
            if os.path.isfile(os.path.join(diretorio, nome)):
                print(nome)
