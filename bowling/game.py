MAX_NUM_THROWS_IN_FRAME = 2
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
    def __init__(self):
        self.score = 0
        self.num_throws = 0

    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        assert not self.is_finished
        value = next(throws)
        self.score += value
        self.num_throws += 1

    @property
    def is_finished(self):
        if self.num_throws == MAX_NUM_THROWS_IN_FRAME:
            return True
        if self.score == PINS_IN_FRAME:
            return True
        return False
