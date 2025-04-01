import pygame
import sys
import random
import os
import time
import math
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BOARD_SIZE = 600
GRID_SIZE = 10  # 10x10 grid
CELL_SIZE = BOARD_SIZE // GRID_SIZE
DICE_SIZE = 80
PLAYER_SIZE = 30
ANIMATION_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (173, 216, 230)
BACKGROUND_COLOR = (240, 240, 240)
BOARD_COLOR = (220, 220, 220)
GRID_COLOR = (200, 200, 200)
SNAKE_COLOR = (255, 50, 50)
LADDER_COLOR = (50, 205, 50)

# Player colors and icons
PLAYER_COLORS = [RED, BLUE, GREEN, YELLOW]
PLAYER_NAMES = ["Red", "Blue", "Green", "Yellow"]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Enhanced Snake and Ladders Game')

# Load fonts
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 30)
font_large = pygame.font.SysFont('Arial', 40)
font_title = pygame.font.SysFont('Arial', 60, bold=True)

# Load sounds
try:
    dice_sound = pygame.mixer.Sound('dice_roll.wav')
    move_sound = pygame.mixer.Sound('move.wav')
    snake_sound = pygame.mixer.Sound('snake.wav')
    ladder_sound = pygame.mixer.Sound('ladder.wav')
    win_sound = pygame.mixer.Sound('win.wav')
except:
    # If sound files are not found, create silent sounds
    dice_sound = pygame.mixer.Sound(buffer=bytearray(44))
    move_sound = pygame.mixer.Sound(buffer=bytearray(44))
    snake_sound = pygame.mixer.Sound(buffer=bytearray(44))
    ladder_sound = pygame.mixer.Sound(buffer=bytearray(44))
    win_sound = pygame.mixer.Sound(buffer=bytearray(44))
    print("Sound files not found. Using silent sounds.")

