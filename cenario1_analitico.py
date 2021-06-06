import random
import numpy as np

def pega_aleatorio(conteudos: list):
    return conteudos[random.randrange(len(conteudos))]

def to_list(estado: str) -> list:
    lista = []
    for i in range(int(len(estado)/2)):
        lista.append(estado[i*2]+estado[i*2+1])
    return lista

def to_str(estado: list) -> str:
    return ''.join(estado)

def insere_FIFO_ou_LRU(estado: str, conteudo: str) -> str:
    if conteudo in estado:
        raise Exception('Conteúdo já está na cache')
    return conteudo + estado[:-2]

def atualiza_LRU(estado: str, conteudo: str) -> str:
    if conteudo not in estado:
        raise Exception('Conteúdo não está na cache')
    return conteudo + estado.replace(conteudo, '')

def insere_Random(estado: str, conteudo: str) -> str:
    if conteudo in estado:
        raise Exception('Conteúdo já está na cache')
    lista = to_list(estado)
    i = random.randrange(len(lista))
    lista[i] = conteudo
    return to_str(lista)

def processa_FIFO(estado: str, conteudo: str) -> (str, bool):
    if conteudo in estado:
        return estado, True
    else:
        return insere_FIFO_ou_LRU(estado, conteudo), False

def processa_LRU(estado: str, conteudo: str) -> (str, bool):
    if conteudo in estado:
        return atualiza_LRU(estado, conteudo), True
    else:
        return insere_FIFO_ou_LRU(estado, conteudo), False

def monta_estados(conteudos: list) -> list:
    estados = []
    for conteudo1 in conteudos:
        for conteudo2 in conteudos:
            if conteudo1 != conteudo2:
                estados.append(conteudo1+conteudo2)
    return estados

def simula(conteudos: list, estado_inicial_cache1: str, estado_inicial_cache2: str, f_processa):
    estado_cache1 = estado_inicial_cache1
    estado_cache2 = estado_inicial_cache2
    falhas = 0
    for i in range(1000):
        requisicao = pega_aleatorio(conteudos)
        estado_cache1, hit_cache1 = f_processa(estado_cache1, requisicao)
        estado_cache2, hit_cache2 = f_processa(estado_cache2, requisicao)
        if not hit_cache1 and not hit_cache2:
            falhas += 1
    return falhas/1000

def pega_estado_aleatorio(conteudos: list) -> str:
    estados = monta_estados(conteudos)
    return estados[random.randrange(len(estados))]

conteudos = ['c1', 'c2', 'c3']

simulacoes = 10000
falhas = 0
for i in range(simulacoes):
    cache1 = pega_estado_aleatorio(conteudos)
    cache2 = cache1
    cache2 = pega_estado_aleatorio(conteudos)
    falhas += simula(conteudos, cache1, cache2, processa_FIFO)
print('Média de falhas:', falhas/simulacoes)

