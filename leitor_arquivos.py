"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 21/03/2024
Última Atualização: 26/03/2024 - 19:33:55
Linguagem: Python

Descrição: Realizar a leitura dos arquivos

"""

from ebooklib import epub
from docx import Document
import fitz, re, ebooklib

class LeitorArquivos:
    
    extensoes = ["EPUB", "DOCX", "PDF", "MOBI"]
  
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

    
    def extrair_texto_docx(arquivo_docx, limite_palavras, posicao_leitura):
        doc = Document(arquivo_docx)
        texto_completo = ''
        for paragraph in doc.paragraphs:
            texto_completo += paragraph.text + ' '
            palavras = texto_completo.split()
            if len(palavras) >= limite_palavras:
                break
        return ' '.join(palavras[posicao_leitura:limite_palavras + posicao_leitura])

    
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
