import numpy as np
import heapq as hq

from cache import Cache

class CacheRandom(Cache):
    def _handle_hit(self, event):
        return

    def _handle_miss(self, event):
        index_remove_event = np.random.randint(len(self._events))
        self._events[index_remove_event] = event

    # def add(self, event, cid):
    #     ''' Adiciona evento (arrival_time, content) a cache'''
    #     if len(self._events) == self._size:
    #         if event[1] not in self.events():
    #             self.misses[cid] = 1
    #             index_remove_event = np.random.randint(len(self._events))
    #             self._events[index_remove_event] = event
    #             # print(f"Elemento {removed_element} removido da cache {self.id}")
    #             # print(f"Elemento {event} adicionado a cache {self.id}")
    #         else:
    #             self.misses[cid] = 0
    #             # print(f"Elemento {event} já presente na cache {self.id}")

    #     else:
    #         self.misses[cid] = 1
    #         hq.heappush(self._events, event)
    #         # print(f"Elemento {event} adicionado a cache {self.id}")

    #     self._last_arrival = max(self._last_arrival, event[0])