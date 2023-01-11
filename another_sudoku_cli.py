#!/usr/bin/env python

"""Main module."""

from random import randint
import time
import click
import another_sudoku_library as su


def prefill(s):
    return click.style(s, bold=True)

def userfill(s):
    return click.style(s, fg="red")

def cursor(s):
    return click.style(s, reverse=True, fg="red")

def reverse(s):
    return click.style(s, fg="black", bg="white")

def fmtSeconds(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)

menu = """
0) Basic
1) Easy
2) Medium
3) Hard
q) Quit 
Your choice\
"""

board_template = """
{b[0][0]} {b[0][1]} {b[0][2]} │ {b[0][3]} {b[0][4]} {b[0][5]} │ {b[0][6]} {b[0][7]} {b[0][8]}
{b[1][0]} {b[1][1]} {b[1][2]} │ {b[1][3]} {b[1][4]} {b[1][5]} │ {b[1][6]} {b[1][7]} {b[1][8]}
{b[2][0]} {b[2][1]} {b[2][2]} │ {b[2][3]} {b[2][4]} {b[2][5]} │ {b[2][6]} {b[2][7]} {b[2][8]}
──────┼───────┼──────
{b[3][0]} {b[3][1]} {b[3][2]} │ {b[3][3]} {b[3][4]} {b[3][5]} │ {b[3][6]} {b[3][7]} {b[3][8]}
{b[4][0]} {b[4][1]} {b[4][2]} │ {b[4][3]} {b[4][4]} {b[4][5]} │ {b[4][6]} {b[4][7]} {b[4][8]}
{b[5][0]} {b[5][1]} {b[5][2]} │ {b[5][3]} {b[5][4]} {b[5][5]} │ {b[5][6]} {b[5][7]} {b[5][8]}
──────┼───────┼──────
{b[6][0]} {b[6][1]} {b[6][2]} │ {b[6][3]} {b[6][4]} {b[6][5]} │ {b[6][6]} {b[6][7]} {b[6][8]}
{b[7][0]} {b[7][1]} {b[7][2]} │ {b[7][3]} {b[7][4]} {b[7][5]} │ {b[7][6]} {b[7][7]} {b[7][8]}
{b[8][0]} {b[8][1]} {b[8][2]} │ {b[8][3]} {b[8][4]} {b[8][5]} │ {b[8][6]} {b[8][7]} {b[8][8]}
"""

hints = """\
cursor: {WASD} | enter number: {NUMS} | clear: {SPACE} | submit: {ENTER} | quit: {Q}\
""".format(
    WASD=reverse("WASD"),
    NUMS=reverse("1-9"),
    SPACE=reverse("SPACE"),
    Q=reverse("q"),
    ENTER=reverse("ENTER"),
)


ACTIVE = "active"
OVER = "over"
WON = "won"


class Game:
    def __init__(self, diff, show_hints=True):
        self.start_puzzle = su.getPuzzle(diff)
        self.bitmap = su.getBitmap(self.start_puzzle)
        self.working = su.copyBoard(self.start_puzzle)
        self.y = 0
        self.x = 0
        self.gamestate = ACTIVE
        self.start_time = time.time()
        self.show_hints = show_hints

    def draw(self):
        rendered = su.getEmptyBoard()
        for y, x in su.fullGen():
            if self.bitmap[y][x]:
                rendered[y][x] = prefill(self.working[y][x])
            elif self.working[y][x] != 0:
                rendered[y][x] = userfill(self.working[y][x])
            else:
                rendered[y][x] = " "

        rendered[self.y][self.x] = cursor(rendered[self.y][self.x])

        click.clear()
        click.echo(board_template.format(b=rendered))
        if self.show_hints:
            click.echo(hints)

    def handleInput(self, char):
        """Accepts user input, changes state"""
        try:
            unicode = ord(char)
        except TypeError:
            unicode = ""

        if unicode == 119:
            self.y = (self.y + 8) % 9
        elif unicode == 115:
            self.y = (self.y + 10) % 9
        elif unicode == 97:
            self.x = (self.x + 8) % 9
        elif unicode == 100:
            self.x = (self.x + 10) % 9
        elif unicode in range(49, 58) and not self.bitmap[self.y][self.x]:
            self.working[self.y][self.x] = int(char)
        elif unicode == 32 and not self.bitmap[self.y][self.x]:
            self.working[self.y][self.x] = 0
        elif unicode == 113:
            if click.confirm("Are you sure you would like to quit?"):
                self.gamestate = OVER
        elif unicode == 13 or unicode == 10:
            if su.checkComplete(self.working) and su.checkConsistent(self.working):
                self.gamestate = WON
            else:
                click.echo("That's not quite right")
                if not click.confirm(
                    "Would you like to continue playing?", default=True
                ):
                    self.gamestate = OVER

    def loop(self):
        self.draw()
        while self.gamestate == ACTIVE:
            c = click.getchar()
            self.handleInput(c)
            self.draw()

        if self.gamestate == WON:
            finish_time = reverse(
                fmtSeconds(time.time() - self.start_time)
            )
            click.echo(
                "Congratulations! You finished the puzzle in {}!".format(finish_time)
            )
            click.pause("Press any key to return to menu")


@click.command()
def main():
    choice = ""
    while choice != "q":
        if choice == "1":
            g = Game(randint(30, 40))
            g.loop()
        elif choice == "2":
            g = Game(randint(40, 47))
            g.loop()
        elif choice == "3":
            g = Game(randint(47, 55))
            g.loop()
        elif choice == "0":
            g = Game(randint(10, 15))
            g.loop()

        click.clear()
        choice = click.prompt(menu)


if __name__ == "__main__":
    main()
