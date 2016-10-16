import pytest

from bowling import Frame, Game, LastFrame, ObservableStream, Observer


# TODO: unskip this test


class SavingObserver(Observer):
    def __init__(self, values):
        self.values = values

    def on_new_value(self, observable, value):
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
    ([0], False),
    ([0, 1], True),
    ([10, 10, 10], True),
])
def test_frame_is_finished(values, expected_is_finished):
    frame = _perform_throws_in_frame(values, Frame)
    assert frame.is_finished is expected_is_finished


@pytest.mark.parametrize('values,expected_throws', [
    ([10], [10]),
    # 9 is from another frame
    ([10, 9], [10]),
    ([9, 1], [9, 1]),
])
def test_frame_throws(values, expected_throws):
    frame = _perform_throws_in_frame(values, Frame)
    assert frame.throws == expected_throws


@pytest.mark.parametrize('values, expected_score', [
    ([10], 10),
    # next after strike
    ([10, 9], 19),
    # 2 next after strike
    ([10, 9, 9], 28),
    # only 2 next after strike
    ([10, 9, 9, 1], 28),
    # next after spare
    ([9, 1, 8], 18),
    # only 1 next after spare
    ([9, 1, 8, 1], 18),
])
def test_frame_score(values, expected_score):
    frame = _perform_throws_in_frame(values, Frame)
    assert frame.score == expected_score


def _perform_throws_in_frame(values, frame_class):
    throws = _make_throws(values)
    frame = frame_class()
    for _ in values:
        if not frame.is_finished:
            frame.add_throw(throws)
        else:
            next(throws)
    return frame


@pytest.mark.skip
@pytest.mark.parametrize('values, expected_is_finished', [
    ([0, 0], True),
    ([9], False),
    ([10], False),
    ([10, 10, 10], True),
    ([10, 0], False),
    ([9, 1], False),
    ([8, 1], True),
    ([9, 1, 10], True),
])
def test_last_frame_is_finished(values, expected_is_finished):
    throws = _make_throws(values)
    frame = LastFrame()
    for _ in values:
        frame.add_throw(throws)
    assert frame.is_finished is expected_is_finished


@pytest.mark.skip
@pytest.mark.parametrize('values,expected_frame_scores', [
    ([10], [10]),
    ([5, 4], [9]),
    ([5, 4, 6], [9]),
    ([10, 6, 3], [18]),
])
def test_game_score(values, expected_frame_scores):
    game = Game()
    for one_value in values:
        game.add_throw(one_value)
    assert game.get_frame_scores() == expected_frame_scores


def _make_throws(values):
    stream = ObservableStream()
    for one_value in values:
        stream.add(one_value)
    return stream
