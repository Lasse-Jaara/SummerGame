import pygame
import os
import random
#from enemy import Enemy  # <--- Import your enemy class

# Here all variables and constants are defined, such as screen size, colors, etc.
fps = 60
width, height = 900, 500
window = pygame.display.set_mode((width, height)) # Set the window size base of the WIDTH and HEIGHT variables

spawn_x_min = 30
spawn_x_max = width -30
spawn_y_min = 10
spawn_y_max = height -400
can_enemy_spawn = True  # Variable to control enemy spawning
# Here load images and other assets
player_img = pygame.image.load(os.path.join('Assets', 'cursor.png'))
player_attack_img = pygame.image.load(os.path.join('Assets', 'cursor_clicked.png'))
castle_img = pygame.image.load(os.path.join('Assets', 'background.png'))
#mossya_img = pygame.image.load(os.path.join('Assets', 'mossya.png'))
#mossya_hurted_img = pygame.image.load(os.path.join('Assets', 'mossya_hurted.png'))
enemy_list = []
spawn_time = 5
SPAWN_EVENT = pygame.USEREVENT + 1 # Custom event for spawning enemies
pygame.time.set_timer(SPAWN_EVENT, round(spawn_time*1000))  # Every 1000x ms

pygame.init() # start all necessary systems (graphics, sound, input, etc.)
pygame.mouse.set_visible(False) # Hide the mouse cursor


def draw_window(mouse_pos, left_click, ): # Draws the game window and updates the display and all assets -- pass here all things you want to draw
    pygame.display.flip() # Update the display
    window.fill((255, 255, 255)) # Fill the screen with white color *reset the frame*
    window.blit(castle_img, (0, 0))  # Draw the background image

    for enemy in enemy_list:
            if enemy.pygame_rect.collidepoint((mouse_pos[0], mouse_pos[1])) and left_click:
                enemy.take_damage(10)
            if enemy.health <= 0:
                enemy_list.remove(enemy)
            enemy.draw(window)
    
    if(left_click):
        window.blit(player_attack_img, (mouse_pos[0] - player_img.get_width() * 0.5, mouse_pos[1] - player_img.get_height() * 0.1 )) # center mouse cursor to cursor tip on image
    else:
        window.blit(player_img, (mouse_pos[0] - player_img.get_width() * 0.5, mouse_pos[1] - player_img.get_height() * 0.1 )) # center mouse cursor to cursor tip on image

def spawn_enemy(count):  # Function to spawn an enemy at a random position
    for _ in range(count):  # load some enemies
        x = random.randint(spawn_x_min, spawn_x_max)
        y = random.randint(spawn_y_min, spawn_y_max)
        enemy = Enemy(pygame_rect=pygame.Rect(x, y, 25, 25))
        enemy_list.append(enemy)

def main(): # Here you can add game logic, update positions, etc.
    global spawn_time
    clock = pygame.time.Clock()
    running = True
    enemy_count = 2  # Number of enemies to spawn initially
    spawned_round = 0
    while running:
        clock.tick(fps)  # Limit the frame rate to FPS
        left_click = False
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
            if event.type == SPAWN_EVENT: # event that start every 5 seconds
                if (len(enemy_list) < enemy_count): # if less enemies are than it would try spawn in arena
                    spawned_round += 1
                    spawn_enemy(round(enemy_count)) # spawn enemies but still keep 20% increase every time
                    enemy_count += enemy_count * 0.10
                    spawn_time += spawn_time * 0.25

        castle_rect = pygame.Rect(0, height-90, width, 90)
        #pygame.draw.rect(window, (255, 0, 0), castle_rect, 2)
        for enemy in enemy_list:
            if castle_rect.colliderect(enemy.pygame_rect):
                pass
            else:
                enemy.move()
        #check_collisions(mouse_x, mouse_y, left_click)  # Check for collisions with enemies
        draw_window(mouse_pos, left_click)  # Call the draw function to update the display
    pygame.quit()


if __name__ == "__main__": # Starts the game if is file opened directly
    main()