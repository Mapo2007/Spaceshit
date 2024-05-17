
import pygame
from pygame.locals import *

class Miorettangolo:
    def __init__(self, screen, pos, size) -> None:
        self.screen = screen
        self.colore1 = (100,100,100)
        self.colore2 = (255,255,255)
        self.colore = self.colore1
        self.image = pygame.Surface(size)
        # self.image.fill(self.colore) # posso già riempirlo di colore
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.rect.center = pos
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos

    def draw(self):
        self.image.fill(self.colore)
        self.screen.blit(self.image, self.rect)

    def toggle_color(self):
        if self.colore == self.colore1:
            self.colore = self.colore2
        else:
            self.colore = self.colore1
        self.draw()
    
    def set_color(self, colore):
            self.colore = colore

    def set_color_1(self):
        self.colore = self.colore1
    def set_color_2(self):
        self.colore = self.colore2