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

    def __next__(self):
        try:
            value = self.values.popleft()
        except IndexError:
            raise StopIteration
        for observer in self.observers:
            observer.on_new_value(self, value)
        return value


class Observer(object):
    def on_new_value(self, observable, value):
        raise NotImplementedError
