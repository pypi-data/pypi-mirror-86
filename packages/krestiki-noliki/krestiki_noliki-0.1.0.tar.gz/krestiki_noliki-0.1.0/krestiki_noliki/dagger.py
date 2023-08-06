import colorama


class Dagger:

    def __init__(self):
        self._name = "X"

    def __str__(self):
        return colorama.Fore.RED + self._name + colorama.Style.RESET_ALL
