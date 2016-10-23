import pytest

from bowling import Frame, Game, LastFrame


@pytest.mark.parametrize('frame_class, values, expected_is_finished', [
    (Frame, [0], False),
    (Frame, [10], True),
    (Frame, [0, 1], True),
    (Frame, [9, 1], True),
    # strike in last frame gives another shot
    (LastFrame, [10], False),
    (LastFrame, [10, 0], False),
    (LastFrame, [10, 0, 0], True),
    # strike in last frame gives 2 another shots
    (LastFrame, [10, 10], False),
    # strike in last frame gives at most 2 another shots
    (LastFrame, [10, 10, 10], True),
    # spare in last frame gives another shot
    (LastFrame, [9, 1], False),
    # spare in last frame gives at most 1 another shot
    (LastFrame, [9, 1, 1], True),
    # not a strike/spare - only 2 shots
    (LastFrame, [1, 1], True),
])
def test_frame_is_finished(frame_class, values, expected_is_finished):
    frame = _perform_throws_in_frame(values, frame_class)
    assert frame.is_finished is expected_is_finished


@pytest.mark.parametrize('values, bonus_scores, expected_score', [
    ([10], [3], 13),
])
def test_frame_add_bonus_score(values, bonus_scores, expected_score):
    frame = _perform_throws_in_frame(values, Frame)
    for to_add in bonus_scores:
        frame.add_bonus_score(to_add)
    assert frame.score == expected_score


@pytest.mark.parametrize('frame_class, values, expected_throws', [
    (Frame, [9], [9]),
    (Frame, [9, 1], [9, 1]),
    (Frame, [10], [10]),
    (LastFrame, [0], [0]),
    (LastFrame, [1, 2], [1, 2]),
    (LastFrame, [10, 10, 10], [10, 10, 10]),
])
def test_frame_throws(frame_class, values, expected_throws):
    frame = _perform_throws_in_frame(values, frame_class)
    assert frame.throws == expected_throws


@pytest.mark.parametrize('frame_class, values, expected_score', [
    (Frame, [8, 1], 9),
    (Frame, [9, 1], 10),
    (Frame, [10], 10),
    (LastFrame, [10], 10),
    (LastFrame, [10, 10], 20),
    (LastFrame, [10, 10, 10], 30),
    (LastFrame, [9, 1], 10),
    (LastFrame, [9, 1, 5], 15),
])
def test_frame_score(frame_class, values, expected_score):
    frame = _perform_throws_in_frame(values, frame_class)
    assert frame.score == expected_score


@pytest.mark.parametrize('frame_class, values, expected_num_bonus_throws', [
    (Frame, [10], 2),
    (Frame, [9, 1], 1),
    (LastFrame, [10], 0),
    (LastFrame, [10, 10, 10], 0),
])
def test_frame_num_bonus_throws(frame_class, values, expected_num_bonus_throws):
    frame = frame_class()
    num_bonus_throws = None  # to silence linters
    for one_value in values:
        num_bonus_throws = frame.add_throw(one_value)
    assert num_bonus_throws == expected_num_bonus_throws


@pytest.mark.parametrize('values, expected_is_finished', [
    ([], False),
    ([10], False),
    ([10] * 11, False),
    ([10] * 12, True),
    ([1] * 19, False),
    ([1] * 20, True),
])
def test_game_is_finished(values, expected_is_finished):
    game = _perform_throws_in_game(values)
    assert game.is_finished == expected_is_finished


@pytest.mark.parametrize('values,expected_frame_scores', [
    ([10], [10]),
    ([10, 10], [20, 10]),
    ([10] * 12, [30] * 10),
])
def test_game_frame_scores(values, expected_frame_scores):
    game = _perform_throws_in_game(values)
    assert game.get_frame_scores() == expected_frame_scores


@pytest.mark.parametrize('values, expected_game_score', [
    ([10] * 12, 300),
    ([1] * 20, 20),
])
def test_game_score(values, expected_game_score):
    game = _perform_throws_in_game(values)
    assert game.score == expected_game_score


def _perform_throws_in_frame(values, frame_class):
    frame = frame_class()
    for one_value in values:
        assert not frame.is_finished
        frame.add_throw(one_value)
    return frame


def _perform_throws_in_game(values):
    game = Game()
    for one_value in values:
        game.add_throw(one_value)
    return game

