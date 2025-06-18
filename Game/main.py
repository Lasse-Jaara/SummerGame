import pygame

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
img = pygame.image.load('player.png').convert_alpha()
running = True
x = 0
player = pygame.Rect(0, 0, 50, 50)

delta_time = 0.1
while running:
    pygame.mouse.set_visible(False)
    screen.fill((255, 255, 255))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Draw image at mouse position
    screen.blit(img, (mouse_x - img.get_width() * 0.5, mouse_y - img.get_height() * 0.1 )) # center mouse cursor to cursor tip on image


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000 # limits FPS to 60
    delta_time = max(0.001, min(0.1, delta_time))  # Ensure delta_time is never zero

pygame.quit()