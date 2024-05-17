import pygame, sys
from pygame.locals import *
from button import *
from image import *
from random import randint
from roccia import *
from space import *
from Animations import *

class run:
    def __init__(self, screen, colori, clock, window):
        self.screen = screen
        self.colori = colori
        self.clock = clock
        self.window = window
        self.fps = 60
    

    def start(self, best):
        # Variabili di gioco
        game_pause = False
        pPunt = 0
        pRsPawn = 5500
        punti = 0
        pShrink = 0
        which_frame_rock = 0
        rock_frequency = 10000
        font = pygame.font.Font("Fonts/Upheavtt.ttf", 30)
        start_animation = False
        drawShrink = False
        update_velocity = False
        
        # Caricamentp immagini:
        resume_img = pygame.image.load("Images/layer3.png")
        resume_img = pygame.transform.scale(resume_img, (200,71))
        exit_img = pygame.image.load("Images/layer3.png")
        exit_img = pygame.transform.scale(exit_img, (200,71))
        ship_img = pygame.image.load("Images/navicella.png")
        ship_img = pygame.transform.scale(ship_img, (115,144))
        rock_img = pygame.image.load("Images/asteroide.png")
        space_img = pygame.image.load("Images/space.png")
        exp_frames = []
        for i in range(10):
            exp_frames.append(pygame.image.load(f"Images/Explosion/frame{str(i)}.png"))
        shrink_img = pygame.image.load("Images/shrink.png")
        shrink_img = pygame.transform.scale(shrink_img, (50,50))
        asteroide_frames = []
        for i in range(4):
            asteroide_frames.append(pygame.image.load(f"Images/Asteroid_Frames/frame{str(i)}.png"))
            asteroide_frames[i] = pygame.transform.rotate(asteroide_frames[i], 45)
        
            

        
        # Creazione dei bottoni:
        resume_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2-60), resume_img)
        exit_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2+80), exit_img)

        # Creazione oggetti
        navRect = Image(self.screen, (self.window[0]/2, self.window[1]-200), (100,100), ship_img)
        rock = Roccia(self.screen, asteroide_frames, tot = 10)
        spaceRect = Space(self.screen, (self.window[0], self.window[1]), space_img)
        spaceRect.new()
        pos = (randint(100,self.window[0]-100), -100)
        shrinkRect = Image(self.screen, pos, (100,100), shrink_img)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_pause = True
                if event.type == QUIT:
                    fScore = open("Files/BestScore.txt", "w", encoding= "Utf-8")
                    fScore.writelines(str(punti))
                    fScore.close
                    pygame.quit()
                    sys.exit()
            
            spaceRect.draw()

            if game_pause == False:    
                # prendo l'elenco dei tasti premuti
                keys = pygame.key.get_pressed()
                # movimenti della navicella (a/d)
                if keys[K_a] and navRect.rect.center[0] > 50:
                    navRect.move_left()
                if keys[K_d] and navRect.rect.center[0] < self.window[0]-50:
                    navRect.move_right()
                
                # movimento roccia
                rock.move()
                # movimento spazio
                spaceRect.move()

                # aggiunta rocce
                if pRsPawn >= randint(1000, rock_frequency):
                    rock.newRock()
                    pRsPawn = 0

                # velocità delle rocce a score = 25
                if punti == 25 and pPunt >= 1500:
                    rock.velocity += 10
                    rock.tot += 20
                    rock_frequency = 2000
                    update_velocity = True

                # aggiunta punti
                if pPunt >= 1500:
                    punti += 1
                    pPunt = 0
                

                # powerup: shrink
                if punti%30 == 0 and punti > 0:
                    drawShrink = True
                if drawShrink == True:
                    shrinkRect.move()
                    if (shrinkRect.rect.y / 1080) > 1:
                        drawShrink = False
                        pos = (randint(100,self.window[0]-100), -100)
                        shrinkRect = Image(self.screen, pos, (100,100), shrink_img)
                    shrinkRect.draw()

                # collisione shrink
                if shrinkRect.rect.colliderect(navRect.collide_recta):
                    drawShrink = False
                    pos = (randint(100,self.window[0]-100), -100)
                    shrinkRect = Image(self.screen, pos, (100,100), shrink_img)
                    navRect.shrink(navRect.rect.center)

            navRect.draw()
            rock.draw(which_frame_rock)
            
            # punti
            if punti <= best:
                text = font.render(f"Score:", 1, self.colori[1])
                text2 = font.render(f"{punti}", 1, self.colori[1])
            else:
                text = font.render(f"Score:", 1, self.colori[1])
                text2 = font.render(f"{punti}", 1, self.colori[2])
            self.screen.blit(text, (50, 50))
            self.screen.blit(text2, (190, 50))

            # menu di pausa
            if game_pause == True: 

                # animazione tasto play 
                pos1 = pygame.mouse.get_pos()
                if resume_btn.rect.collidepoint(pos1):
                    resume_img = pygame.image.load("Images/layer4.png")
                    resume_img = pygame.transform.scale(resume_img, (200,71))
                    resume_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2-80), resume_img)
                else:
                    resume_img = pygame.image.load("Images/layer3.png")
                    resume_img = pygame.transform.scale(resume_img, (200,71))
                    resume_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2-80), resume_img)

                # animazione tasto exit 
                pos2 = pygame.mouse.get_pos()
                if exit_btn.rect.collidepoint(pos2):
                    exit_img = pygame.image.load("Images/layer4.png")
                    exit_img = pygame.transform.scale(exit_img, (200,71))
                    exit_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2+80), exit_img)
                else:
                    exit_img = pygame.image.load("Images/layer3.png")
                    exit_img = pygame.transform.scale(exit_img, (200,71))
                    exit_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2+80), exit_img)

                resume_btn.draw()
                exit_btn.draw()

                text = font.render(f"Continua", 1, self.colori[1])
                self.screen.blit(text, (self.window[0]/2-68, self.window[1]/2-100))

                text = font.render(f"Menù", 1, self.colori[1])
                self.screen.blit(text, (self.window[0]/2-35, self.window[1]/2+60))

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if resume_btn.rect.collidepoint(pos):
                        game_pause = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if exit_btn.rect.collidepoint(pos):
                        return punti
            
            
            # collisione roccia astronave
            for i in range(len(rock.lista)):
                if rock.lista[i].collide_recta.colliderect(navRect.collide_recta):
                    # animazione esplosione
                    pos = (((rock.lista[i].collide_recta.x + 150) + navRect.collide_recta.x)/2  ,  ((rock.lista[i].collide_recta.y + 200) + navRect.collide_recta.y)/2)
                    exp_an = Animation(self.screen, exp_frames, pos)
                    start_animation = True
            if start_animation == True:
                exp_an.play()
                return punti
            
            if pShrink >= 10000:
                navRect.unShrink(navRect.rect.center)
                pShrink = 0

            
            if update_velocity == True:
                text = font.render(f"Velocità aumentata", 1, (70,240,100))
                self.screen.blit(text, (self.window[0]/2-150, self.window[1]/2-50))
            if navRect.velocity == 30:
                pShrink += self.fps
            if which_frame_rock == 3:
                which_frame_rock = 0
            else:
                which_frame_rock += 1
            pRsPawn += self.fps
            pPunt += self.fps
            pygame.display.flip()
            if update_velocity == True:
                pygame.time.wait(1100)
                update_velocity = False
            self.clock.tick(self.fps)