import pygame
import sys
import os
import random

game_name = "Geometry Arsch"

# Initialisieren von pygame
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(game_name)

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
GRAY = (80, 80, 80)
LIGHT_BLUE = (173, 216, 230)

# Spielstatus
MENU = 0
PLAYING = 1
GAME_OVER = 2
LEVEL_COMPLETE = 3
game_state = MENU

# Spielereigenschaften
player_size = 40 #  größe vom spieler
player_x = 200
player_y = HEIGHT - 150
player_y_velocity = 0
gravity = 0.8
jump_strength = -16
is_jumping = False
rotation_angle = 0

# Sprungeigentschaften
is_on_surface = False
coyote_time = 0 # added zeit um nach dem fallen noch springen zu können
coyote_time_max = 6 # ca. 0.1 seconds
jump_buffer = 0 # added zeit um vor dem aufprall einen jump zu machen
jump_buffer_max = 6 # ca. 0.1 seconds
jump_requested = False

# Kamera und Leveleigenschaften
camera_x = 0
ground_height = HEIGHT - 100
game_speed = 7

# Levelelemente
GROUND = "G"
SPIKE = "S"
EMPTY = "."
PORTAL_END = "E"

GRID_SIZE = 40

level_objects = []
level_width = 0
level_name = "Level 1"

# Hintergrund
bg_elements = []
for i in range(20):
    bg_elements.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT - 150),
        "size": random.randint(2, 6),
        "speed": random.uniform(0.2, 0.5)
    })


# GAME MAIN LOOP (LOOP GEHT SO LANGE BIS DAS SPIEL BEENDET WIRD)
# HIER KOMMT DAS SPIEL...


# GANZ UNTEN, SPIEL BEENDEN
pygame.quit()
sys.exit()
