from colorama import Fore as f, Back as b, Style as s
class X:
    def __str__(self):
        return f.RED + 'x' + s.RESET_ALL
