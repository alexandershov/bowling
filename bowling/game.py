PINS_IN_FRAME = 10

from bowling.stream import ObservableStream, Observer


class BaseFrame(object):
    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        raise NotImplementedError

    @property
    def is_finished(self):
        raise NotImplementedError


class Frame(BaseFrame, Observer):
    MAX_NUM_THROWS_IN_FRAME = 2

    def __init__(self):
        self.score = 0
        self.num_throws = 0
        self.num_next_balls_bonuses = 0

    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        assert not self.is_finished
        value = next(throws)
        self.add(value)
        if self.score == PINS_IN_FRAME:
            self.num_next_balls_bonuses = 1 + self.MAX_NUM_THROWS_IN_FRAME - self.num_throws
            throws.register(self)

    def on_new_value(self, throws, value):
        if not self.num_next_balls_bonuses:
            throws.unregister(self)
            return
        self.score += value
        self.num_next_balls_bonuses -= 1

    def add(self, value):
        self.score += value
        self.num_throws += 1

    @property
    def is_finished(self):
        if self.num_throws == self.MAX_NUM_THROWS_IN_FRAME:
            return True
        if self.score == PINS_IN_FRAME:
            return True
        return False


class LastFrame(Frame):
    MAX_NUM_THROWS_IN_FRAME = 3

    def __init__(self):
        super(LastFrame, self).__init__()
        self.max_num_throws = 2

    def add(self, value):
        super(LastFrame, self).add(value)
        if self.score == PINS_IN_FRAME:
            if self.max_num_throws < self.MAX_NUM_THROWS_IN_FRAME:
                self.max_num_throws += 1

    @property
    def is_finished(self):
        if self.num_throws == self.max_num_throws:
            return True
        return False


class Game(object):
    MAX_NUM_FRAMES = 10
    assert MAX_NUM_FRAMES > 0

    def __init__(self):
        self.throws = ObservableStream()
        self.frames = []

    def add_throw(self, value):
        self.throws.add(value)
        if len(self.frames) == self.MAX_NUM_FRAMES - 1:
            frame = LastFrame()
        else:
            frame = Frame()

    def get_frame_scores(self):
        return [10]
