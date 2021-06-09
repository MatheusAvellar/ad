import heapq as hq
import numpy as np

from cache import Cache
from util import write_log

class CacheCamada(Cache):
    def __init__(self, id_, events, size=2, theta=float('inf'), mu=1, n_children=0, level=0, max_level=3):
        super().__init__(id_, events, size=size, theta=theta, mu=mu)
        self._level = level
        self._max_level = max_level
        self._n_children = n_children
        self.children_cache = []
        if level < max_level:
            self._init_children()

    def _init_children(self):
        for _ in range(self._n_children):
            id_ = f'{self.id}{self._level}'
            self.children_cache.append(
                CacheCamada(id_, self._events, size=self._size, theta=self.theta*3, mu=self.mu*3,
                    n_children=self._n_children, level=self._level+1, max_level=self._max_level)
            )

    def _update_entry(self, event):
        ''' Usado apenas no caso da LRU '''
        for i in range(len(self._events)):
            e = self._events[i]
            if event[1] == e[1]:
                self._events[i] = event
        hq.heapify(self._events)

    def _handle_hit(self, event):
        self._update_entry(event)

    def _handle_miss(self, event):
        hq.heapreplace(self._events, event)

    def add(self, event, cid, n_pending_requests, p=1):
        ''' Adiciona evento (arrival_time, content) a cache'''
        arrival_time, content = event
        response_time = 0
        if np.random.random() <= p:
            if len(self._events) == self._size:
                if content not in self.events():
                    request_type = 'miss'
                    self.misses[cid] = 1
                    self._handle_miss(event)
                    response_time = min([cache.add(event, cid, n_pending_requests, p=p)
                        for cache in self.children_cache])
                else:
                    request_type = 'hit'
                    self.misses[cid] = 0
                    self._handle_hit(event)
                    response_time = 0

            else:
                request_type = 'miss'
                self.misses[cid] = 1
                self._handle_empty(event)
                response_time = 0
        else:
            request_type = 'miss'
            self.misses[cid] = 1

        downstream_time = np.random.exponential(1/self.mu)
        response_time += downstream_time
        write_log(tempo=arrival_time, cache=self.id, cid=cid,
            tipo_requisicao=request_type, n_requisicoes_pendentes=n_pending_requests)

        return response_time