import numpy as np
import heapq as hq

from util import write_log

# [ref] heapq: https://docs.python.org/3/library/heapq.html#basic-examples
class Cache:
    def __init__(self, id, events, size=2):
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
        self._last_arrival = 0
        self.misses = {}

    def next_execution(self):
        return self._events[0]

    def events(self):
        for event in self._events:
            yield event[1]

    def _handle_hit(self, event):
        ''' Função a ser implementa nas caches que herdam a cache principal'''
        return

    def _handle_miss(self, event):
        ''' Função a ser implementa nas caches que herdam a cache principal'''
        return

    def add(self, event, cid, n_pending_requests, p=1):
        ''' Adiciona evento (arrival_time, content) a cache'''
        arrival_time, content = event
        if np.random.random() <= p:
            if len(self._events) == self._size:
                if content not in self.events():
                    request_type = 'miss'
                    self.misses[cid] = 1
                    self._handle_miss(event)
                else:
                    request_type = 'hit'
                    self.misses[cid] = 0
                    self._handle_hit(event)

            else:
                request_type = 'miss'
                self.misses[cid] = 1
                hq.heappush(self._events, event)
        else:
            request_type = 'miss'
            self.misses[cid] = 1

        write_log(tempo=arrival_time, cache=self.id, cid=cid,
            tipo_requisicao=request_type, n_requisicoes_pendentes=n_pending_requests)

        self._last_arrival = max(self._last_arrival, event[0])