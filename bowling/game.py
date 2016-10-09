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

    def add_throw(self, throws):
        """
        :type throws: bowling.ObservableStream
        """
        value = next(throws)
        self.score += value

    @property
    def is_finished(self):
        return self.score == PINS_IN_FRAME
