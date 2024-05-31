import pygame, sys
from pygame.locals import *
from button import *
from ship import *
from random import randint
from roccia import *
from ufo import *
from space import *
from Animations import *
from projectile import *

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
        pRsPawn = 5500 # frequenza spawn asteroidi
        pUsPawn = 0 # frequenza spawn ufo
        punti = 0
        pRsFrame = 0
        pUsFrame = 0
        pShrink = 0
        which_frame_rock = 0
        which_frame_ufo = 0
        which_frame_proj = 0
        ufo_frequency = 6500
        rock_frequency = 10000
        font = pygame.font.Font("Fonts/Upheavtt.ttf", 30)
        start_animation = False
        drawShrink = False
        update_velocity = False
        draw_proj = False
        
        # SUONI
        Play_sound = pygame.mixer.Sound("Sounds/Play.mp3")
        audio_play = True #uso questa variabile per riprodurre la canzone una volta sola
        explosion_sound = pygame.mixer.Sound("Sounds/explosion.mp3")
        PowerUp_sound = pygame.mixer.Sound("Sounds/PowerUp.mp3")
        projectile_sound = pygame.mixer.Sound("Sounds/projectile.mp3")
        rock_sound = pygame.mixer.Sound("Sounds/rock.mp3")

        # Caricamentp immagini:
        resume_img = pygame.image.load("Images/layer3.png")
        resume_img = pygame.transform.scale(resume_img, (200,71))
       
        exit_img = pygame.image.load("Images/layer3.png")
        exit_img = pygame.transform.scale(exit_img, (200,71))
        
        ship_img = pygame.image.load("Images/navicella.png")
        ship_img = pygame.transform.scale(ship_img, (115,144))
        
        space_img = pygame.image.load("Images/space.png")
        
        exp_frames = []
        for i in range(10):
            exp_frames.append(pygame.image.load(f"Images/Explosion/frame{str(i)}.png"))
        
        shrink_img = pygame.image.load("Images/shrink.png")
        shrink_img = pygame.transform.scale(shrink_img, (50,50))
        
        asteroide_frames = []
        for i in range(80):
            asteroide_frames.append(pygame.image.load(f"Images/Fireball_Frames/frame_{str(i)}_delay-0.02s.png"))
            asteroide_frames[i] = pygame.transform.rotate(asteroide_frames[i], 90)
        
        projectil_frames = []
        for i in range(4):
            projectil_frames.append(pygame.image.load(f"Images/Projectile_Frames/frame{str(i)}.png"))
            projectil_frames[i] = pygame.transform.rotate(projectil_frames[i], (-135))
        
        ufo_frames = []
        for i in range(15):
            if i <= 9:
                ufo_frames.append(pygame.image.load(f"Images/Ufo_Frames/frame_0{str(i)}_delay-0.1s.png"))
                ufo_frames[i] = pygame.transform.scale(ufo_frames[i], (500, 500))
                #ufo_frames[i] = pygame.transform.rotate(ufo_frames[i], (-135))
            if i >= 10:
                ufo_frames.append(pygame.image.load(f"Images/Ufo_Frames/frame_{str(i)}_delay-0.1s.png"))
                ufo_frames[i] = pygame.transform.scale(ufo_frames[i], (500, 500))
                #ufo_frames[i] = pygame.transform.rotate(ufo_frames[i], (-135))
            
        # Creazione dei bottoni:
        resume_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2-60), resume_img)
        exit_btn = Button(self.screen, (self.window[0]/2, self.window[1]/2+80), exit_img)

        # Creazione oggetti
        navRect = Ship(self.screen, (self.window[0]/2, self.window[1]-200), (100,100), ship_img)
        rock = Roccia(self.screen, asteroide_frames, tot = 10)
        ufo = Ufo(self.screen, ufo_frames, tot = 1)
        spaceRect = Space(self.screen, (self.window[0], self.window[1]), space_img)
        spaceRect.new()
        pos = (randint(100,self.window[0]-100), -100)
        shrinkRect = Ship(self.screen, pos, (100,100), shrink_img)
        projectilRect = Projectil(self.screen, projectil_frames, (-1,-1))


        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_pause = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    draw_proj = True


                if event.type == QUIT:
                    Play_sound.stop()
                    fScore = open("Files/BestScore.txt", "w", encoding= "Utf-8")
                    fScore.writelines(str(punti))
                    fScore.close
                    pygame.quit()
                    sys.exit()
            
            spaceRect.draw()
            if game_pause == False:
                #riproduci canzone una volta
                if audio_play == True:
                    Play_sound.play()
                    Play_sound.set_volume(0.1)  
                audio_play = False   
                # prendo l'elenco dei tasti premuti
                keys = pygame.key.get_pressed()
                # movimenti della navicella (a/d)
                if keys[K_a] and navRect.rect.center[0] > 50:
                    navRect.move_left()
                if keys[K_d] and navRect.rect.center[0] < self.window[0]-50:
                    navRect.move_right()
                
                # movimento roccia
                rock.move()
                # movimento ufo
                ufo.move()
                # movimento spazio
                spaceRect.move()

                # aggiunta rocce
                if pRsPawn >= randint(1000, rock_frequency):
                    rock.newRock()
                    rock_sound.play()
                    rock_sound.set_volume(0.1)
                    pRsPawn = 0
                    
                # aggiunta ufo
                if pUsPawn >= randint(000, ufo_frequency):
                    ufo.newUfo()
                    pUsPawn = 0
                    
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
                        shrinkRect = Ship(self.screen, pos, (100,100), shrink_img)
                    shrinkRect.draw()

                # collisione shrink
                if shrinkRect.rect.colliderect(navRect.collide_recta):
                    drawShrink = False
                    PowerUp_sound.play()
                    PowerUp_sound.set_volume(0.4)
                    pos = (randint(100,self.window[0]-100), -100)
                    shrinkRect = Ship(self.screen, pos, (100,100), shrink_img)
                    navRect.shrink(navRect.rect.center)


                # sparare i colpi
                if draw_proj == True and projectilRect.collide_recta.y < 0:
                    projectilRect = Projectil(self.screen, projectil_frames, (navRect.rect.center[0], navRect.rect.center[1]-50))
                if draw_proj == True:
                    projectile_sound.play()
                    projectile_sound.set_volume(0.5) 
                    projectilRect.move()
                    

            if draw_proj == True:
                projectilRect.draw(which_frame_proj)
            navRect.draw()
            rock.draw(which_frame_rock)
            ufo.draw(which_frame_ufo)
            
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

                text = font.render(f"Esci", 1, self.colori[1])
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
                    Play_sound.stop()
                    explosion_sound.play()
                    explosion_sound.set_volume(0.5)
                    pos = (((rock.lista[i].collide_recta.x + 100) + navRect.collide_recta.x)/2  ,  ((rock.lista[i].collide_recta.y + 200) + navRect.collide_recta.y)/2)
                    exp_an = Animation(self.screen, exp_frames, pos)
                    start_animation = True
            if start_animation == True:
                exp_an.play()
                return punti
            
            # collisione ufo astronave
            for i in range(len(ufo.lista)):
                if ufo.lista[i].collide_recta.colliderect(navRect.collide_recta):
                    # animazione esplosione
                    Play_sound.stop()
                    explosion_sound.play()
                    explosion_sound.set_volume(0.5)
                    pos = (((ufo.lista[i].collide_recta.x + 100) + navRect.collide_recta.x)/2  ,  ((ufo.lista[i].collide_recta.y + 200) + navRect.collide_recta.y)/2)
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

            if projectilRect.out() == True:
                draw_proj = False
            # rocce
            if which_frame_rock == 79:
                which_frame_rock = 0
            else:
                which_frame_rock += 1
            # proiettile
            if which_frame_proj == 3:
                which_frame_proj = 0
            else:
                which_frame_proj += 1
            # ufo    
            if which_frame_ufo == 14:
                which_frame_ufo = 0
            else:
                which_frame_ufo += 1


            pRsPawn += self.fps
            pUsPawn += self.fps
            pPunt += self.fps
            pRsFrame += self.fps
            pUsFrame += self.fps
            pygame.display.flip()
            if update_velocity == True:
                pygame.time.wait(1100)
                update_velocity = False
            self.clock.tick(self.fps)