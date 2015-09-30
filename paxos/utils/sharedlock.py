from threading import Condition, Lock


class SharedLock(object):
    def __init__(self):
        self._condition = Condition(Lock())

        self._is_locked = False

    def acquire(self):
        self._condition.acquire()
        try:
            while self._is_locked:
                self._condition.wait()
            self._is_locked = True
        finally:
            self._condition.release()

    def release(self):
        self._condition.acquire()
        try:
            self._is_locked = False
            self._condition.notify()
        finally:
            self._condition.release()
