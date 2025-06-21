import pygame
import sys

pygame.init()

# === SETTINGS ===
INTERNAL_WIDTH = 320
INTERNAL_HEIGHT = 180
FPS = 60
AVAILABLE_RESOLUTIONS = [
    (640, 360),
    (1280, 720),
    (1920, 1080)
]

# === START IN WINDOWED MODE ===
current_resolution_index = 1  # Start at 1280x720
windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
is_fullscreen = False

# Create display
screen = pygame.display.set_mode(windowed_resolution, pygame.RESIZABLE)
pygame.display.set_caption("Resolution + Fullscreen Template")

# Internal surface (game world)
game_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))

clock = pygame.time.Clock()

# Example object
player_color = (255, 0, 0)
player_rect = pygame.Rect(50, 50, 16, 16)

def toggle_fullscreen():
    global is_fullscreen, screen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(windowed_resolution, pygame.RESIZABLE)

def change_resolution(delta):
    global current_resolution_index, windowed_resolution, screen
    current_resolution_index = (current_resolution_index + delta) % len(AVAILABLE_RESOLUTIONS)
    windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
    if not is_fullscreen:
        screen = pygame.display.set_mode(windowed_resolution, pygame.RESIZABLE)

# === MAIN LOOP ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
            elif event.key == pygame.K_LEFT:
                change_resolution(-1)
            elif event.key == pygame.K_RIGHT:
                change_resolution(1)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # === DRAW TO INTERNAL GAME SURFACE ===
    game_surface.fill((20, 20, 30))  # Background
    pygame.draw.rect(game_surface, player_color, player_rect)

    # === SCALE INTERNAL SURFACE TO FIT WINDOW ===
    window_width, window_height = screen.get_size()
    scaled_surface = pygame.transform.scale(game_surface, (window_width, window_height))
    screen.blit(scaled_surface, (0, 0))

    pygame.display.set_caption(f"Resolution: {window_width}x{window_height} | Press ←/→ to change, F11 to toggle fullscreen")
    pygame.display.flip()
    clock.tick(FPS)
