import pygame
import os
import random
from enemy import Enemy

# === Initialization ===
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

# === Constants ===
FPS = 60
WIDTH, HEIGHT = 900, 500
SPAWN_EVENT = pygame.USEREVENT + 1

# === Window ===
window = pygame.display.set_mode((WIDTH, HEIGHT))

# === Assets ===
player_img = pygame.image.load(os.path.join('Assets', 'cursor.png'))
player_attack_img = pygame.image.load(os.path.join('Assets', 'cursor_clicked.png'))
castle_img = pygame.image.load(os.path.join('Assets', 'background.png'))
cursor_click_sound = pygame.mixer.Sound(os.path.join('Assets', 'SD_cursor_clicked.wav'))
cursor_click_sound.set_volume(0.4)

# === Enemy Settings ===
enemy_list = []
spawn_time = 5
pygame.time.set_timer(SPAWN_EVENT, round(spawn_time * 1000))
spawn_x_min = 30
spawn_x_max = WIDTH - 30
spawn_y_min = 10
spawn_y_max = HEIGHT - 400


def draw_window(mouse_pos, left_click):
    #Draws the background, enemies, and player cursor each frame
    window.fill((255, 255, 255))
    window.blit(castle_img, (0, 0))

    # Handle enemy clicks and draw them
    for enemy in enemy_list[:]:
        if enemy.pygame_rect.collidepoint(mouse_pos) and left_click:
            enemy.take_damage(10)

        if enemy.health <= 0:
            enemy_list.remove(enemy)

    for enemy in enemy_list:
        enemy.draw(window)

    if left_click:
        cursor_img = player_attack_img
        cursor_click_sound.play()
    else:
        cursor_img = player_img

    window.blit(
        cursor_img,(mouse_pos[0] - player_img.get_width() * 0.5,mouse_pos[1] - player_img.get_height() * 0.1)
    )

    # == Debug visuals ==
    # rect = pygame.Rect(x, y, width, height)
    #castle_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
    #castle_tower_left_rect = pygame.Rect(0, HEIGHT - 90, 90, 90)
    #castle_tower_right_rect = pygame.Rect(WIDTH-90, HEIGHT - 90, 90, 90)

    #pygame.draw.rect(window, (255, 0, 255), castle_tower_left_rect, 2)
    #pygame.draw.rect(window, (255, 0, 255), castle_tower_right_rect, 2)
    #pygame.draw.rect(window, (255, 0, 0), castle_rect, 2)
    pygame.display.flip()


def spawn_enemy(count):
    #Spawns a specified number of enemies at random positions
    for _ in range(count):
        x = random.randint(spawn_x_min, spawn_x_max)
        y = random.randint(spawn_y_min, spawn_y_max)
        enemy = Enemy(pygame_rect=pygame.Rect(x, y, 25, 25))
        enemy_list.append(enemy)


def main():
    #Main game loop
    global spawn_time
    clock = pygame.time.Clock()
    running = True
    enemy_count = 2
    spawned_round = 0

    while running:
        clock.tick(FPS)
        left_click = False
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
            elif event.type == SPAWN_EVENT:
                if len(enemy_list) < enemy_count:
                    spawned_round += 1
                    spawn_enemy(round(enemy_count))
                    enemy_count += enemy_count * 0.10
                    spawn_time += spawn_time * 0.25
        
        # rect = pygame.Rect(x, y, width, height)
        castle_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
        castle_tower_left_rect = pygame.Rect(0, HEIGHT - 90, 90, 90)
        castle_tower_right_rect = pygame.Rect(WIDTH-90, HEIGHT - 90, 90, 90)
        for enemy in enemy_list:
            if not castle_rect.colliderect(enemy.pygame_rect):
                if not castle_tower_left_rect.colliderect(enemy.pygame_rect):
                    if not castle_tower_right_rect.colliderect(enemy.pygame_rect):
                        enemy.move()

        draw_window(mouse_pos, left_click)
    pygame.quit()


if __name__ == "__main__":
    main()
