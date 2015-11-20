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
