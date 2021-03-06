import pytest

from life.life import Life


def test_create_game():
    assert Life()


def test_check_initially_blank():
    game = Life()
    assert len(list(game.living)) == 0


def test_set_living():
    game = Life()
    game.set_living((0, 0))
    game.set_living((-1, -3))
    game.set_living((3, 3))

    assert (0, 0) in game.living
    assert (-1, -3) in game.living
    assert (3, 3) in game.living


def test_non_integer_set_living():
    game = Life()
    with pytest.raises(TypeError):
        game.set_living((True, True))
    with pytest.raises(TypeError):
        game.set_living(('test', 'test'))

    assert (True, True) not in game.living
    assert ('test', 'test') not in game.living


def test_repeated_set_living():
    game = Life()
    assert (0, 0) not in game.living
    game.set_living((0, 0))
    assert (0, 0) in game.living

    game.set_living((0, 0))
    assert (0, 0) in game.living


def test_is_alive():
    game = Life()
    assert not game.is_alive((0, 0))

    game.set_living((0, 0))
    assert game.is_alive((0, 0))


def test_set_dead():
    game = Life()
    game.set_dead((0, 0))
    assert not game.is_alive((0, 0))

    game.set_living((0, 0))
    assert game.is_alive((0, 0))
    game.set_dead((0, 0))
    assert not game.is_alive((0, 0))


def test_non_integer_set_dead():
    # Technically nothing bad could happen by them calling set_dead with something invalid anyway --- since it could never exist in the set as set_living checks it is valid. It seems better to explicitly throw an exception, however, so that if an accidental mistake was made, it could be caught early.
    game = Life()
    with pytest.raises(TypeError):
        game.set_dead((True, True))
    with pytest.raises(TypeError):
        game.set_dead(('test', 'test'))

    assert (True, True) not in game.living
    assert ('test', 'test') not in game.living


def test_neighbours():
    game = Life()
    neighbours = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1)
    )

    assert len(neighbours) == len(list(game.neighbours((0, 0))))
    assert sorted(neighbours) == sorted(list(game.neighbours((0, 0))))


def test_invalid_neighbours():
    game = Life()
    with pytest.raises(TypeError):
        list(game.neighbours((True, True)))


def test_count_living_neighbours():
    game = Life()
    assert game.count_living_neighbours((0, 0)) == 0

    game.set_living((0, 1))
    assert game.count_living_neighbours((0, 0)) == 1

    game.set_living((1, 1))
    assert game.count_living_neighbours((0, 0)) == 2
    assert game.count_living_neighbours((0, 1)) == 1
    assert game.count_living_neighbours((1, 1)) == 1


def test_empty_tick():
    game = Life()
    assert len(list(game.living)) == 0
    game.tick()
    assert len(list(game.living)) == 0
    game.tick()
    assert len(list(game.living)) == 0


def test_stable_block_tick():
    game = Life()
    game.set_living((0, 0))
    game.set_living((0, 1))
    game.set_living((1, 0))
    game.set_living((1, 1))

    assert len(list(game.living)) == 4
    game.tick()
    assert len(list(game.living)) == 4
    game.tick()
    assert len(list(game.living)) == 4


def test_under_population_death():
    game = Life()
    game.set_living((0, 0))
    assert game.is_alive((0, 0))

    game.tick()
    assert len(list(game.living)) == 0
    game.tick()
    assert len(list(game.living)) == 0


def test_under_population_death_one_neighbour():
    game = Life()
    game.set_living((0, 0))
    game.set_living((0, 1))
    assert len(list(game.living)) == 2

    game.tick()
    assert len(list(game.living)) == 0


def test_isolated_under_population():
    game = Life()
    game.set_living((0, 0))
    game.set_living((2, 2))
    game.set_living((2, 3))
    game.set_living((2, 4))

    assert len(list(game.living)) == 4

    game.tick()

    # In this case, we need to check specific spaces, since the number alive will change once the reproduction rule is implemented
    assert not game.is_alive((0, 0))
    assert not game.is_alive((2, 2))
    assert not game.is_alive((2, 4))
    assert game.is_alive((2, 3))


