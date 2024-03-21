"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 21/03/2024 - 17:23:47
Linguagem: Python

Descrição: Menu inicial

"""

from ebooklib import epub
from docx import Document
import fitz, re, ebooklib

class LeitorArquivos:
    
    def extrair_texto_epub(arquivo_epub, limite_palavras):
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
        return ' '.join(palavras[:limite_palavras])

    
    def extrair_texto_docx(arquivo_docx, limite_palavras):
        doc = Document(arquivo_docx)
        texto_completo = ''
        for paragraph in doc.paragraphs:
            texto_completo += paragraph.text + ' '
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[:limite_palavras])

    
    def extrair_texto_pdf(arquivo_pdf, limite_palavras):
        texto_completo = ''
        doc = fitz.open(arquivo_pdf)
        for page_num in range(len(doc)):
            texto_pagina = doc[page_num].get_text()
            texto_completo += texto_pagina
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[:limite_palavras])

    
    def extrair_texto_mobi(arquivo_mobi, limite_palavras):
        texto_completo = ''
        doc = fitz.open(arquivo_mobi)
        for page_num in range(len(doc)):
            texto_pagina = doc[page_num].get_text()
            texto_completo += texto_pagina
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[:limite_palavras])
