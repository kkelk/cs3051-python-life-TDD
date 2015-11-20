class Life(object):
    def __init__(self):
        self._living = set()

    @property
    def living(self):
        for cell in self._living:
            yield cell

    def set_living(self, (x, y)):
        if type(x) is not int or type(y) is not int:
            raise TypeError('It is only possible to set an integer co-ordinate pair to be a living cell.')
        self._living.add((x, y))
