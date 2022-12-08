from __future__ import annotations
import threading


class PooledWorker:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, type, value, tb):
        self.lock.release()
