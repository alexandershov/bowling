from bowling import ObservableStream, Observer


class SavingObserver(Observer):
    def __init__(self, values):
        self.values = values

    def on_new_value(self, value):
        self.values.append(value)


def test_observer():
    values = []
    observer = SavingObserver(values)
    stream = ObservableStream()
    stream.register(observer)
    stream.add(1)
    stream.add(2)
    assert values == []
    next(stream)
    assert values == [1]
    stream.unregister(observer)
    assert next(stream) == 2
    assert values == [1]
