import random

def to_list(estado_cache: str) -> list:
    lista = []
    for i in range(int(len(estado_cache)/2)):
        lista.append(estado_cache[i*2]+estado_cache[i*2+1])
    return lista

def to_str(estado_cache: list) -> str:
    return ''.join(estado_cache)

def insere_FIFO_ou_LRU(estado_cache: str, conteudo: str) -> str:
    if conteudo in estado_cache:
        raise Exception('Conteúdo já está na cache')
    return conteudo + estado_cache[:-2]

def atualiza_LRU(estado_cache: str, conteudo: str) -> str:
    if conteudo not in estado_cache:
        raise Exception('Conteúdo não está na cache')
    return conteudo + estado_cache.replace(conteudo, '')

def insere_Random(estado_cache: str, conteudo: str) -> str:
    if conteudo in estado_cache:
        raise Exception('Conteúdo já está na cache')
    lista = to_list(estado_cache)
    i = random.randrange(len(lista))
    lista[i] = conteudo
    return to_str(lista)

def pega_cache1(estado: str):
    metade = int(len(estado)/2)
    return estado[:metade]

def pega_cache2(estado: str):
    metade = int(len(estado)/2)
    return estado[metade:]

def monta_estados(conteudos: list):
    estados = []
    for cache1 in monta_estados_cache(conteudos):
        for cache2 in monta_estados_cache(conteudos):
            estados.append(cache1+cache2)
    return estados

def monta_estados_cache(conteudos: list):
    estados = []
    for conteudo1 in conteudos:
        for conteudo2 in conteudos:
            if conteudo1 != conteudo2:
                estados.append(conteudo1+conteudo2)
    return estados

conteudos = ['c1', 'c2', 'c3']

# estados = monta_estados(conteudos)

estado = 'c1c2c3c2c4c1'

print(insere_Random(pega_cache1(estado), 'c4'))

