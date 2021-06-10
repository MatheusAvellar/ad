import numpy as np
import heapq as hq

import cenario3

from cacheLRU import CacheLRU
from cacheFIFO import CacheFIFO
from cacheRandom import CacheRandom
from cacheStatic import CacheStatic

from util import parse_arguments, confidence_interval

def main(args):
    args.theta = 1
    return cenario3.main(args)

if __name__ == "__main__":
    main(parse_arguments())