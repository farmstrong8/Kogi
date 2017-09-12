# Sprite classes for platform game
import pygame as pg
import os
import random
from settings import *
#from spritesheet_functions import SpriteSheet
vec = pg.math.Vector2 




game_folder = os.path.dirname(__file__) #special variable where python keeps track of the file name itself
img_folder = os.path.join(game_folder, "img") #makes sure that the program works on any computer

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game #reference to game file for platforms
        self.image = pg.image.load(os.path.join(img_folder, "corgi.png"))
        self.image.set_colorkey(BLACK) #tells you wahat color you want to make transparent
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.steps = 0
        self.score = 0
        
        self.walking_frames_r = ['dog/walk_1.png',
                                 'dog/walk_2.png',
                                 'dog/walk_3.png',
                                 'dog/walk_4.png',
                                 'dog/walk_5.png',
                                 'dog/walk_6.png',
                                 'dog/walk_7.png',
                                 'dog/walk_8.png',
                                 'dog/walk_9.png',
                                 'dog/walk_10.png']
        
            
        
            

    def jump(self):
        #jump only if standing on platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        #accounts for acceleration in the y and x direction
        self.acc = vec(0, PLAYER_GRAV)
        
        #gets the keys pressed
        keys = pg.key.get_pressed()
             
        
        #if it is left...
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            frame = (self.steps // 10) % len(self.walking_frames_r)
            self.image = pg.image.load(self.walking_frames_r[frame])
            self.steps += 1
            #print(frame)
        
        #if it is right...
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            frame = (self.steps // 10) % len(self.walking_frames_r)
            self.image = pg.image.load(self.walking_frames_r[frame])
            self.steps += 1
            self.score += 1
            
        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc #adds more natural feel
        self.pos += self.vel + 0.5 * self.acc #adds more natural feel
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos #calculated position will always be the midbottom of the player
        
        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((32,32))
        self.image.fill(RED)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(WIDTH - self.rect.width)
        self.rect.x = random.randrange(-100,-40)
        self.speedx = random.randrange(5,12)
        self.step = 0 
        
        #animation
        self.chompFrames = ['chomp/chain1.png',
                            'chomp/chain2.png',
                            'chomp/chain3.png',
                            'chomp/chain4.png']
        
    def update(self):
        self.rect.x += self.speedx
        self.step += 1
        if self.rect.right > WIDTH + 10:
            self.rect.y = random.randrange(WIDTH - self.rect.width)
            self.rect.x = random.randrange(-100,-40)
            self.speedx = random.randrange(1,8)
            
        frame1 = (self.step // 20) % len(self.chompFrames)
        self.image = pg.image.load(self.chompFrames[frame1])
        

class Food(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "bone.png"))
        #self.image.fill(BLUE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        
        

 