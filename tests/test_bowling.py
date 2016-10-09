import pytest

from bowling import Frame, ObservableStream, Observer


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


@pytest.mark.parametrize('values, expected_is_finished', [
    ([10], True),
    ([9], False),
])
def test_frame(values, expected_is_finished):
    throws = _make_throws(values)
    frame = Frame()
    for _ in values:
        frame.add_throw(throws)
    assert frame.is_finished is expected_is_finished


def _make_throws(values):
    stream = ObservableStream()
    for one_value in values:
        stream.add(one_value)
    return stream
