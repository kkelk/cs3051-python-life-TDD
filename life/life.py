class Life(object):
    def __init__(self):
        self._living = set()

    @property
    def living(self):
        for cell in self._living:
            yield cell
