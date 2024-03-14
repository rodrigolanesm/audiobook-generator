# Fiz com um limitador de palavras pra testar

from ebooklib import epub
import re, ebooklib

def extrair_texto_epub(arquivo_epub, limite_palavras):
    # Abre o arquivo EPUB
    livro = epub.read_epub(arquivo_epub)

    texto_completo = ''

    # Itera sobre cada item do livro (geralmente cada item é um arquivo HTML)
    for item in livro.get_items():
        # Verifica se o item é HTML
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Extrai o conteúdo do item
            texto = item.get_body_content().decode('utf-8')
            # Remove tags HTML usando expressão regular
            texto_sem_tags = re.sub('<[^<]+?>', '', texto)
            # Adiciona o texto sem tags ao texto completo
            texto_completo += texto_sem_tags

            # Quebra o texto em palavras
            palavras = texto_completo.split()
            # Verifica se o número de palavras já ultrapassou o limite
            if len(palavras) >= limite_palavras:
                break

    # Retorna as primeiras 'limite_palavras' palavras do texto
    return ' '.join(palavras[:limite_palavras])

# Caminho para o arquivo EPUB de entrada
arquivo_epub = 'O_Pequeno_Príncipe.epub'
# Limite de palavras para extração
limite_palavras = 1000

# Chama a função para extrair texto do arquivo EPUB
texto_extraido = extrair_texto_epub(arquivo_epub, limite_palavras)

# Imprime o texto extraído
print(texto_extraido)

