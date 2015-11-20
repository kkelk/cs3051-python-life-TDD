from life.life import Life


def test_create_game():
    assert Life()


def test_check_initially_blank():
    game = Life()
    assert len(list(game.living)) == 0
