class Life(object):
    def __init__(self):
        self._living = set()

    @property
    def living(self):
        for cell in self._living:
            yield cell

    def is_alive(self, (x, y)):
        return (x, y) in self._living

    def neighbours(self, (x, y)):
        if type(x) is not int or type(y) is not int:
            raise TypeError('It is only possible to calculate the neighbours for an integer co-ordinate pair.')

        yield (x - 1, y - 1)
        yield (x - 1, y)
        yield (x - 1, y + 1)
        yield (x, y + 1)
        yield (x + 1, y + 1)
        yield (x + 1, y)
        yield (x + 1, y - 1)
        yield (x, y - 1)

    def set_dead(self, (x, y)):
        if type(x) is not int or type(y) is not int:
            raise TypeError('It is only possible to set an integer co-ordinate pair to be a dead cell.')
        self._living.discard((x, y))

    def set_living(self, (x, y)):
        if type(x) is not int or type(y) is not int:
            raise TypeError('It is only possible to set an integer co-ordinate pair to be a living cell.')
        self._living.add((x, y))
