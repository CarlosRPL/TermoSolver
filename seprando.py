import unicodedata

# Arquivo de entrada e saída
entrada = "res/lexico"
saida = "res/lexico-5-letras"

# Função para remover acentos e Ç
def remover_acentos(palavra):
    nfkd = unicodedata.normalize("NFKD", palavra)
    return "".join(
        c for c in nfkd
        if not unicodedata.combining(c)
    ).replace("ç", "c").replace("Ç", "C")

# Conjunto para palavras únicas
vocabulario = set()

# Lê o arquivo de entrada
with open(entrada, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        palavras = linha.split()
        vocabulario.update(palavras)

# Filtra palavras com exatamente 5 letras (ANTES de remover acentos)
palavras_5_letras = [p for p in vocabulario if len(p) == 5]

# Remove acentos depois da filtragem
palavras_normalizadas = {
    remover_acentos(p) for p in palavras_5_letras
}

# Escreve no arquivo de saída
with open(saida, "w", encoding="utf-8") as arquivo:
    for palavra in sorted(palavras_normalizadas):
        arquivo.write(palavra + "\n")
print(len(palavras_5_letras))
