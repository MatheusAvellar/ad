import numpy as np
import heapq as hq

from cache import Cache

class CacheRandom(Cache):
    def _handle_hit(self, event):
        return

    def _handle_miss(self, event):
        index_remove_event = np.random.randint(len(self._events))
        self._events[index_remove_event] = event
