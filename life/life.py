class Life(object):
    def __init__(self, living_set=None):
        if living_set:
            self._living = living_set
        else:
            self._living = set()

    @property
    def living(self):
        for cell in self._living:
            yield cell

    def count_living_neighbours(self, (x, y)):
        count = 0
        for neighbour in self.neighbours((x, y)):
            if self.is_alive(neighbour):
                count += 1

        return count

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

    def tick(self):
        # Take a copy of the current board state, since the next board state is a pure function of the current one, and should not be affected by intermediate results.
        next_iteration = Life(living_set=self._living.copy())

        # Underpopulation deaths.
        for cell in self.living:
            if self.count_living_neighbours(cell) < 2:
                next_iteration.set_dead(cell)

        # Overpopulation deaths.
        for cell in self.living:
            if self.count_living_neighbours(cell) > 3:
                next_iteration.set_dead(cell)

        # Once all modifications to the next board state have been calculated, replace the current board with the newly calculated one.
        self._living = next_iteration._living
