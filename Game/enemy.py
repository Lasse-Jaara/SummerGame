import pygame
import os

# === Initialization ===
pygame.init()
pygame.mixer.init()

# === Assets ===
mossya_img = pygame.image.load(os.path.join('Assets', 'mossya.png'))
mossya_hurted_img = pygame.image.load(os.path.join('Assets', 'mossya_hurted.png'))

mossya_hurted_sound = pygame.mixer.Sound(os.path.join('Assets', 'SD_mossya_hurt.wav'))
mossya_death_sound = pygame.mixer.Sound(os.path.join('Assets', 'SD_mossya_death.wav'))  # Currently unused
mossya_hurted_sound.set_volume(0.3)
mossya_death_sound.set_volume(0.1)
class Enemy:
    hurt_sound = mossya_hurted_sound
    death_sound = mossya_death_sound
    def __init__(self, pygame_rect=pygame.Rect(0, 0, 25, 25), health=20,
                 image=mossya_img, hurted_image=mossya_hurted_img):

        self.health = health
        self.image = image
        self.hurted_image = hurted_image
        self.pygame_rect = pygame_rect
        self.hurted = False
        self.hurt_timer = 0

    def take_damage(self, amount):
        self.health -= amount
        self.hurted = True
        self.hurt_timer = 5
        Enemy.hurt_sound.play()
        if self.health <= 0:
            Enemy.death_sound.play()

    def draw(self, window):
        if self.hurt_timer > 0:
            window.blit(self.hurted_image, self.pygame_rect)
            self.hurt_timer -= 1
        else:
            window.blit(self.image, self.pygame_rect)

    def move(self, speed=1):
        self.pygame_rect.y += speed
