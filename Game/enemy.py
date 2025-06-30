import pygame
import os
mossya_img = pygame.image.load(os.path.join('Assets', 'mossya.png'))
mossya_hurted_img = pygame.image.load(os.path.join('Assets', 'mossya_hurted.png'))

class Enemy:
    def __init__(self,pygame_rect=pygame.Rect(0, 0, 25, 25), health=30, image=mossya_img, hurted_image=mossya_hurted_img): #  __init__ function is called automatically every time the class is being used to create a new class instance.
        # Attributes
        self.health = health
        self.image = image
        self.hurted_image = hurted_image
        self.pygame_rect = pygame_rect
        self.hurted = False  # Track if recently damaged

    # Methods
    def take_damage(self, amount):
        self.health -= amount
        self.hurted = True

    def draw(self, window):
        if self.hurted:
            window.blit(self.hurted_image, self.pygame_rect)
        else:
            window.blit(self.image, self.pygame_rect)
        self.hurted = False  # Reset after drawing

    def move(self, speed=1):
        self.pygame_rect.y += speed
        