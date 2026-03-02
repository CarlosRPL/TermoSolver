import math
import json
import os

def gettermo(tentativa: str, acerto: str) -> list[int]:
    resultado = [0] * 5
    restantes = {}

    for i in range(5):
        if tentativa[i] == acerto[i]:
            resultado[i] = 2
        else:
            letra = acerto[i]
            restantes[letra] = restantes.get(letra, 0) + 1

    for i in range(5):
        if resultado[i] == 0:
            letra = tentativa[i]
            if restantes.get(letra, 0) > 0:
                resultado[i] = 1
                restantes[letra] -= 1

    return resultado
def contar_resultados(tentativa, vocabulario):
    contagem = {}

    for palavra in vocabulario:
        resultado = tuple(gettermo(tentativa, palavra))

        contagem[resultado] = contagem.get(resultado, 0) + 1

    return contagem

def calculandoinfo(tenta,voc):
    soma=0
    dict=contar_resultados(tenta,voc)
    m=len(voc)
    for i in dict:
        v=dict.get(i,0)
        info=(v/m)*(math.log(m/v,2))
        soma+=info
    return soma
vocabulario=set()
entrada="res/lexico-5-letras"
with open(entrada, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        palavras = linha.split()
        vocabulario.update(palavras)
def calcular_todos(voc):
    resultados = []

    for p in voc:
        info = calculandoinfo(p, voc)
        resultados.append((info, p))

    return resultados
def gerar_vocabulario_possivel(tentativa, resultado, vocabulario):
    resultado = list(resultado)  # garante comparação correta
    novo_vocabulario = set()

    for palavra in vocabulario:
        if gettermo(tentativa, palavra) == resultado:
            novo_vocabulario.add(palavra)

    return novo_vocabulario
def game(acerto,voc):
    n=True
    nvoc=voc
    i=0
    while(n):
        tentativa = max(calcular_todos(nvoc), key=lambda x: x[0])[1]
        if (tentativa==acerto):
            break
        res=gettermo(tentativa,acerto)
        tvoc=gerar_vocabulario_possivel(tentativa,res,nvoc)
        v=len(tvoc)
        m=len(nvoc)
        nvoc=tvoc
        if v == 0:
            print("⚠️ Vocabulário ficou vazio — impossível continuar")
            print("Tentativa:", tentativa)
            print("Resultado:", res)
            break
        inf=(math.log(m/v,2))
        print(tentativa,res,inf)
        i+=1
    return 
def precalcular_primeiros_chutes(vocabulario, arquivo_saida="top15.json"):
    if os.path.exists(arquivo_saida):
        print("Top 15 já calculado.")
        return

    print("Calculando top 15 primeiros chutes...")

    resultados = calcular_todos(vocabulario)
    resultados.sort(reverse=True)  # maior informação primeiro

    top15 = resultados[:15]

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(top15, f, ensure_ascii=False, indent=2)

    print("Top 15 salvo em", arquivo_saida)