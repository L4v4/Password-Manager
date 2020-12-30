from typing import List, Optional
from collections.abc import Callable


class Handler:
    _counter = 0

    def __init__(self, func) -> None:
        super().__init__()
        self.id = Handler._counter
        Handler._counter += 1
        self.update = func

    def __eq__(self, other) -> bool:
        return type(other) is Handler and self.id == other.id


class Event:
    def __init__(self):
        super().__init__()
        self._observers: List[Handler] = list()

    def subscribe(self, observer: Handler) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Handler) -> None:
        self._observers.remove(observer)

    def invoke(self, *args, **kwargs) -> None:
        for observer in self._observers:
            observer.update(*args, **kwargs)
