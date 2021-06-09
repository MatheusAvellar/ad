import heapq as hq

from cache import Cache

class CacheLRU(Cache):
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

    # def add(self, event, cid, n_pending_requests):
    #     ''' Adiciona evento (arrival_time, content) a cache'''
    #     arrival_time, content = event
    #     if len(self._events) == self._size:
    #         if content not in self.events():
    #             request_type = 'miss'
    #             self.misses[cid] = 1
    #             removed_element = hq.heapreplace(self._events, event)
    #             # print(f"Elemento {removed_element} removido da cache {self.id}")
    #             # print(f"Elemento {event} adicionado a cache {self.id}")
    #         else:
    #             request_type = 'hit'
    #             self.misses[cid] = 0
    #             self._update_entry(event)

    #     else:
    #         request_type='miss'
    #         self.misses[cid] = 1
    #         hq.heappush(self._events, event)
    #         # print(f"Elemento {event} adicionado a cache {self.id}")

    #     write_log(tempo=arrival_time, cache=self.id, cid=cid,
    #         tipo_requisicao=request_type, n_requisicoes_pendentes=n_pending_requests)

    #     self._last_arrival = max(self._last_arrival, event[0])