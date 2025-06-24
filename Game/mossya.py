import pygame
import random
class Mossya:
    def __init__(self, name, age): #  __init__ function is called automatically every time the class is being used to create a new object.
        self.health = 100
        self.position = (0, 0)
        self.image
        self.enemy.hurted_image
        self.spawn_radius = (30, 900-30, 10, 500-400)
        self.pygame.rect = pygame.Rect(0, 0, 25, 25)

    def take_damage(self, amount): # Mossya.take_damage(10)
        self.health -= amount
        print("Current health:", self.health)
    
    def move(self, speed=1):
        self.rect.y += speed
        