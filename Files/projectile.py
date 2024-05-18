import pygame
from pygame.locals import *

class Projectil:
    def __init__(self, screen, frames, pos):
        self.screen = screen
        self.frames = frames
        self.pos = pos
        self.rect = []
        self.collide_recta = pygame.rect.Rect((0,0), (50,50))
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (70,70))
            self.rect.append(self.frames[i].get_rect())
        for i in range(len(self.frames)):
            self.rect[i].center = self.pos
        self.collide_recta.center = self.pos
        self.velocity = 35

    def draw(self, j):
        image = self.frames[j]
        rect = self.rect[j]
        self.screen.blit(image, rect)

    def move(self):
        for i in range(len(self.frames)):
            self.rect[i].y -= self.velocity
        self.collide_recta.y -= self.velocity

    def out(self):
        if self.collide_recta.y < 0: 
            return True