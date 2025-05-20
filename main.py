import pygame
import sys
import os
import random

from astropy.io.fits import GroupData

game_name = "Geometry Arsch"

# Initialisieren von pygame
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(game_name)

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
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
jump_strength = -18
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


# Texturen
try:
    ground_image = pygame.Surface((GRID_SIZE, GRID_SIZE))
    ground_image.fill(GRAY)

    spike_image = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.polygon(spike_image, RED, [(0, GRID_SIZE), (GRID_SIZE // 2, 0), (GRID_SIZE, GRID_SIZE)])    # dreieck

    portal_end_image = pygame.Surface((GRID_SIZE, GRID_SIZE * 2), pygame.SRCALPHA)
    pygame.draw.rect(portal_end_image, GREEN, (0, 0, GRID_SIZE, GRID_SIZE * 2), border_radius=10)

    player_image = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
    pygame.draw.rect(player_image, BLUE, (0, 0, player_size, player_size))
    pygame.draw.rect(player_image, BLACK, (player_size - 20, 8, 12, 12)) #augen
except Exception as e:
    print(f"Fehler beim laden der Textur: {e}")
    pygame.quit()
    sys.exit()

# Level
def load_level(filename):
    global level_objects, level_width, level_name

    level_objects = []

    try:
        with open(filename, "r") as file:
            level_name = file.readline().strip()

            rows = []
            for line in file:
                if line.strip():
                    rows.append(line.strip())

            height = len(rows)
            width = max(len(row) for row in rows)
            level_width = width * GRID_SIZE

            for y, row in enumerate(rows):
                for x, cell in enumerate(row):
                    grid_x = x * GRID_SIZE
                    grid_y = y * GRID_SIZE

                    if cell == GROUND:
                        level_objects.append({
                            "type": GROUND,
                            "x": grid_x,
                            "y": grid_y,
                            "width": GRID_SIZE,
                            "height": GRID_SIZE
                        })

                    elif cell == SPIKE:
                        level_objects.append({
                            "type": SPIKE,
                            "x": grid_x,
                            "y": grid_y,
                            "width": GRID_SIZE,
                            "height": GRID_SIZE
                        })

                    elif cell == PORTAL_END:
                        level_objects.append({
                            "type": PORTAL_END,
                            "x": grid_x,
                            "y": grid_y,
                            "width": GRID_SIZE,
                            "height": GRID_SIZE * 2
                        })

        print(f"Successfully loaded {len(level_objects)} game objects from {filename}.")
        return True
    except Exception as e:
        print(f"Error loading level: {e}")
        return False

# Reset game
def reset_game():
    global player_x, player_y, player_y_velocity, is_jumping, rotation_angle, camera_x, game_state
    global is_on_surface, coyote_time, jump_buffer, jump_requested
    player_x = 200
    player_y = HEIGHT - 150
    player_y_velocity = 0
    is_jumping = False
    rotation_angle = 0
    camera_x = 0
    game_state = PLAYING
    is_on_surface = False
    coyote_time = 0
    jump_buffer = 0
    jump_requested = False


# Level laden
level_file = "level.txt"
if not os.path.exists(level_file):
    print(f"The level file {level_file} does not exist.")

if not load_level(level_file):
    print("Failed to load level.")

clock = pygame.time.Clock()         # FPS
debug_font = pygame.font.SysFont(None, 24)

running = True
while running:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # WIRD AUSGEFÜHRT WENN DER SPIELER SPACE DRÜCKT
                if game_state == MENU or game_state == GAME_OVER or game_state == LEVEL_COMPLETE:
                    reset_game()
                elif game_state == PLAYING:
                    jump_requested = True
                    jump_buffer = jump_buffer_max

    # HIER KOMMT DER INGAME CODE
    if game_state == PLAYING:
        # Gravity
        player_y_velocity += gravity
        player_y += player_y_velocity

        camera_x += game_speed

        if is_jumping:
            rotation_angle = (rotation_angle + 7) % 360

        # Kollisionen
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)         #erstellt den spieler
        was_on_surface = is_on_surface
        is_on_surface = False

        ground_check_rect = pygame.Rect(            # Hitbox
            player_rect.x,
            player_rect.y + player_rect.height - 5,
            player_rect.width,
            10
        )

        for obj in level_objects:
            obj_rect = pygame.Rect(
                obj["x"] - camera_x,
                obj["y"],
                obj["width"],
                obj["height"]
            )

            if obj["type"] == GROUND:
                if ground_check_rect.colliderect(obj_rect):
                    if player_y_velocity >= 0: # FALLS DER SPIELER SICH BEWEGT
                        player_y = obj_rect.top - player_size
                        player_y_velocity = 0
                        is_on_surface = True
                        rotation_angle = 0

                elif player_rect.colliderect(obj_rect) and not is_on_surface:
                    if not (player_rect.bottom - 5 <= obj_rect.top):
                        game_state = GAME_OVER

            elif obj["type"] == SPIKE:
                if player_rect.colliderect(obj_rect):
                    game_state = GAME_OVER

            elif obj["type"] == PORTAL_END:
                if player_rect.colliderect(obj_rect):
                    game_state = LEVEL_COMPLETE

        # Coyote Jump Time
        if was_on_surface and not is_on_surface:
            coyote_time = coyote_time_max
        elif not is_on_surface:
            if coyote_time > 0:
                coyote_time -= 1

        # Buffer Jump Time
        if jump_buffer > 0:
            jump_buffer -= 1

        # Jump
        if (jump_requested or jump_buffer > 0) and (is_on_surface or coyote_time > 0):
            player_y_velocity = jump_strength
            is_jumping = True
            jump_requested = False
            jump_buffer = 0
            coyote_time = 0

        if not pygame.key.get_pressed()[pygame.K_SPACE]:
            jump_requested = False

        is_jumping = not is_on_surface

        if player_y > HEIGHT:
            game_state = GAME_OVER

        if player_y < 0:
            player_y = 0
            player_y_velocity = 0

        if camera_x >= level_width - WIDTH:
            game_state = LEVEL_COMPLETE

    # Drawing (Objekte im Fenster anzeigen)
    screen.fill(LIGHT_BLUE)

    # Hintergrundobjekte
    for bg in bg_elements:                  # Kreiseigenschaften
        bg["x"] -= bg["speed"] * game_speed
        if bg["x"] < 0:
            bg["x"] = WIDTH
            bg["y"] = random.randint(0, HEIGHT - 150)
        pygame.draw.circle(screen, WHITE, (int(bg["x"]), int(bg["y"])), int(bg["size"]))

    # Levelobjekte
    for obj in level_objects:
        if -200 <= obj["x"] - camera_x <= WIDTH:
            if obj["type"] == GROUND:
                screen.blit(ground_image, (obj["x"] - camera_x, obj["y"]))
            elif obj["type"] == SPIKE:
                screen.blit(spike_image, (obj["x"] - camera_x, obj["y"]))
            elif obj["type"] == PORTAL_END:
                screen.blit(portal_end_image, (obj["x"] - camera_x, obj["y"]))

    # Spieler
    rotated_player = pygame.transform.rotate(player_image, rotation_angle)
    rotated_rect = rotated_player.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
    screen.blit(rotated_player, rotated_rect.topleft)

    # Draw UI
    font = pygame.font.SysFont(None, 36)

    if game_state == MENU:
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render('GEOMETRY ASS', True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        level_text = font.render(f"Level: {level_name}", True, BLACK)
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 50))

        instruction_text = font.render("Press SPACE to Start", True, BLACK)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))

    elif game_state == GAME_OVER:
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

        restart_text = font.render('Press SPACE to Restart', True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    elif game_state == LEVEL_COMPLETE:
        complete_font = pygame.font.SysFont(None, 72)
        complete_text = complete_font.render('LEVEL COMPLETE!', True, (255, 0, 255))
        screen.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 3))

        restart_text = font.render('Press SPACE to Play Again', True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    if game_state == PLAYING:
        progress = min(1.0, camera_x / (level_width - WIDTH))
        pygame.draw.rect(screen, BLACK, (50, 20, WIDTH - 100, 10), 1)
        pygame.draw.rect(screen, BLUE, (50, 20, int((WIDTH - 100) * progress), 10))

    pygame.display.flip()

# GANZ UNTEN, SPIEL BEENDEN
pygame.quit()
sys.exit()