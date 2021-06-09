import heapq as hq

from cache import Cache

class CacheFIFO(Cache):
    def _handle_hit(self, event):
        return

    def _handle_miss(self, event):
        hq.heapreplace(self._events, event)
