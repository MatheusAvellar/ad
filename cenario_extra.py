import numpy as np
import heapq as hq

from cacheLRU import CacheLRU
from cacheFIFO import CacheFIFO
from cacheRandom import CacheRandom
from cacheStatic import CacheStatic

from util import parse_arguments, confidence_interval

N = 3
cache_size = 2
p = 0.9
mu = 1
alpha = 1
phi = 1
theta = float('inf')

n_events = 100

# faço broadcast desse conteudo para todas as caches
# mantenho também uma heap de prioridade dos eventos
# TODO: transformar (arrival_time, (cache, content)) em um objeto
def broadcast_content(events, caches, time, content, cid):
    for cache in caches:
        service_time = np.random.exponential(1/mu)
        arrival_time = time + service_time

        timeout = np.random.exponential(1/alpha)
        timeout_time = time + timeout

        hq.heappush(events, (arrival_time, (cache, cid, content, timeout_time)))

def simulate_cenario(CacheType):
    events = []
    means_response_time = []
    hq.heapify(events)
    contents = [f"c{i}" for i in range(1,N+1)]

    initial_contents = [(0, contents[i]) for i in range(cache_size)]
    cache1 = CacheCamada(1, initial_contents, size=cache_size, theta=theta, mu=mu, n_children=2)
    cache2 = CacheCamada(2, initial_contents, size=cache_size, theta=theta, mu=mu, n_children=2)
    caches = [cache1, cache2]

    # sorteia primeiro conteúdo a ser processado
    content = np.random.choice(contents)

    content_id = 0
    broadcast_content(events, caches, 0, content, content_id)
    for _ in range(n_events):
        # processa próximo evento
        try:
            time, (cache, cid, content, timeout) = hq.heappop(events)
            if time > timeout:
                # deu timeout, devemos enviar para o servidor a parte
                time_fallback_server = time + np.random.exponential(1/phi)
                cache.misses[cid] = 1
                # print(f'Conteúdo servido pelo servidor a parte no tempo {time_fallback_server}')
                response_time = time_fallback_server
            else:
                # print(f"[{time}] Adicionando {content} a cache {cache.id}")
                response_time = cache.add((time, content), cid, len(events))

            # service_times = remove_pending(events, content, time)

            means_response_time.append(response_time)
            # means_response_time += service_times

        except:
            print("eventos vazio")

        finally:
            # sorteia processo conteudo a ser processado
            content = np.random.choice(contents)
            content_id += 1
            broadcast_content(events, caches, time, content, content_id)

    # processa as requisições restantes
    while len(events) > 0:
        # processa próximo evento
        time, (cache, cid, content, timeout) = hq.heappop(events)

        if time > timeout:
            # deu timeout, devemos enviar para o servidor a parte
            time_fallback_server = np.random.exponential(1/phi)
            response_time = time_fallback_server
        else:
            # print(f"[{time}] Adicionando {content} a cache {cache.id}")
            response_time = cache.add((time, content), cid, len(events))

        means_response_time.append(response_time)

    # computa perdas
    # misses = 0
    # for cid in range(content_id):
    #     if sum([cache.misses[cid] for cache in caches]) == len(caches):
    #         misses += 1
    return np.mean(means_response_time)

def run_simulation(cache_type, n_sims=100, n_rounds=100):
    cache_class_mapping = {
        "FIFO": CacheFIFO,
        "LRU": CacheLRU,
        "RAND": CacheRandom,
        "STATIC": CacheStatic
    }
    Cache = cache_class_mapping[cache_type]

    means = []
    for _ in range(n_rounds):
        response_time_total = 0
        # misses_l = []
        for _ in range(n_sims):
            response_time_mean = simulate_cenario3(Cache)
            response_time_total += response_time_mean
            # misses_l.append(unit_miss/n_events)
        means.append((response_time_mean/n_sims)/n_events)

    print("Média:", np.mean(means))
    print("Intervalo de confiança:", confidence_interval(means))

    return means

def main(args):
    global N
    global n_events
    global lambda_
    global cache_size
    global p
    global mu
    global alpha
    global phi
    global theta

    N = args.N
    n_events = args.n_events
    lambda_ = args.lambda_
    cache_size = args.cache_size
    p = args.p
    mu = args.mu
    alpha = args.alpha
    phi = args.phi
    theta = args.theta

    run_simulation(args.cache, n_sims=args.n_sims, n_rounds=args.n_rounds)

if __name__ == "__main__":
    main(parse_arguments())