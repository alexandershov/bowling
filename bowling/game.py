PINS_IN_FRAME = 10


class BaseFrame(object):
    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        raise NotImplementedError

    @property
    def is_finished(self):
        raise NotImplementedError


class Frame(BaseFrame):
    MAX_NUM_THROWS_IN_FRAME = 2

    def __init__(self):
        self.score = 0
        self.num_throws = 0

    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        assert not self.is_finished
        value = next(throws)
        self.add(value)

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
    def throw(self, value):
        pass
