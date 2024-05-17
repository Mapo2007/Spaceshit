import pygame
from pygame.locals import *

class Button:
    def __init__(self, screen, pos, image):
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self):
        self.screen.blit(self.image, self.rect)