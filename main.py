# -*- coding: utf-8 -*-
import pygame as pg
import random
from settings import *
from sprites import *



class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()

        #makes the screen with given width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.background = pg.image.load(os.path.join(img_folder, "background.jpg")).convert()
        self.background1 = pg.image.load(os.path.join(img_folder, "background.gif")).convert()
        self.background2 = pg.image.load(os.path.join(img_folder, "goscreen1.jpg")).convert()

        #Displays the title "Oni Inu"
        pg.display.set_caption(TITLE)

        #game clock
        self.clock = pg.time.Clock()

        #assures that it is runninga
        self.running = True

        #font
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game


        #score
        self.score = 0

        #holds all of the sprites
        self.all_sprites = pg.sprite.Group()

        #holds all of the platforms
        self.platforms = pg.sprite.Group()

        #initializes player
        self.player = Player(self)
        self.all_sprites.add(self.player)


        #mob group
        self.mobs = pg.sprite.Group()

        #Food
        self.food = pg.sprite.Group()
        f = Food(random.randrange(5000,7000), random.randrange(HEIGHT-50))
        self.all_sprites.add(f)
        self.food.add(f)
#
        #initializes mob
#        for i in range(MOB_DIFFICULTY):
#            m = Mob()
#            self.all_sprites.add(m)
#            self.mobs.add(m)

        #initializes platforms
        for plat in PLATFORM_LIST:
            p = Platform(*plat) # * means explode in python and so it pretty much reduces it by 1 dimension
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()


        #check if player hits platform, only when falling
        if self.player.vel.y > 0:
            hits1 = pg.sprite.spritecollide(self.player, self.platforms, False)
            hits2 = pg.sprite.spritecollide(self.player, self.mobs, False)
            #hits3 = pg.sprite.spritecollide(f, self.platforms, False)
            hits4 = pg.sprite.spritecollide(self.player, self.food, False)
            if hits1:
                self.player.pos.y = hits1[0].rect.top #sets the bottom of the play to the top of the platform
                self.player.vel.y = 0 #makes sure that there is no acceleration in the y direction

            if hits2:
                self.playing = False

#            if hits3:
#                f.pos.y = hits3[0].rect.top

            if hits4:
                self.show_cg_screen()
                self.playing = False
                #self.playing = False
                #self.running = False


        #if player reaches right 1/4 of screen
        if self.player.rect.right >= 3* WIDTH /4:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
                if plat.rect.right <= 0:
                    plat.kill()
            for mob in self.mobs:
                mob.rect.x -= abs(self.player.vel.x)
            for food in self.food:
                food.rect.x -= abs(self.player.vel.x)

        #spawn new platforms to keep same average number
        while len(self.platforms) < 7:
            width = random.randrange (1,50)
            p = Platform(random.randrange(WIDTH, WIDTH + width),
                         random.randrange(HEIGHT-50),
                          50+width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

        #Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            self.playing = False


        #score update based on chain comps dodged
        for mob in self.mobs:
            if self.player.rect.right < mob.rect.left:
                self.score += 0

        #score update based on position or steps taken
        counter = (self.player.steps // 10) % len(self.player.walking_frames_r)
        self.score += counter


        difficulty = ((self.player.steps // 70) + 1)

        #change the difficulty
        if difficulty % 10 == 0:
            self.player.steps = 0
            for i in range(random.randrange(1,4)):
                m = Mob()
                self.all_sprites.add(m)
                self.mobs.add(m)
            return
                #print("how many mobs:" + str(len(self.mobs)))



    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    if(len(self.food) == 1):
                        for food in self.food:
                            food.kill()
    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        #adds the background
        self.screen.blit(self.background, (self.player.vel.x,0))
        #adds the sprites to the screen
        self.all_sprites.draw(self.screen)

        #draw the score
        self.draw_text(str(self.player.score), 22, WHITE, 50, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(WHITE)
        self.screen.blit(self.background1, (0,0))
        self.draw_text(TITLE, 44, BGCOLOR, WIDTH / 2, HEIGHT - 470)
        self.draw_text("Press arrows to move, space to jump", 22, BGCOLOR, WIDTH / 2, HEIGHT - 40)
        self.draw_text("Press Ax2 for arcade, S for story mode", 16, BGCOLOR, WIDTH / 2, HEIGHT - 420)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background2, (0,0))
        self.draw_text("GAME OVER", 37, WHITE, 230, HEIGHT - 465)
        self.draw_text("Score: " + str(self.score), 22, WHITE, 230, HEIGHT - 420)
        self.draw_text("Press Ax2 for arcade, S for story mode", 21, WHITE, 240, HEIGHT - 390)
        pg.display.flip()
        self.wait_for_key()

    def show_cg_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("Congratulations, you won!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any button to quit.", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    def wait_for_quit(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    self.running = False
        # KEYUP means any key press will start game,
        # to change it to press A for arcade, replace keyup with K_A
        # for S for story, replayce KEYUP with K_S
        # this might be tricky to get two separate modes based on what this guy did.

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        #rectangle to hold it on the screen
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
