import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
BOARD_COLOR = (0, 128, 0)
SNAKE_COLOR = (255, 0, 0)
LADDER_COLOR = (0, 0, 255)
PLAYER_COLORS = [(255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 165, 0)]
SQUARE_SIZE = 80

class SnakeAndLaddersGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake and Ladders")
        self.clock = pygame.time.Clock()
        self.players = []
        self.current_player = 0
        self.board = self.create_board()
        self.running = True
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    def create_board(self):
        return [i for i in range(1, 101)]

    def add_player(self, color):
        self.players.append({'position': 0, 'color': color})

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self):
        player = self.players[self.current_player]
        roll = self.roll_dice()
        new_position = player['position'] + roll
        if new_position in self.snakes:
            player['position'] = self.snakes[new_position]
        elif new_position in self.ladders:
            player['position'] = self.ladders[new_position]
        elif new_position < 100:
            player['position'] = new_position

        if player['position'] == 100:
            player['position'] = 100
            self.running = False  # End game if player reaches 100

    def draw_board(self):
        self.screen.fill(BOARD_COLOR)
        for player in self.players:
            player_radius = 20
            pygame.draw.circle(self.screen, player['color'], (player['position'] * 80 + 40, HEIGHT - (player['position'] // 10 + 1) * 80 + 40), player_radius)

        # Draw snakes
        for start, end in self.snakes.items():
            start_pos = ((start - 1) % 10, (start - 1) // 10)
            end_pos = ((end - 1) % 10, (end - 1) // 10)
            pygame.draw.line(self.screen, SNAKE_COLOR, (start_pos[0] * 80 + 40, HEIGHT - (start_pos[1] + 1) * 80 + 40),
                             (end_pos[0] * 80 + 40, HEIGHT - (end_pos[1] + 1) * 80 + 40), 5)

        # Draw ladders
        for start, end in self.ladders.items():
            start_pos = ((start - 1) % 10, (start - 1) // 10)
            end_pos = ((end - 1) % 10, (end - 1) // 10)
            pygame.draw.line(self.screen, LADDER_COLOR, (start_pos[0] * 80 + 40, HEIGHT - (start_pos[1] + 1) * 80 + 40),
                             (end_pos[0] * 80 + 40, HEIGHT - (end_pos[1] + 1) * 80 + 40), 5)

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.move_player()
            self.draw_board()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeAndLaddersGame()
    game.add_player(PLAYER_COLORS[0])  # Add first player
    game.add_player(PLAYER_COLORS[1])  # Add second player
    game.run()
