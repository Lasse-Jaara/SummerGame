import pygame
import os

# === Initialization ===
pygame.init()
pygame.mixer.init()


# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, 'Assets')

# === Assets ===
mossya_img = pygame.image.load(os.path.join(assets_dir, 'mossya.png'))
mossya_hurted_img = pygame.image.load(os.path.join(assets_dir, 'mossya_hurted.png'))

mossya_hurted_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'SD_mossya_hurt.wav'))
mossya_death_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'SD_mossya_death.wav'))  # Currently unused
mossya_hurted_sound.set_volume(0.3)
mossya_death_sound.set_volume(0.1)

class Mossya:
    hurt_sound = mossya_hurted_sound
    death_sound = mossya_death_sound
    def __init__(self, pygame_rect=pygame.Rect(0, 0, 25, 25), health=20,image=mossya_img, hurted_image=mossya_hurted_img):

        self.health = health
        self.image = image
        self.hurted_image = hurted_image
        self.pygame_rect = pygame_rect
        self.hurted = False
        self.hurt_timer = 0
        self.died_to_castle = False

    def take_damage(self, amount):
        self.health -= amount
        self.hurted = True
        self.hurt_timer = 5
        Mossya.hurt_sound.play()
        if self.health <= 0:
            Mossya.death_sound.play()

    def draw(self, window):
        if self.hurt_timer > 0:
            window.blit(self.hurted_image, self.pygame_rect)
            self.hurt_timer -= 1
        else:
            window.blit(self.image, self.pygame_rect)
        #pygame.draw.rect(window, (255, 0, 255), self.pygame_rect, 2)
    def move(self, speed=1): # needs be 1,2,3,etc not 0,5 etc. You cant move object half pixsel
        self.pygame_rect.y += speed

    def die_to_castle(self):
        self.died_to_castle = True
        self.take_damage(1000)