class EnhancedSnakeAndLadderGame:
    def __init__(self):
        self.players = []
        self.current_player = 0
        self.dice_value = 1
        self.game_state = "menu"  # menu, setup, game, game_over
        self.winner = None
        self.dice_rolling = False
        self.dice_roll_time = 0
        self.target_players = 0
        self.input_text = ""
        self.input_active = False
        self.moving_animation = False
        self.animation_start_time = 0
        self.animation_start_pos = 0
        self.animation_end_pos = 0
        self.animation_current_pos = 0
        self.animation_path = []
        self.animation_index = 0
        self.show_rules = False
        self.show_credits = False
        
        # Game elements
        self.snakes = {
            16: 6, 47: 26, 49: 11, 56: 53, 62: 19,
            64: 60, 87: 24, 93: 73, 95: 75, 98: 78
        }
        self.ladders = {
            1: 38, 4: 14, 9: 31, 21: 42, 28: 84,
            36: 44, 51: 67, 71: 91, 80: 100
        }
        
        # Create board positions
        self.board_positions = self.create_board_positions()
        self.sound_enabled = True  # Sound effects toggle
        self.sound_enabled = True  # Sound effects toggle
        
        # Load dice images
        self.dice_images = self.load_dice_images()
        
        # Create player tokens
        self.player_tokens = self.create_player_tokens()

    def create_board_positions(self):
        positions = {}
        board_x = (SCREEN_WIDTH - BOARD_SIZE) // 2
        board_y = (SCREEN_HEIGHT - BOARD_SIZE) // 2
        
        for i in range(1, 101):
            row = (i - 1) // GRID_SIZE
            col = (i - 1) % GRID_SIZE
            
            # Reverse column order for odd rows to create snake pattern
            if row % 2 == 1:
                col = GRID_SIZE - 1 - col
            
            x = board_x + col * CELL_SIZE + CELL_SIZE // 2
            y = board_y + (GRID_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
            
            positions[i] = (x, y)
        
        return positions

    def load_dice_images(self):
        dice_images = []
        for i in range(1, 7):
            img = pygame.Surface((DICE_SIZE, DICE_SIZE))
            img.fill(WHITE)
            pygame.draw.rect(img, BLACK, (0, 0, DICE_SIZE, DICE_SIZE), 2)
            
            # Draw dots based on dice value
            if i == 1:
                pygame.draw.circle(img, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
            elif i == 2:
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 3:
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 4:
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 5:
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 6:
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, DICE_SIZE//2), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//2), 8)
                pygame.draw.circle(img, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
                pygame.draw.circle(img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            
            dice_images.append(img)
        
        return dice_images

    def create_player_tokens(self):
        tokens = []
        for color in PLAYER_COLORS:
            token = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(token, color, (PLAYER_SIZE//2, PLAYER_SIZE//2), PLAYER_SIZE//2)
            pygame.draw.circle(token, BLACK, (PLAYER_SIZE//2, PLAYER_SIZE//2), PLAYER_SIZE//2, 2)
            tokens.append(token)
        return tokens

    def add_player(self, name):
        if len(self.players) < 4:
            player_color = PLAYER_COLORS[len(self.players)]
            self.players.append({
                "name": name,
                "position": 1,
                "color": player_color,
                "token_index": len(self.players)
            })

    def roll_dice(self):
        if not self.dice_rolling and not self.moving_animation:
            dice_sound.play()
            self.dice_rolling = True
            self.dice_roll_time = pygame.time.get_ticks()

    def update_dice(self):
        if self.dice_rolling:
            current_time = pygame.time.get_ticks()
            if current_time - self.dice_roll_time > 1000:  # Roll for 1 second
                self.dice_rolling = False
                self.dice_value = random.randint(1, 6)
                self.start_move_animation()
            else:
                self.dice_value = random.randint(1, 6)

    def start_move_animation(self):
        player = self.players[self.current_player]
        old_position = player["position"]
        new_position = old_position + self.dice_value
        
        if new_position > 100:
            new_position = old_position  # Can't move beyond 100
        
        # Create animation path
        self.animation_path = []
        for pos in range(old_position, new_position + 1):
            self.animation_path.append(pos)
        
        # Check for snakes and ladders at the end position
        if new_position in self.snakes:
            self.animation_path.append(self.snakes[new_position])
        elif new_position in self.ladders:
            self.animation_path.append(self.ladders[new_position])
        
        if len(self.animation_path) > 1:  # Only animate if there's movement
            self.moving_animation = True
            self.animation_index = 1  # Start from the second position (after current)
            self.animation_start_time = pygame.time.get_ticks()
            move_sound.play()
        else:
            self.next_player_turn()

    def update_animation(self):
        if self.moving_animation:
            current_time = pygame.time.get_ticks()
            
            # Move to next position every 300ms
            if current_time - self.animation_start_time > 300:
                player = self.players[self.current_player]
                
                # Update player position
                player["position"] = self.animation_path[self.animation_index]
                
                # Check for snake or ladder
                if self.animation_index == len(self.animation_path) - 2:
                    current_pos = self.animation_path[self.animation_index]
                    next_pos = self.animation_path[self.animation_index + 1]
                    
                    if current_pos in self.snakes and self.snakes[current_pos] == next_pos:
                        snake_sound.play()
                    elif current_pos in self.ladders and self.ladders[current_pos] == next_pos:
                        ladder_sound.play()
                
                self.animation_index += 1
                self.animation_start_time = current_time
                
                # End of animation
                if self.animation_index >= len(self.animation_path):
                    self.moving_animation = False
                    
                    # Check for winner
                    if player["position"] == 100:
                        self.winner = self.current_player
                        win_sound.play()
                        self.game_state = "game_over"
                    else:
                        self.next_player_turn()

    def next_player_turn(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def draw_board(self):
        # Draw board background
        board_rect = pygame.Rect(
            (SCREEN_WIDTH - BOARD_SIZE) // 2,
            (SCREEN_HEIGHT - BOARD_SIZE) // 2,
            BOARD_SIZE,
            BOARD_SIZE
        )
        pygame.draw.rect(screen, BOARD_COLOR, board_rect)
        pygame.draw.rect(screen, BLACK, board_rect, 2)

        # Draw grid cells with alternating colors
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_x = board_rect.left + col * CELL_SIZE
                cell_y = board_rect.top + row * CELL_SIZE
                
                # Alternating cell colors
                if (row + col) % 2 == 0:
                    cell_color = (230, 230, 230)
                else:
                    cell_color = (210, 210, 210)
                
                pygame.draw.rect(screen, cell_color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GRID_COLOR, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 1)

        # Draw snakes
        for start, end in self.snakes.items():
            start_pos = self.board_positions[start]
            end_pos = self.board_positions[end]
            
            # Calculate control points for curved line
            control_x = (start_pos[0] + end_pos[0]) / 2 + random.randint(-50, 50)
            control_y = (start_pos[1] + end_pos[1]) / 2 + random.randint(-50, 50)
            
            # Draw snake body (curved line)
            points = []
            for t in range(0, 101, 5):
                t = t / 100
                # Quadratic Bezier curve
                x = (1-t)**2 * start_pos[0] + 2*(1-t)*t*control_x + t**2 * end_pos[0]
                y = (1-t)**2 * start_pos[1] + 2*(1-t)*t*control_y + t**2 * end_pos[1]
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, SNAKE_COLOR, False, points, 5)
            
            # Draw snake head
            pygame.draw.circle(screen, SNAKE_COLOR, start_pos, 10)
            
            # Draw snake tail
            pygame.draw.circle(screen, (200, 0, 0), end_pos, 7)

        # Draw ladders
        for start, end in self.ladders.items():
            start_pos = self.board_positions[start]
            end_pos = self.board_positions[end]
            
            # Calculate ladder width
            ladder_width = 10
            
            # Calculate perpendicular vector for ladder sides
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            length = (dx**2 + dy**2)**0.5
            
            if length > 0:
                perpx = -dy / length * ladder_width / 2
                perpy = dx / length * ladder_width / 2
                
                # Draw ladder sides
                pygame.draw.line(screen, LADDER_COLOR, 
                               (start_pos[0] + perpx, start_pos[1] + perpy),
                               (end_pos[0] + perpx, end_pos[1] + perpy), 3)
                pygame.draw.line(screen, LADDER_COLOR, 
                               (start_pos[0] - perpx, start_pos[1] - perpy),
                               (end_pos[0] - perpx, end_pos[1] - perpy), 3)
                
                # Draw ladder rungs
                num_rungs = int(length / 30)
                for i in range(1, num_rungs + 1):
                    t = i / (num_rungs + 1)
                    rung_x1 = start_pos[0] + dx * t + perpx
                    rung_y1 = start_pos[1] + dy * t + perpy
                    rung_x2 = start_pos[0] + dx * t - perpx
                    rung_y2 = start_pos[1] + dy * t - perpy
                    pygame.draw.line(screen, LADDER_COLOR, (rung_x1, rung_y1), (rung_x2, rung_y2), 2)

        # Draw numbers
        for i in range(1, 101):
            pos = self.board_positions[i]
            
            # Highlight special cells
            if i in self.snakes:
                pygame.draw.circle(screen, (255, 200, 200), pos, 15)
            elif i in self.ladders:
                pygame.draw.circle(screen, (200, 255, 200), pos, 15)
            
            num_text = font_small.render(str(i), True, BLACK)
            num_rect = num_text.get_rect(center=pos)
            screen.blit(num_text, num_rect)

    def draw_players(self):
        for i, player in enumerate(self.players):
            pos = self.board_positions[player["position"]]
            
            # Add offset to prevent overlapping
            offset_x = (i - len(self.players)/2 + 0.5) * (PLAYER_SIZE * 0.7)
            offset_y = (i - len(self.players)/2 + 0.5) * (PLAYER_SIZE * 0.3)
            player_pos = (pos[0] + offset_x, pos[1] + offset_y)
            
            # Draw player token
            token = self.player_tokens[player["token_index"]]
            token_rect = token.get_rect(center=player_pos)
            screen.blit(token, token_rect)

    def draw_dice(self):
        dice_x = SCREEN_WIDTH - DICE_SIZE - 40
        dice_y = (SCREEN_HEIGHT - DICE_SIZE) // 2
        dice_rect = pygame.Rect(dice_x, dice_y, DICE_SIZE, DICE_SIZE)
        
        # Draw dice label
        label = font_medium.render("DICE", True, BLACK)
        screen.blit(label, (dice_x + DICE_SIZE//2 - label.get_width()//2, dice_y - 40))
        
        # Draw dice
        if self.dice_rolling:
            screen.blit(self.dice_images[random.randint(0, 5)], dice_rect)
        else:
            screen.blit(self.dice_images[self.dice_value - 1], dice_rect)
        
        # Draw roll button
        roll_button = pygame.Rect(dice_x, dice_y + DICE_SIZE + 20, DICE_SIZE, 40)
        button_color = GREEN if not self.dice_rolling and not self.moving_animation else GRAY
        pygame.draw.rect(screen, button_color, roll_button)
        pygame.draw.rect(screen, BLACK, roll_button, 2)
        
        roll_text = font_small.render("Roll Dice", True, BLACK)
        roll_text_rect = roll_text.get_rect(center=roll_button.center)
        screen.blit(roll_text, roll_text_rect)
        
        return dice_rect, roll_button

    def draw_player_info(self):
        info_x = 20
        info_y = 20
        
        # Draw game title
        title = font_large.render("Snake and Ladders", True, BLUE)
        screen.blit(title, (info_x, info_y))
        
        # Draw player information
        for i, player in enumerate(self.players):
            y_pos = info_y + 60 + i * 50
            
            # Highlight current player
            if i == self.current_player:
                pygame.draw.rect(screen, LIGHT_BLUE, (info_x - 5, y_pos - 5, 250, 40))
                pygame.draw.rect(screen, BLACK, (info_x - 5, y_pos - 5, 250, 40), 1)
            
            # Draw player token
            token = self.player_tokens[player["token_index"]]
            screen.blit(token, (info_x, y_pos))
            
            # Draw player name and position
            name_text = font_medium.render(f"{player['name']}", True, player["color"])
            screen.blit(name_text, (info_x + 40, y_pos))
            
            pos_text = font_small.render(f"Position: {player['position']}", True, BLACK)
            screen.blit(pos_text, (info_x + 40, y_pos + 25))
        
        # Draw menu button
        menu_button = pygame.Rect(info_x, SCREEN_HEIGHT - 60, 120, 40)
        pygame.draw.rect(screen, ORANGE, menu_button)
        pygame.draw.rect(screen, BLACK, menu_button, 2)
        
        menu_text = font_small.render("Main Menu", True, BLACK)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        screen.blit(menu_text, menu_text_rect)
        
        return menu_button

    def draw_menu(self):
        # Draw background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title = font_title.render("Snake and Ladders", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        # Draw menu buttons
        button_width = 200
        button_height = 60
        button_spacing = 20
        start_y = 250
        
        # Play button
        play_button = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, start_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, play_button)
        pygame.draw.rect(screen, BLACK, play_button, 2)
        
        play_text = font_medium.render("Play Game", True, BLACK)
        play_text_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_text_rect)
        
        # Rules button
        rules_button = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, 
                                 start_y + button_height + button_spacing, 
                                 button_width, button_height)
        pygame.draw.rect(screen, YELLOW, rules_button)
        pygame.draw.rect(screen, BLACK, rules_button, 2)
        
        rules_text = font_medium.render("Game Rules", True, BLACK)
        rules_text_rect = rules_text.get_rect(center=rules_button.center)
        screen.blit(rules_text, rules_text_rect)
        
        # Credits button
        credits_button = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, 
                                   start_y + 2 * (button_height + button_spacing), 
                                   button_width, button_height)
        pygame.draw.rect(screen, ORANGE, credits_button)
        pygame.draw.rect(screen, BLACK, credits_button, 2)
        
        credits_text = font_medium.render("Credits", True, BLACK)
        credits_text_rect = credits_text.get_rect(center=credits_button.center)
        screen.blit(credits_text, credits_text_rect)
        
        # Quit button
        quit_button = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, 
                                start_y + 3 * (button_height + button_spacing), 
                                button_width, button_height)
        pygame.draw.rect(screen, RED, quit_button)
        pygame.draw.rect(screen, BLACK, quit_button, 2)
        
        quit_text = font_medium.render("Quit Game", True, BLACK)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(quit_text, quit_text_rect)
        
        # Draw decorative elements
        self.draw_decorative_elements()
        
        return play_button, rules_button, credits_button, quit_button

    def draw_decorative_elements(self):
        # Draw some decorative snakes and ladders around the menu
        
        # Snake 1
        points1 = [(100, 150), (150, 200), (100, 250), (150, 300), (100, 350)]
        pygame.draw.lines(screen, SNAKE_COLOR, False, points1, 5)
        pygame.draw.circle(screen, SNAKE_COLOR, points1[0], 10)
        
        # Snake 2
        points2 = [(SCREEN_WIDTH - 100, 150), (SCREEN_WIDTH - 150, 200), 
                  (SCREEN_WIDTH - 100, 250), (SCREEN_WIDTH - 150, 300), 
                  (SCREEN_WIDTH - 100, 350)]
        pygame.draw.lines(screen, SNAKE_COLOR, False, points2, 5)
        pygame.draw.circle(screen, SNAKE_COLOR, points2[0], 10)
        
        # Ladder 1
        pygame.draw.line(screen, LADDER_COLOR, (150, 400), (150, 550), 3)
        pygame.draw.line(screen, LADDER_COLOR, (180, 400), (180, 550), 3)
        for i in range(5):
            y = 420 + i * 30
            pygame.draw.line(screen, LADDER_COLOR, (150, y), (180, y), 2)
        
        # Ladder 2
        pygame.draw.line(screen, LADDER_COLOR, (SCREEN_WIDTH - 150, 400), 
                        (SCREEN_WIDTH - 150, 550), 3)
        pygame.draw.line(screen, LADDER_COLOR, (SCREEN_WIDTH - 180, 400), 
                        (SCREEN_WIDTH - 180, 550), 3)
        for i in range(5):
            y = 420 + i * 30
            pygame.draw.line(screen, LADDER_COLOR, (SCREEN_WIDTH - 150, y), 
                           (SCREEN_WIDTH - 180, y), 2)
        
        # Dice
        dice_img = self.dice_images[random.randint(0, 5)]
        screen.blit(dice_img, (SCREEN_WIDTH//2 - DICE_SIZE//2, SCREEN_HEIGHT - DICE_SIZE - 20))

    def draw_rules(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw rules panel
        panel_width = 700
        panel_height = 500
        panel = pygame.Rect(SCREEN_WIDTH//2 - panel_width//2, 
                          SCREEN_HEIGHT//2 - panel_height//2,
                          panel_width, panel_height)
        pygame.draw.rect(screen, WHITE, panel)
        pygame.draw.rect(screen, BLACK, panel, 3)
        
        # Draw title
        title = font_large.render("Game Rules", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, panel.top + 40))
        screen.blit(title, title_rect)
        
        # Draw rules text
        rules = [
            "1. Each player starts at position 1.",
            "2. Players take turns rolling the dice and moving their token.",
            "3. If a player lands on the bottom of a ladder, they climb up to the top.",
            "4. If a player lands on the head of a snake, they slide down to the tail.",
            "5. The first player to reach position 100 exactly wins the game.",
            "6. If a player's move would take them beyond position 100, they stay in place.",
            "7. Click the 'Roll Dice' button on your turn to roll the dice.",
            "8. Watch for animations showing your movement on the board."
        ]
        
        for i, rule in enumerate(rules):
            rule_text = font_small.render(rule, True, BLACK)
            screen.blit(rule_text, (panel.left + 50, panel.top + 100 + i * 30))
        
        # Draw close button
        close_button = pygame.Rect(SCREEN_WIDTH//2 - 60, panel.bottom - 60, 120, 40)
        pygame.draw.rect(screen, RED, close_button)
        pygame.draw.rect(screen, BLACK, close_button, 2)
        
        close_text = font_small.render("Close", True, BLACK)
        close_text_rect = close_text.get_rect(center=close_button.center)
        screen.blit(close_text, close_text_rect)
        
        return close_button

    def draw_credits(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw credits panel
        panel_width = 600
        panel_height = 400
        panel = pygame.Rect(SCREEN_WIDTH//2 - panel_width//2, 
                          SCREEN_HEIGHT//2 - panel_height//2,
                          panel_width, panel_height)
        pygame.draw.rect(screen, WHITE, panel)
        pygame.draw.rect(screen, BLACK, panel, 3)
        
        # Draw title
        title = font_large.render("Credits", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, panel.top + 40))
        screen.blit(title, title_rect)
        
        # Draw credits text
        credits = [
            "Enhanced Snake and Ladders Game",
            "",
            "Developed by: Your Name",
            "",
            "Graphics: Pygame",
            "",
            "Special thanks to:",
            "- The Pygame Community",
            "- All the players who enjoy this game"
        ]
        
        for i, line in enumerate(credits):
            credit_text = font_small.render(line, True, BLACK)
            credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH//2, panel.top + 100 + i * 30))
            screen.blit(credit_text, credit_rect)
        
        # Draw close button
        close_button = pygame.Rect(SCREEN_WIDTH//2 - 60, panel.bottom - 60, 120, 40)
        pygame.draw.rect(screen, RED, close_button)
        pygame.draw.rect(screen, BLACK, close_button, 2)
        
        close_text = font_small.render("Close", True, BLACK)
        close_text_rect = close_text.get_rect(center=close_button.center)
        screen.blit(close_text, close_text_rect)
        
        return close_button

    def draw_setup(self):
        # Draw background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title = font_large.render("Game Setup", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        # Draw player count selection
        count_text = font_medium.render("Select Number of Players:", True, BLACK)
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(count_text, count_rect)
        
        count_buttons = []
        for i in range(2, 5):
            button = pygame.Rect(SCREEN_WIDTH//2 - 150 + (i-2)*100, 200, 80, 60)
            color = GREEN if self.target_players == i else WHITE
            pygame.draw.rect(screen, color, button)
            pygame.draw.rect(screen, BLACK, button, 2)
            
            text = font_large.render(str(i), True, BLACK)
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)
            
            count_buttons.append(button)
        
        # Draw player name input section
        if self.target_players > 0:
            input_text = font_medium.render(f"Enter Player {len(self.players) + 1} Name:", True, BLACK)
            input_rect = input_text.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(input_text, input_rect)
            
            # Draw input box
            input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, 340, 300, 50)
            color = BLUE if self.input_active else WHITE
            pygame.draw.rect(screen, color, input_box)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            
            text_surface = font_medium.render(self.input_text, True, BLACK)
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
            
            # Draw add player button
            add_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 410, 200, 50)
            add_color = GREEN if self.input_text and len(self.players) < self.target_players else GRAY
            pygame.draw.rect(screen, add_color, add_button)
            pygame.draw.rect(screen, BLACK, add_button, 2)
            
            add_text = font_medium.render("Add Player", True, BLACK)
            add_text_rect = add_text.get_rect(center=add_button.center)
            screen.blit(add_text, add_text_rect)
            
            # Draw player list
            player_list_y = 480
            if len(self.players) > 0:
                list_text = font_medium.render("Players:", True, BLACK)
                screen.blit(list_text, (SCREEN_WIDTH//2 - 150, player_list_y))
                
                for i, player in enumerate(self.players):
                    token = self.player_tokens[player["token_index"]]
                    screen.blit(token, (SCREEN_WIDTH//2 - 150, player_list_y + 40 + i * 40))
                    
                    player_text = font_medium.render(player["name"], True, player["color"])
                    screen.blit(player_text, (SCREEN_WIDTH//2 - 110, player_list_y + 40 + i * 40))
            
            # Draw start game button
            start_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 60)
            start_color = GREEN if len(self.players) == self.target_players else GRAY
            pygame.draw.rect(screen, start_color, start_button)
            pygame.draw.rect(screen, BLACK, start_button, 2)
            
            start_text = font_medium.render("Start Game", True, BLACK)
            start_text_rect = start_text.get_rect(center=start_button.center)
            screen.blit(start_text, start_text_rect)
            
            # Draw back button
            back_button = pygame.Rect(50, SCREEN_HEIGHT - 100, 120, 50)
            pygame.draw.rect(screen, ORANGE, back_button)
            pygame.draw.rect(screen, BLACK, back_button, 2)
            
            back_text = font_medium.render("Back", True, BLACK)
            back_text_rect = back_text.get_rect(center=back_button.center)
            screen.blit(back_text, back_text_rect)
            
            return count_buttons, input_box, add_button, start_button, back_button
        
        return count_buttons, None, None, None, None

    def draw_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Draw game over panel
        panel_width = 500
        panel_height = 300
        panel = pygame.Rect(SCREEN_WIDTH//2 - panel_width//2, 
                          SCREEN_HEIGHT//2 - panel_height//2,
                          panel_width, panel_height)
        pygame.draw.rect(screen, WHITE, panel)
        pygame.draw.rect(screen, BLACK, panel, 3)
        
        # Draw winner information with celebration effects
        winner = self.players[self.winner]
        
        # Draw celebratory particles
        current_time = pygame.time.get_ticks() // 100  # Used for animation
        for i in range(20):
            x = SCREEN_WIDTH//2 + int(math.sin(current_time * 0.1 + i) * 200)
            y = SCREEN_HEIGHT//2 + int(math.cos(current_time * 0.1 + i) * 100)
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            pygame.draw.circle(screen, color, (x, y), 5)
        
        # Animated congratulations text
        scale = 1.0 + math.sin(current_time * 0.2) * 0.1  # Pulsing effect
        congrats_text = font_large.render("Congratulations!", True, BLUE)
        congrats_text = pygame.transform.scale(congrats_text, 
                                             (int(congrats_text.get_width() * scale), 
                                              int(congrats_text.get_height() * scale)))
        congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH//2, panel.top + 60))
        screen.blit(congrats_text, congrats_rect)
        
        # Animated winner text
        winner_text = font_large.render(f"{winner['name']} Wins!", True, winner["color"])
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH//2, panel.top + 120))
        screen.blit(winner_text, winner_rect)
        
        # Animated winner token with rotation
        token = pygame.transform.scale(self.player_tokens[winner["token_index"]], (60, 60))
        token = pygame.transform.rotate(token, current_time * 2)  # Rotating effect
        token_rect = token.get_rect(center=(SCREEN_WIDTH//2, panel.top + 180))
        screen.blit(token, token_rect)
        
        # Draw only the main menu button
        menu_button = pygame.Rect(SCREEN_WIDTH//2 - 80, panel.bottom - 60, 160, 50)
        pygame.draw.rect(screen, ORANGE, menu_button)
        pygame.draw.rect(screen, BLACK, menu_button, 2)
        
        menu_text = font_medium.render("Main Menu", True, BLACK)
        menu_rect = menu_text.get_rect(center=menu_button.center)
        screen.blit(menu_text, menu_rect)
        
        return menu_button

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN:
                if self.game_state == "setup" and self.input_active:
                    if event.key == K_RETURN:
                        if self.input_text and len(self.players) < self.target_players:
                            self.add_player(self.input_text)
                            self.input_text = ""
                    elif event.key == K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        # Limit name length
                        if len(self.input_text) < 15:
                            self.input_text += event.unicode
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.game_state == "menu":
                    if self.show_rules:
                        close_button = self.draw_rules()
                        if close_button.collidepoint(mouse_pos):
                            self.show_rules = False
                    elif self.show_credits:
                        close_button = self.draw_credits()
                        if close_button.collidepoint(mouse_pos):
                            self.show_credits = False
                    else:
                        play_button, rules_button, credits_button, quit_button = self.draw_menu()
                        
                        if play_button.collidepoint(mouse_pos):
                            self.game_state = "setup"
                            self.target_players = 0
                            self.players = []
                        elif rules_button.collidepoint(mouse_pos):
                            self.show_rules = True
                        elif credits_button.collidepoint(mouse_pos):
                            self.show_credits = True
                        elif quit_button.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
                
                elif self.game_state == "setup":
                    count_buttons, input_box, add_button, start_button, back_button = self.draw_setup()
                    
                    # Handle player count selection
                    for i, button in enumerate(count_buttons):
                        if button.collidepoint(mouse_pos):
                            self.target_players = i + 2
                            self.players = []
                            self.input_text = ""
                            break
                    
                    if input_box and input_box.collidepoint(mouse_pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                    
                    if add_button and add_button.collidepoint(mouse_pos) and self.input_text and len(self.players) < self.target_players:
                        self.add_player(self.input_text)
                        self.input_text = ""
                    
                    if start_button and start_button.collidepoint(mouse_pos) and len(self.players) == self.target_players:
                        self.game_state = "game"
                        self.current_player = 0
                        self.winner = None
                    
                    if back_button and back_button.collidepoint(mouse_pos):
                        self.game_state = "menu"
                
                elif self.game_state == "game":
                    if self.winner is not None:
                        play_again_button, menu_button = self.draw_game_over()
                        
                        if play_again_button.collidepoint(mouse_pos):
                            # Reset game with same players
                            for player in self.players:
                                player["position"] = 1
                            self.current_player = 0
                            self.winner = None
                            self.dice_value = 1
                        
                        elif menu_button.collidepoint(mouse_pos):
                            self.game_state = "menu"
                    
                    else:
                        dice_rect, roll_button = self.draw_dice()
                        menu_button = self.draw_player_info()
                        
                        if roll_button.collidepoint(mouse_pos) and not self.dice_rolling and not self.moving_animation:
                            self.roll_dice()
                        
                        if menu_button.collidepoint(mouse_pos):
                            self.game_state = "menu"

    def update(self):
        if self.game_state == "game":
            self.update_dice()
            self.update_animation()

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        
        if self.game_state == "menu":
            if self.show_rules:
                self.draw_menu()
                self.draw_rules()
            elif self.show_credits:
                self.draw_menu()
                self.draw_credits()
            else:
                self.draw_menu()
        
        elif self.game_state == "setup":
            self.draw_setup()
        
        elif self.game_state == "game":
            self.draw_board()
            self.draw_players()
            self.draw_dice()
            self.draw_player_info()
            
            if self.winner is not None:
                self.draw_game_over()
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = EnhancedSnakeAndLadderGame()
    
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
