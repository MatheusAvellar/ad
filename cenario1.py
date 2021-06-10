import numpy as np
import heapq as hq

from cacheLRU import CacheLRU
from cacheFIFO import CacheFIFO
from cacheRandom import CacheRandom
from cacheStatic import CacheStatic

from util import parse_arguments, confidence_interval

lambda_ = None
N = None
cache_size = None

n_events = None

# faço broadcast desse conteudo para todas as caches
# mantenho também uma heap de prioridade dos eventos
# TODO: transformar (arrival_time, (cache, content)) em um objeto
def broadcast_content(events, caches, time, content, cid):
    for cache in caches:
        arrival_time = time + np.random.exponential(1/lambda_)
        hq.heappush(events, (arrival_time, (cache, cid, content)))

def simulate_cenario1(CacheType):
    events = []
    hq.heapify(events)
    contents = [f"c{i}" for i in range(1,N+1)]

    copy_contents = contents.copy()
    initial_contents = [(0, copy_contents.pop(np.random.randint(len(copy_contents)))) for i in range(cache_size)]
    cache1 = CacheType(1, initial_contents, size=cache_size)
    cache2 = CacheType(2, initial_contents, size=cache_size)
    caches = [cache1, cache2]

    # sorteia primeiro conteúdo a ser processado
    content = np.random.choice(contents)

    content_id = 0
    broadcast_content(events, caches, 0, content, content_id)
    for _ in range(n_events):
        # processa próximo evento
        time, (cache, cid, content) = hq.heappop(events)
        # print(f"[{time}] Adicionando {content} a cache {cache.id}")
        cache.add((time, content), cid, len(events))

        # sorteia processo conteudo a ser processado
        content = np.random.choice(contents)
        content_id += 1
        broadcast_content(events, caches, time, content, content_id)

    # processa as requisições restantes
    while len(events) > 0:
        # processa próximo evento
        time, (cache, cid, content) = hq.heappop(events)
        # print(f"[{time}] Adicionando {content} a cache {cache.id}")
        cache.add((time, content), cid, len(events))

    # computa perdas
    misses = 0
    for cid in range(content_id):
        try:
            if sum([cache.misses[cid] for cache in caches]) == len(caches):
                misses += 1
        except:
            misses += 1
    return misses

def run_simulation(cache_type, n_sims=100, n_rounds=30):
    cache_class_mapping = {
        "FIFO": CacheFIFO,
        "LRU": CacheLRU,
        "RAND": CacheRandom,
        "STATIC": CacheStatic
    }
    Cache = cache_class_mapping[cache_type]

    means = []
    for _ in range(n_rounds):
        misses = 0
        for _ in range(n_sims):
            unit_miss = simulate_cenario1(Cache)
            misses += unit_miss
        means.append((misses/n_sims)/n_events)

    print("Média:", np.mean(means))
    print("Intervalo de confiança:", confidence_interval(means))

    return means

def main(args):
    global N
    global n_events
    global lambda_
    global cache_size

    N = args.N
    n_events = args.n_events
    lambda_ = args.lambda_
    cache_size = args.cache_size

    return run_simulation(args.cache, n_sims=args.n_sims, n_rounds=args.n_rounds)

if __name__ == "__main__":
    main(parse_arguments())