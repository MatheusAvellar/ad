import numpy as np
import heapq as hq

from cacheFIFO import CacheFIFO
from cacheLRU import CacheLRU
from cacheRandom import CacheRandom

from util import parse_arguments, confidence_interval

lambda_ = 1
N = 3
cache_size = 2
p = 0.9

contents = [f"c{i}" for i in range(1,N+1)]

n_events = 10000

# faço broadcast desse conteudo para todas as caches
# mantenho também uma heap de prioridade dos eventos
# TODO: transformar (arrival_time, (cache, content)) em um objeto
def broadcast_content(events, caches, time, content, cid):
    for cache in caches:
        arrival_time = time + np.random.exponential(1/lambda_)
        hq.heappush(events, (arrival_time, (cache, cid, content)))

def simulate_cenario2(CacheType):
    events = []
    hq.heapify(events)

    initial_contents = [(0, contents[i]) for i in range(cache_size)]
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
        cache.add((time, content), cid, len(events), p=p)

        # sorteia processo conteudo a ser processado
        content = np.random.choice(contents)
        content_id += 1
        broadcast_content(events, caches, time, content, content_id)

    # processa as requisições restantes
    while len(events) > 0:
        # processa próximo evento
        time, (cache, cid, content) = hq.heappop(events)
        cache.add((time, content), cid, len(events), p=p)

    # computa perdas
    misses = 0
    for cid in range(content_id):
        if sum([cache.misses[cid] for cache in caches]) == len(caches):
            misses += 1
    return misses

def run_simulation(cache_type, n_sims=100, n_rounds=100):
    cache_class_mapping = {
        "FIFO": CacheFIFO,
        "LRU": CacheLRU,
        "RAND": CacheRandom,
    }
    Cache = cache_class_mapping[cache_type]

    means = []
    for _ in range(n_rounds):
        misses = 0
        for _ in range(n_sims):
            unit_miss = simulate_cenario2(Cache)
            misses += unit_miss
        means.append((misses/n_sims)/n_events)

    return means

def main():
    global N
    global n_events
    global lambda_
    global cache_size
    global p
    args = parse_arguments()

    N = args.N
    n_events = args.n_events
    lambda_ = args.lambda_
    cache_size = args.cache_size
    p = args.p

    run_simulation(args.cache, n_sims=args.n_sims, n_rounds=args.n_rounds)

if __name__ == "__main__":
    main()