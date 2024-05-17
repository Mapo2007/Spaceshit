import pygame
from pygame.locals import *

class Space:
    def __init__(self, screen, pos, image):
        self.screen = screen
        self.pos = pos
        self.image = pygame.Surface(self.pos)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0]/2,pos[1]/2)
        self.lista = []
        
    def draw(self):
        for i in range(len(self.lista)):
            image = self.lista[i].image
            rect = self.lista[i].rect
            self.screen.blit(image, rect)
            
    def move(self):
        for i in range(0,len(self.lista)):
            if i == 0 and self.lista[i+1].rect.center[1] ==  self.pos[1]/2:
                self.lista[i].rect.y = -self.pos[1]
            elif i == 1 and self.lista[i-1].rect.center[1] ==  self.pos[1]/2:
                self.lista[i].rect.y =  -self.pos[1]
            else:
                self.lista[i].rect.y += 3
                
    def new(self):
        self.lista.append(Space(self.screen,(self.pos[0],self.pos[1]), self.image))
        self.lista.append(Space(self.screen, (self.pos[0],self.pos[1]), self.image))