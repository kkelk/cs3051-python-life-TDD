class Life(object):
    def __init__(self):
        self._living = set()

    @property
    def living(self):
        for cell in self._living:
            yield cell

    def set_living(self, (x, y)):
        self._living.add((x, y))
