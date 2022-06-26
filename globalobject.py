from PyQt5 import QtCore
import functools

@functools.lru_cache()
class GlobalObject(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self._events = {}
        self._user = ""

    def addEventListener(self, name, func):
        if name not in self._events:
            self._events[name] = [func]
        else:
            self._events[name].append(func)

    def dispatchEvent(self, name):
        functions = self._events.get(name, [])
        for func in functions:
            QtCore.QTimer.singleShot(0, func)

    def addUser(self, usr):
        self._user = usr

    def getUser(self):
        return self._user