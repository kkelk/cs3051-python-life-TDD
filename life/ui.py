import curses
from curses.wrapper import wrapper

from life import Life

KEYBINDINGS = {
    curses.KEY_LEFT: 'cursor_left',
    curses.KEY_RIGHT: 'cursor_right',
    curses.KEY_UP: 'cursor_up',
    curses.KEY_DOWN: 'cursor_down',
    ord('h'): 'screen_left',
    ord('l'): 'screen_right',
    ord('j'): 'screen_down',
    ord('k'): 'screen_up',
    ord(' '): 'toggle_live',
    ord('n'): 'tick',
    ord('p'): 'toggle_play'
}


class CursesScreen(object):
    def __init__(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

        self._stdscr = stdscr
        self._stdscr.nodelay(1)

        self._offset_x = 0
        self._offset_y = 0

        maxy, maxx = stdscr.getmaxyx()
        self._cursor_x = maxx / 2
        self._cursor_y = maxy / 2

        self._game = Life()
        self._playing = False

    def _render(self):
        maxy, maxx = self._stdscr.getmaxyx()
        for x in range(1, maxx - 1):
            for y in range(1, maxy - 1):
                if self._game.is_alive((x + self._offset_x, y + self._offset_y)):
                    if (x, y) == (self._cursor_x, self._cursor_y):
                        self._stdscr.addch(y, x, ord('X'), curses.color_pair(2) | curses.A_REVERSE)
                    else:
                        self._stdscr.addch(y, x, ord('0'), curses.color_pair(1) | curses.A_BOLD)
                elif (x, y) == (self._cursor_x, self._cursor_y):
                    self._stdscr.addch(y, x, ord('X'), curses.color_pair(2) | curses.A_BOLD)
                else:
                    self._stdscr.addch(y, x, ord(' '))

            self._stdscr.refresh()

    def loop(self):
        self._render()
        while True:
            maxy, maxx = self._stdscr.getmaxyx()

            try:
                c = self._stdscr.getch()
                action = KEYBINDINGS[c]

                if action == 'screen_left':
                    self._offset_x -= 1
                elif action == 'screen_up':
                    self._offset_y -= 1
                elif action == 'screen_down':
                    self._offset_y += 1
                elif action == 'screen_right':
                    self._offset_x += 1
                elif action == 'cursor_left':
                    if self._cursor_x > 0:
                        self._cursor_x -= 1
                    else:
                        self._offset_x -= 1
                elif action == 'cursor_right':
                    if self._cursor_x < maxx:
                        self._cursor_x += 1
                    else:
                        self._offset_x += 1
                elif action == 'cursor_up':
                    if self._cursor_y > 0:
                        self._cursor_y -= 1
                    else:
                        self._offset_y -= 1
                elif action == 'cursor_down':
                    if self._cursor_y < maxy:
                        self._cursor_y += 1
                    else:
                        self._offset_y += 1
                elif action == 'toggle_live':
                    x = self._cursor_x + self._offset_x
                    y = self._cursor_y + self._offset_y
                    if self._game.is_alive((x, y)):
                        self._game.set_dead((x, y))
                    else:
                        self._game.set_living((x, y))
                elif action == 'tick':
                    self._game.tick()
                elif action == 'toggle_play':
                    self._playing = not self._playing
            except KeyError:
                if c == -1 and self._playing:
                    self._game.tick()

            self._render()


def main(stdscr):
    CursesScreen(stdscr).loop()

if __name__ == '__main__':
    wrapper(main)
