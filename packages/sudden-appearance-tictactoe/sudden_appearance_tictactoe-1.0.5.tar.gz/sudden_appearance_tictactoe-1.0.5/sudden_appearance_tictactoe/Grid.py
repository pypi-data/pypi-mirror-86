from colorama import Fore as f, Back as b, Style as s


class Grid:
    def insert(self, x, y, value):
        if self.a[x - 1][y - 1]:
            raise IOError
        else:
            self.a[x - 1][y - 1] = value
            self.moves += 1

    def over(self):
        for i in range(3):
            if self.a[0][i] == self.a[1][i] == self.a[2][i]:
                return self.a[0][i]
            if self.a[i][0] == self.a[i][1] == self.a[i][2]:
                return self.a[i][0]
        if self.a[0][0] == self.a[1][1] == self.a[2][2]:
            return self.a[0][0]
        if self.a[2][0] == self.a[1][1] == self.a[0][2]:
            return self.a[2][0]
        return None if self.moves < 9 else "Draw"

    def get(self, x, y):
        if not self.a[x - 1][y - 1]:
            return " "
        else:
            return self.a[x - 1][y - 1]

    def __init__(self):
        self.a = [[0] * 3 for i in range(3)]
        self.moves = 0

    def __str__(self):
        return f"""
{f.GREEN}  | {f.CYAN}1{f.GREEN} | {f.CYAN}2{f.GREEN} | {f.CYAN}3{f.GREEN} |{s.RESET_ALL}
{f.GREEN}--+---+---+---+{s.RESET_ALL}
{f.CYAN}1{f.GREEN} | {f.CYAN + str(self.get(1, 1)) + f.GREEN} | {f.CYAN + str(self.get(2, 1)) + f.GREEN} | {f.CYAN + str(self.get(3, 1)) + f.GREEN} |
{f.GREEN}--+---+---+---+{s.RESET_ALL}
{f.CYAN}2{f.GREEN} | {f.CYAN + str(self.get(1, 2)) + f.GREEN} | {f.CYAN + str(self.get(2, 2)) + f.GREEN} | {f.CYAN + str(self.get(3, 2)) + f.GREEN} |
{f.GREEN}--+---+---+---+{s.RESET_ALL}
{f.CYAN}3{f.GREEN} | {f.CYAN + str(self.get(1, 3)) + f.GREEN} | {f.CYAN + str(self.get(2, 3)) + f.GREEN} | {f.CYAN + str(self.get(3, 3)) + f.GREEN} |
{f.GREEN}--+---+---+---+{s.RESET_ALL}
"""
