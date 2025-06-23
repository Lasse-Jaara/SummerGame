import pygame
import os
import random
# Here all variables and constants are defined, such as screen size, colors, etc.
fps = 60
width, height = 900, 500
window = pygame.display.set_mode((width, height)) # Set the window size base of the WIDTH and HEIGHT variables

# Here load images and other assets
player_img = pygame.image.load(os.path.join('Assets', 'cursor.png'))
castle_img = pygame.image.load(os.path.join('Assets', 'background.png'))
mossya_img = pygame.image.load(os.path.join('Assets', 'enemy_1.png'))

pygame.init() # start all necessary systems (graphics, sound, input, etc.)
pygame.mouse.set_visible(False) # Hide the mouse cursor


def draw_window(mouse_x, mouse_y): # Draws the game window and updates the display and all assets -- pass here all things you want to draw
    pygame.display.flip() # Update the display
    window.fill((255, 255, 255)) # Fill the screen with white color *reset the frame*
    window.blit(castle_img, (0, 0))  # Draw the background image
    window.blit(mossya_img, (width // 2, height // 2))  # Draw the background image
    window.blit(player_img, (mouse_x - player_img.get_width() * 0.5, mouse_y - player_img.get_height() * 0.1 )) # center mouse cursor to cursor tip on image

def spawn_enemy():  # Function to spawn an enemy at a random position
    pass
        #x = random.randint(1,100)
        #print(x)
def main(): # Here you can add game logic, update positions, etc.
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)  # Limit the frame rate to FPS
        left_click = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True


        spawn_enemy()
        draw_window(mouse_x, mouse_y)  # Call the draw function to update the display
    pygame.quit()


if __name__ == "__main__": # Starts the game if is file opened directly
    main()