"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 24/04/2024 - 22:43:19
Linguagem: Python

Descrição: Realizar a leitura dos arquivos

"""

from ebooklib import epub
from docx import Document
import fitz, ebooklib, re

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
