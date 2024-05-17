import pygame
from pygame.locals import *

class Animation:
        def __init__(self,screen,frames,pos):
            self.screen = screen
            self.frames = frames
            self.pos = pos
            
        def play(self):
            for frame in self.frames:
                frame = pygame.transform.scale(frame, (100,100))
                rect = frame.get_rect()
                rect.center = self.pos
                self.screen.blit(frame, rect)
                pygame.display.flip()
                pygame.event.wait(100)