import pygame
from pygame.locals import *
from random import randint

class Roccia:
    def __init__(self,screen, frames, tot = 20):
        self.screen = screen
        self.frames = frames
        self.tot = tot
        self.pos = (randint(100,1820), -100)
        self.rect = []
        self.collide_recta = pygame.rect.Rect((0,0), (80,280))
        for i in range(4):
            self.frames[i] = pygame.transform.scale(self.frames[i], (300,300))
            self.rect.append(self.frames[i].get_rect())
        for i in range(4):
            self.rect[i].center = self.pos
        self.collide_recta.center = self.pos


        self.lista = []
        self.j = 0
        self.velocity = 15
        

    def draw(self, j):
        for i in range(len(self.lista)):
            image = self.lista[i].frames[j]
            rect = self.lista[i].rect[j]
            self.screen.blit(image, rect)

    def move(self):
        for i in range(len(self.lista)):
            for j in range(4):
                self.lista[i].rect[j].y += self.velocity
            self.lista[i].collide_recta.y += self.velocity

    def newRock(self):
        if len(self.lista) <= self.tot:
            self.lista.append(Roccia(self.screen, self.frames, self.tot))
        elif 0 < self.lista[self.j].collide_recta.center[1] < 1200:
            return 0
        else:
            self.lista[self.j] = Roccia(self.screen, self.frames, self.tot)
            if self.j < self.tot:
                self.j += 1
            else:
                self.j = 0