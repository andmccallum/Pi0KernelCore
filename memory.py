
from collections import deque
class LernPi0n:
    def __init__(self, size=1000):
        self.buf = deque(maxlen=size)
    def put(self, tile):
        self.buf.append(tile)
    def query(self, theta=None, C_hat=None):
        return list(self.buf)
