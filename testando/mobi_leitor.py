# Fiz com um limitador de palavras pra testar

import fitz  # PyMuPDF

def extrair_texto_mobi(arquivo_mobi, limite_palavras):
    texto_completo = ''
    # Abre o arquivo MOBI
    doc = fitz.open(arquivo_mobi)

    # Itera sobre cada página do documento
    for page_num in range(len(doc)):
        # Extrai texto da página
        texto_pagina = doc[page_num].get_text()

        # Adiciona o texto da página ao texto completo
        texto_completo += texto_pagina

        # Quebra o texto em palavras
        palavras = texto_completo.split()
        # Verifica se o número de palavras já ultrapassou o limite
        if len(palavras) >= limite_palavras:
            break

    # Retorna as primeiras 'limite_palavras' palavras do texto
    return ' '.join(palavras[:limite_palavras])

# Caminho para o arquivo MOBI de entrada
arquivo_mobi = 'OPequenoPríncipe.mobi'
# Limite de palavras para extração
limite_palavras = 1000

# Chama a função para extrair texto do arquivo MOBI
texto_extraido = extrair_texto_mobi(arquivo_mobi, limite_palavras)

# Imprime o texto extraído
print(texto_extraido)
