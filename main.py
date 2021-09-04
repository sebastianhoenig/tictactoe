import random


class Player:

    def __init__(self, name, symbol, ki):
        self.name = name
        self.symbol = symbol
        self.ki = ki
        self.score = 0


class Board:

    def __init__(self):
        self.fields = [Field(i+1) for i in range(9)]
        self.win_cond = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7},
                         {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 7}]

    def available(self):
        empty_fields = []
        for field in self.fields:
            if field.symbol == " ":
                empty_fields.append(field.number)
        return empty_fields

    def set_mark(self, coordinate, symbol):
        for field in self.fields:
            if field.number == coordinate:
                field.set_symbol(symbol)

    def check_winner(self, symbol):
        marked = {field.number for field in self.fields if field.symbol ==
                  symbol}
        for sub in self.win_cond:
            if sub.issubset(marked):
                print(sub)
                print(marked)
                return True
        return False

    def check_draw(self):
        draw_check = [field for field in self.fields if
                      field.symbol == " "]
        if len(draw_check) == 0:
            return True
        return False

    def visual(self):
        v = ""
        v += " --- --- ---\n" + \
             "| {} | {} | {} |\n".format(self.fields[0].symbol, self.fields[
                 1].symbol, self.fields[2].symbol)
        v+= " --- --- ---\n" + \
            "| {} | {} | {} |\n".format(self.fields[3].symbol, self.fields[
                4].symbol, self.fields[5].symbol)
        v += " --- --- ---\n" + \
             "| {} | {} | {} |\n".format(self.fields[6].symbol, self.fields[
                 7].symbol, self.fields[8].symbol)
        v += " --- --- ---\n"
        return v


class Field:

    def __init__(self, number):
        self.number = number
        self.symbol = " "

    def set_symbol(self, symbol):
        self.symbol = symbol


class Game:

    def __init__(self):
        self.players = []
        self.Board = Board()

    def set_up(self):
        # symbols = ["X", "O"]
        self.players.append(Player("Seb", "X", False))
        self.players.append(Player("KI", "O", True))

    def game(self):
        winner = False
        print(self.Board.visual())
        while not winner:
            for player in self.players:
                available = self.Board.available()
                if not player.ki:
                    self.player_plays(available, player)
                else:
                    self.ki_plays(available, player)
                print(self.Board.visual())
                if self.Board.check_winner(player.symbol):
                    print("Game over, {} hat gewonnen".format(player.name))
                    winner = True
                elif self.Board.check_draw():
                    print("Draw!")
                    winner = True

    def player_plays(self, available, player):
        print(available)
        choice = int(input("Choose a field from the available ones:"))
        if choice not in available:
            print("Not possible. Again")
            self.player_plays(available)
        else:
            self.Board.set_mark(choice, player.symbol)

    def ki_plays(self, available, player):
        choice = random.choice(available)
        self.Board.set_mark(choice, player.symbol)


def main():
    game = Game()
    game.set_up()
    game.game()


if __name__ == "__main__":
    main()
