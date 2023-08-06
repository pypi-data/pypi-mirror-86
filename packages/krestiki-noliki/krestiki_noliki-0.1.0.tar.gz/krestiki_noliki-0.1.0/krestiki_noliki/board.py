from krestiki_noliki.dagger import Dagger
from krestiki_noliki.zero import Zero


class Board:
    _dagger = Dagger()
    _zero = Zero()

    def __init__(self):
        self._cells = []
        numb = 1
        for i in range(3):
            self._cells.append([numb, numb + 1, numb + 2])
            numb += 3

    def setFigure(self, position, figure):
        line = position // 3 - 1
        column = position % 3 - 1

        if column == -1:
            column = 2
        else:
            line += 1

        if self._cells[line][column].__class__ == int:
            self._cells[line][column] = self._dagger if figure == "X" else self._zero
            return True
        else:
            return False

    def getPosition(self, position):
        line = position // 3 - 1
        column = position % 3 - 1

        if column == -1:
            column = 2
        else:
            line += 1

        return str(self._cells[line][column])

    def __str__(self):
        out = ""
        for i in range(3):
            out += "|"

            for j in range(3):
                out += str(self._cells[i][j]) + "|"

            out += "\n"

        return out
