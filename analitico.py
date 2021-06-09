import math

def arranjo(n, k):
    return math.factorial(n)/math.factorial(n-k)

qt_conteudos = 3
capacidade_cache = 2
qt_caches = 2
prob_sucesso = 0.9

qt_estados = arranjo(qt_conteudos, capacidade_cache)
prob_cache_miss = (arranjo(qt_conteudos-1, capacidade_cache)/qt_estados)*prob_sucesso + (1-prob_sucesso)

print('Quantidade de estados:', qt_estados)
print('Probabilidade de cache miss (falha em uma cache):', prob_cache_miss)
print('Probabilidade de user miss (falha em todas as caches):', prob_cache_miss**qt_caches)