def test_over_population_death():
    for count in range(4, 8):
        game = Life()
        game.set_living((0, 0))

        neighbour = game.neighbours((0, 0))
        for i in range(0, count):
            game.set_living(neighbour.next())

        assert game.is_alive((0, 0))
        game.tick()
        assert not game.is_alive((0, 0))


def test_over_population_isolated():
    game = Life()
    game.set_living((0, 0))
    game.set_living((0, 1))
    game.set_living((-1, 0))
    game.set_living((1, 0))
    game.set_living((-1, -1))

    game.set_living((10, 10))
    game.set_living((11, 10))
    game.set_living((9, 10))
    game.set_living((10, 11))
    game.set_living((10, 9))

    assert len(list(game.living)) == 10
    game.tick()
    assert not game.is_alive((0, 0))
    assert not game.is_alive((10, 10))


def test_reproduction():
    game = Life()
    game.set_living((0, 0))
    game.set_living((0, 1))
    game.set_living((0, -1))

    game.tick()
    assert game.is_alive((1, 0))
    assert game.is_alive((-1, 0))


def test_reproduction_stable():
    game = Life()
    game.set_living((0, 0))
    game.set_living((-1, 0))
    game.set_living((-1, -1))

    for i in range(0, 100):
        game.tick()
        assert game.is_alive((0, 0))
        assert game.is_alive((-1, 0))
        assert game.is_alive((-1, -1))

        assert game.is_alive((0, -1))


def test_spinning():
    game = Life()
    game.set_living((0, 0))
    game.set_living((-1, 0))
    game.set_living((1, 0))

    for i in range(0, 100):
        game.tick()
        assert game.is_alive((0, 0))
        assert game.is_alive((0, 1))
        assert game.is_alive((0, -1))
        assert len(list(game.living)) == 3

        game.tick()
        assert game.is_alive((0, 0))
        assert game.is_alive((-1, 0))
        assert game.is_alive((1, 0))
        assert len(list(game.living)) == 3


def test_known_final_result():
    """Using "small exploder" pattern:
    X10
    111
    101
    010

    Known to produce the pattern
    00000010000000
    00000101000000
    00000101000000
    00000010000000
    00000000000000
    01100X00000110
    10010000001001
    01100000000110
    00000000000000
    00000010000000
    00000101000000
    00000101000000
    00000010000000

    after 16 iterations. X used to mark reference point.
    """

    game = Life()
    # Initial pattern
    game.set_living((1, 0))
    game.set_living((0, 1))
    game.set_living((1, 1))
    game.set_living((2, 1))
    game.set_living((0, 2))
    game.set_living((2, 2))
    game.set_living((1, 3))

    for i in range(0, 17):
        game.tick()

    # Top pattern
    assert game.is_alive((1, -5))
    assert game.is_alive((0, -4))
    assert game.is_alive((2, -4))
    assert game.is_alive((0, -3))
    assert game.is_alive((2, -3))
    assert game.is_alive((1, -2))

    # Left pattern
    assert game.is_alive((-3, 0))
    assert game.is_alive((-4, 0))
    assert game.is_alive((-2, 1))
    assert game.is_alive((-5, 1))
    assert game.is_alive((-3, 2))
    assert game.is_alive((-4, 2))

    # Right pattern
    assert game.is_alive((5, 0))
    assert game.is_alive((6, 0))
    assert game.is_alive((4, 1))
    assert game.is_alive((7, 1))
    assert game.is_alive((5, 2))
    assert game.is_alive((6, 2))

    # Bottom pattern
    assert game.is_alive((1, 4))
    assert game.is_alive((0, 5))
    assert game.is_alive((2, 5))
    assert game.is_alive((0, 6))
    assert game.is_alive((2, 6))
    assert game.is_alive((1, 7))

    assert len(list(game.living)) == 24
