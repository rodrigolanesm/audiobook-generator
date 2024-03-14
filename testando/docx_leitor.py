# Fiz com um limitador de palavras pra testar

from docx import Document

def extrair_texto_docx(arquivo_docx, limite_palavras):
    # Abre o arquivo DOCX
    doc = Document(arquivo_docx)

    texto_completo = ''

    # Itera sobre cada parágrafo do documento
    for paragraph in doc.paragraphs:
        # Adiciona o texto do parágrafo ao texto completo
        texto_completo += paragraph.text + ' '

        # Quebra o texto em palavras
        palavras = texto_completo.split()
        # Verifica se o número de palavras já ultrapassou o limite
        if len(palavras) >= limite_palavras:
            break

    # Retorna as primeiras 'limite_palavras' palavras do texto
    return ' '.join(palavras[:limite_palavras])

# Caminho para o arquivo DOCX de entrada
arquivo_docx = 'exemplo.docx'
# Limite de palavras para extração
limite_palavras = 1000

# Chama a função para extrair texto do arquivo DOCX
texto_extraido = extrair_texto_docx(arquivo_docx, limite_palavras)

# Imprime o texto extraído
print(texto_extraido)
