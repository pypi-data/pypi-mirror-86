import colorama


class Zero:

    def __init__(self):
        self._name = "O"

    def __str__(self):
        return colorama.Fore.BLUE + self._name + colorama.Style.RESET_ALL
