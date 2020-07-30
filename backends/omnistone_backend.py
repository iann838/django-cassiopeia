from functools import wraps
from typing import Callable, Any, TypeVar, Tuple
from threading import Lock
from collections import defaultdict
import datetime
import copy

from logging import getLogger

LOGGER = getLogger(__name__)
T = TypeVar("T")

class OmnistoneBackend(object):
    def __init__(self, max_entries: int = None, cull_frecuency: int = None, logs_enabled: bool = False) -> None:
        self._data = dict()
        self._lock = Lock()
        self._max_entries = max_entries if max_entries is not None else 6000
        self._cull_frecuency = cull_frecuency if cull_frecuency is not None else 2
        self._cull_lock = [False, datetime.datetime.now()]
        self._logs_enabled = logs_enabled

    def put(self, omnikey: Tuple, value: Any, timeout: int = -1) -> None:
        if timeout != 0:
            with self._lock:
                if timeout != -1:
                    timeout = datetime.timedelta(seconds=timeout)
                if self.allowed():
                    self._data[omnikey] = (value, timeout, datetime.datetime.now(), datetime.datetime.now())
                    if self._logs_enabled:
                        LOGGER.warn(f"[Trace: django_cassiopeia > Omnistone] PUT: <core {omnikey[0].__name__}>")
            if len(self._data) > self._max_entries and self.allowed():
                LOGGER.warn(f"[Trace: django_cassiopeia > Omnistone] VACUUM: Expiration check starts")
                self._cull_lock = [True, datetime.datetime.now()]
                self.expire()
                if len(self._data) > self._max_entries - self._max_entries/self._cull_frecuency:
                    self.cull()

    def get(self, omnikey: Tuple) -> Any:
        with self._lock:
            item, timeout, entered, lastpull = self._data[omnikey]
            if self._logs_enabled:
                LOGGER.warn(f"[Trace: django_cassiopeia > Omnistone] GET: <core {omnikey[0].__name__}>")
            now = datetime.datetime.now()
            if timeout == -1:
                self._data[omnikey] = (item, timeout, entered, now)
                return item
            elif now > entered + timeout:
                del self._data[omnikey]
                LOGGER.warn(f"[Trace: django_cassiopeia > Omnistone] EXPIRE: <core {omnikey[0].__name__}>")
                raise KeyError
            else:
                self._data[omnikey] = (item, timeout, entered, now)
                return item

    def delete(self, omnikey: Tuple) -> None:
        with self._lock:
            del self._data[omnikey]
            LOGGER.warn(f"[Trace: django_cassiopeia > Omnistone] DELETE: <core {omnikey[0].__name__}>")

    def contains(self, omnikey: Tuple) -> bool:
        with self._lock:
            return self._data.__contains__(omnikey)

    def expire(self, type: Any = None):
        before = self._logs_enabled
        self._logs_enabled = False
        for omnikey in self._data.keys():
            if type is not None and key[0] == type:
                self.get(omnikey)
            else:
                self.get(omnikey)
        self._logs_enabled = before

    def allowed(self):
        if not self._cull_lock[0]:
            return True
        elif self._cull_lock[0] and datetime.datetime.now() > self._cull_lock[1] + datetime.timedelta(seconds=30):
            self._cull_lock[0] = False
            return True
        else:
            return False

    def cull(self, type: Any = None):
        with self._lock:
            data = copy.copy(self._data)
        lru = sorted(data.keys(), key=lambda x: data[x][3])
        for key in lru[:int(len(data)/self._cull_frecuency)]:
            self.delete(key)
        self._cull_lock[0] = False


