PINS_IN_FRAME = 10

from bowling.stream import ObservableStream, Observer


class BaseFrame(object):
    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        raise NotImplementedError

    def on_max_score(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        raise NotImplementedError


class Frame(BaseFrame, Observer):
    MAX_NUM_THROWS_IN_FRAME = 2

    def __init__(self):
        self.score = 0
        self.throws = []
        self.num_throws = 0
        self.max_num_throws = 2
        self.num_next_balls_bonuses = 0
        self.is_finished = False

    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        assert not self.is_finished
        value = next(throws)
        self.throws.append(value)
        self.add(value)
        if self.score == PINS_IN_FRAME:
            self.on_max_score(throws)

        if self.num_throws == self.max_num_throws:
            self.is_finished = True

    def on_max_score(self, throws):
        self.num_next_balls_bonuses = 1 + self.max_num_throws - self.num_throws
        throws.register(self)
        self.is_finished = True

    def on_new_value(self, throws, value):
        if not self.num_next_balls_bonuses:
            throws.unregister(self)
            return
        self.score += value
        self.num_next_balls_bonuses -= 1

    def add(self, value):
        self.score += value
        self.num_throws += 1


class LastFrame(Frame):
    MAX_NUM_THROWS_IN_FRAME = 3

    def add(self, value):
        super(LastFrame, self).add(value)
        if self.score == PINS_IN_FRAME:
            if self.max_num_throws < self.MAX_NUM_THROWS_IN_FRAME:
                self.max_num_throws += 1

    def on_max_score(self, throws):
        pass


class Game(object):
    MAX_NUM_FRAMES = 10

    def __init__(self):
        self.throws = ObservableStream()
        self.frames = []
        self.is_finished = False

    def add_throw(self, value):
        assert not self.is_finished
        self.throws.add(value)
        if not self.frames or self.frames[-1].is_finished:
            if len(self.frames) == self.MAX_NUM_FRAMES:
                self.is_finished = True
                return
            elif len(self.frames) == self.MAX_NUM_FRAMES - 1:
                self.frames.append(LastFrame())
            else:
                self.frames.append(Frame())
        cur_frame = self.frames[-1]
        cur_frame.add_throw(self.throws)
        if len(self.frames) == self.MAX_NUM_FRAMES and cur_frame.is_finished:
            self.is_finished = True

    def get_frame_scores(self):
        return [frame.score for frame in self.frames]

    @property
    def score(self):
        assert self.is_finished
        return sum(self.get_frame_scores())
