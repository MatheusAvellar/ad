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
