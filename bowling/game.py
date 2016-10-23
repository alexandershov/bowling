PINS_IN_FRAME = 10
DEFAULT_NUM_THROWS = 2


class BaseFrame(object):
    def __init__(self):
        self.score = 0
        self.throws = []  # list[int]
        self.is_finished = False
        self.max_num_throws = DEFAULT_NUM_THROWS
        self._num_throws = 0
        self._num_next_balls_bonuses = 0
        self._on_max_score_called = False

    def add_throw(self, value):
        assert not self.is_finished
        self._add(value)
        if self.score == PINS_IN_FRAME:
            self._call_on_max_score_if_for_the_first_time()

        if self._num_throws == self.max_num_throws:
            self.is_finished = True
        return self._num_next_balls_bonuses

    def _call_on_max_score_if_for_the_first_time(self):
        if not self._on_max_score_called:
            self.on_max_score()
            self._on_max_score_called = True

    def _add(self, value):
        self.score += value
        self.throws.append(value)
        self._num_throws += 1

    def add_bonus_score(self, bonus_score):
        assert self.is_finished
        self.score += bonus_score

    def on_max_score(self):
        raise NotImplementedError


class Frame(BaseFrame):
    def on_max_score(self):
        self._num_next_balls_bonuses = (self.max_num_throws - self._num_throws) + 1
        self.is_finished = True


class LastFrame(Frame):
    MAX_NUM_THROWS_IN_FRAME = 3

    def on_max_score(self):
        self.max_num_throws += 1

    def add_bonus_score(self, value):
        raise AssertionError


class Game(object):
    MAX_NUM_FRAMES = 10

    def __init__(self):
        self.frames = []
        self.is_finished = False
        self._frames_waiting_for_bonus = {}  # Frame -> num_bonus_throws

    def add_throw(self, value):
        assert not self.is_finished
        self._add_bonus_to_frames(value)
        if self._needs_to_add_frame():
            self._add_frame()

        num_bonus_throws = self._cur_frame.add_throw(value)
        if num_bonus_throws:
            assert self._cur_frame.is_finished
            self._add_frame_to_bonus_waiters(self._cur_frame, num_bonus_throws)

        if self._is_last_frame_finished():
            self.is_finished = True

    def get_frame_scores(self):
        return [frame.score for frame in self.frames]

    def _add_bonus_to_frames(self, value):
        for frame in self._frames_waiting_for_bonus:
            frame.add_bonus_score(value)
            self._frames_waiting_for_bonus[frame] -= 1
        self._remove_exhausted_frames_from_bonus_waiters()

    def _remove_exhausted_frames_from_bonus_waiters(self):
        for frame, num_bonus_throws in list(self._frames_waiting_for_bonus.items()):
            if not num_bonus_throws:
                self._remove_frame_from_bonus_waiters(frame)

    def _add_frame_to_bonus_waiters(self, frame, num_bonus_throws):
        self._frames_waiting_for_bonus[frame] = num_bonus_throws

    def _remove_frame_from_bonus_waiters(self, frame):
        del self._frames_waiting_for_bonus[frame]

    @property
    def _cur_frame(self):
        return self.frames[-1]

    def _add_frame(self):
        if len(self.frames) == self.MAX_NUM_FRAMES - 1:
            self.frames.append(LastFrame())
        else:
            self.frames.append(Frame())

    def _needs_to_add_frame(self):
        assert not self.is_finished
        if not self.frames:
            return True
        return self._cur_frame.is_finished

    def _is_last_frame_finished(self):
        return len(self.frames) == self.MAX_NUM_FRAMES and self._cur_frame.is_finished

    @property
    def score(self):
        assert self.is_finished
        return sum(self.get_frame_scores())
