import pygame
from pygame.locals import *

class Image:
    def __init__(self, screen, pos, size, image):
        self.screen = screen
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.collide_recta = pygame.Rect((0,0),(80,90))
        self.collide_recta.center = self.pos
        self.velocity = 15

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def move(self):
        # spostamento normale
        self.rect.y += 10

    def move_right(self):
        self.rect.x += self.velocity
        self.collide_recta.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity
        self.collide_recta.x -= self.velocity

    def move_down(self):
        self.rect.y += 100

    def shrink(self, pos):
        self.image = pygame.transform.scale(self.image, (74,94))
        self.velocity = 30
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.collide_recta = pygame.Rect((0,0),(40,80))
        self.collide_recta.center = pos
    
    def unShrink(self, pos):
        self.image = pygame.transform.scale(self.image, (115,144))
        self.velocity = 15
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.collide_recta = pygame.Rect((0,0),(90,100))
        self.collide_recta.center = pos