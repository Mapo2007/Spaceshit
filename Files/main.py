import pygame, sys
from random import randint
from pygame.locals import *
from rettangolo import *
from ship import *
from button import *
from run import *    

pygame.init()

# Window Settings
window_widht = 1920
window_height = 1080
window_size = (window_widht, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Spaceshit")

with open("Files/BestScore.txt", "r", encoding= "Utf-8") as fScore:
    best = int(fScore.readline())

clock = pygame.time.Clock()
fps = 60


# Colori:
RED = (225,0,0)
WHITE = (225,225,225)
GREEN = (0,153,0)
CYANO = (204,227,225)

colori = [RED, WHITE, GREEN, CYANO]

font = pygame.font.Font("Fonts/Upheavtt.ttf", 55)

# Finestra Base:
screen.fill(WHITE)
start_img = pygame.image.load("Images/PlayBtn.png")
start_img = pygame.transform.scale(start_img, (295,130))
exit_img = pygame.image.load("Images/ExitBtn.png")
exit_img = pygame.transform.scale(exit_img, (295,130))
ship_img = pygame.image.load("Images/navicella.png")
space_img = pygame.image.load("Images/space.png")
start_btn = Button(screen, (window_widht/2, window_height/2-80), start_img)
exit_btn = Button(screen, (window_widht/2, window_height/2+100), exit_img)
spaceRect = Space(screen, (window_widht, window_height), space_img)
spaceRect.new()

pygame.display.set_icon(ship_img)

# ---------------------------- MAIN ----------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()  


    # animazione tasto play 
    pos1 = pygame.mouse.get_pos()
    if start_btn.rect.collidepoint(pos1):
        start_img = pygame.image.load("Images/PlayClick.png")
        start_img = pygame.transform.scale(start_img, (295,130))
        start_btn = Button(screen, (window_widht/2, window_height/2-80), start_img)
    else:
        start_img = pygame.image.load("Images/PlayBtn.png")
        start_img = pygame.transform.scale(start_img, (295,130))
        start_btn = Button(screen, (window_widht/2, window_height/2-80), start_img)

    # animazione tasto exit 
    pos2 = pygame.mouse.get_pos()
    if exit_btn.rect.collidepoint(pos2):
        exit_img = pygame.image.load("Images/ExitClick.png")
        exit_img = pygame.transform.scale(exit_img, (295,130))
        exit_btn = Button(screen, (window_widht/2, window_height/2+100), exit_img)
    else:
        exit_img = pygame.image.load("Images/ExitBtn.png")
        exit_img = pygame.transform.scale(exit_img, (295,130))
        exit_btn = Button(screen, (window_widht/2, window_height/2+100), exit_img)
        
         
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if exit_btn.rect.collidepoint(pos):
                fScore = open("Files/BestScore.txt", "w", encoding= "Utf-8")
                fScore.writelines(str(best))
                fScore.close
                event.type = QUIT

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if start_btn.rect.collidepoint(pos):
                start = run(screen, colori, clock, (window_widht, window_height))
                punti = start.start(best)
                if punti > best:
                    best = punti

    spaceRect.draw()

    text = font.render(f"Best Score: {best}", 1, WHITE)
    screen.blit(text, (window_widht/2-195, window_height-150))
    
    start_btn.draw()
    exit_btn.draw()
    
    pygame.display.flip()
    clock.tick(fps)