import pygame
import os
import random

# === Initialization ===
pygame.init()
pygame.mixer.init()


# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, 'Assets')

# === Assets ===
xp_orb_img = pygame.image.load(os.path.join(assets_dir, 'xp_orb.png'))

pi = pygame.mixer.Sound(os.path.join(assets_dir, 'pi.mp3'))
po = pygame.mixer.Sound(os.path.join(assets_dir, 'po.mp3'))
poup = pygame.mixer.Sound(os.path.join(assets_dir, 'poup.mp3'))
pu = pygame.mixer.Sound(os.path.join(assets_dir, 'pu.mp3'))

class Xp_Orb:
    pi_sound = pi
    po_sound = po
    poup_sound = poup
    pu_sound = pu

    def __init__(self, pygame_rect=pygame.Rect(0, 0, 25, 25),image=xp_orb_img):
        self.image = image
        self.pygame_rect = pygame_rect
        

    def sound(self):
        random_number = random.randint(1, 4)
        if random_number==1:
            Xp_Orb.pi_sound.play()
        elif random_number==2:
            Xp_Orb.po_sound.play()
        elif random_number==3:
            Xp_Orb.poup_sound.play()
        else:
            Xp_Orb.pu_sound.play()

    def draw(self, window):
        window.blit(self.image, self.pygame_rect)
        #pygame.draw.rect(window, (255, 0, 255), self.pygame_rect, 1)
        

    def move(self, speed=1): # needs be 1,2,3,etc not 0,5 etc. You cant move object half pixsel
        self.pygame_rect.y += speed # Move to player position