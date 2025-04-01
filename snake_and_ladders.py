import random

class SnakeAndLadders:
    def __init__(self):
        self.board = self.create_board()
        self.players = {}
        self.current_player = 0

    def create_board(self):
        board = list(range(1, 101))
        # Snakes
        board[16] = 6
        board[47] = 26
        board[49] = 11
        board[56] = 53
        board[62] = 19
        board[64] = 60
        board[87] = 24
        board[93] = 73
        board[95] = 75
        board[98] = 78
        # Ladders
        board[1] = 38
        board[4] = 14
        board[9] = 31
        board[21] = 42
        board[28] = 84
        board[36] = 44
        board[51] = 67
        board[71] = 91
        board[80] = 100
        return board

    def add_player(self, name):
        self.players[name] = 0

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self, player):
        roll = self.roll_dice()
        print(f"{player} rolled a {roll}")
        new_position = self.players[player] + roll
        if new_position < 100:
            self.players[player] = self.board[new_position - 1]
            print(f"{player} moved to {self.players[player]}")
        elif new_position == 100:
            self.players[player] = 100
            print(f"{player} reached 100 and wins!")
        else:
            print(f"{player} cannot move, rolled too high!")

    def play_game(self):
        while True:
            player = list(self.players.keys())[self.current_player]
            self.move_player(player)
            if self.players[player] == 100:
                break
            self.current_player = (self.current_player + 1) % len(self.players)

if __name__ == "__main__":
    game = SnakeAndLadders()
    game.add_player("Player 1")
    game.add_player("Player 2")
    game.play_game()
