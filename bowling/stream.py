from collections import deque


class ObservableStream(object):
    def __init__(self):
        self.observers = []
        self.values = deque()

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def add(self, value):
        self.values.append(value)

    def __iter__(self):
        return self

    def next(self):
        value = self.values.popleft()
        for observer in self.observers:
            observer.on_new_value(value)
        return value


class Observer(object):
    def on_new_value(self, value):
        raise NotImplementedError
