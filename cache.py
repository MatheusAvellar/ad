import numpy as np
import heapq as hq

from util import write_log

# [ref] heapq: https://docs.python.org/3/library/heapq.html#basic-examples
class Cache:
    def __init__(self, id, events, size=2, theta=float('inf'), mu=1):
        ''' Inicializa cache
        
        Parametros:
            id (str): identificador da cache
            events (tuple): valores inicias a serem contidos na cache
                do tipo (arrival_time, content)
            size (int): capacidade da cache
        '''
        self.id = id
        self._events = events
        hq.heapify(self._events)
        self._size = size
        self.theta = theta
        self.mu = mu
        self.misses = {}

    def next_execution(self):
        return self._events[0]

    def events(self):
        for event in self._events:
            yield event[1]

    def _handle_empty(self, event):
        hq.heappush(self._events, event)
        return 0

    def _handle_hit(self, event):
        ''' Função a ser implementa nas caches que herdam a cache principal'''
        return 0

    def _handle_miss(self, event):
        ''' Função a ser implementa nas caches que herdam a cache principal'''
        return 0

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
                    response_time = np.random.exponential(1/self.theta)
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