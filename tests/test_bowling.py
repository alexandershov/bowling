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
    observer.observe(stream)
    stream.add(1)
    assert values == []
    next(stream)
    assert values == [1]
