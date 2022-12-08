from __future__ import annotations
from typing import TypeVar, Generic, Callable
import random
from APIs.ExternalAPIs.WorkerPool.pooled_worker import PooledWorker

T = TypeVar('T', bound=PooledWorker)


class Pool(Generic[T]):
    def __init__(self, worker_creation_func: Callable[[], T], max_workers: int):
        """
        Creates a new pool.
        :param worker_creation_func: How to create new workers if needed
        :param max_workers: The maximum number of workers
        """
        self._workers: [T] = []
        self._worker_creation_func = worker_creation_func
        self._max_workers = max_workers

    def get_free_worker(self) -> T:
        """
        Returns one of the free workers in the pool,
        if none is free - returns a random worker.

        :return: T instance
        """

        #  Try to accuire one of the workers
        for worker in self._workers:
            worker: T = worker

            if not worker.lock.locked():
                return worker

        #  If none is available, try to add new one
        if len(self._workers) < self._max_workers:
            self._workers.append(self._worker_creation_func())
            return self._workers[-1]

        #  If none of the above options work,
        #  return a random worker.
        return random.choice(self._workers)
