# game options/settings
TITLE = "Kogi"
WIDTH = 800
HEIGHT = 480
FPS = 60
FONT_NAME = 'arial'


# Player properties
PLAYER_ACC = 0.6
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 45
MOB_DIFFICULTY = 1

#Starting platforms
PLATFORM_LIST = [(0,HEIGHT-40,200,40), #big platform
                 (WIDTH/2 - 50, HEIGHT* 3 / 4, 100, 20),
                 (WIDTH/2 + 200, (HEIGHT*3 / 4) + 10, 100, 20),
                 (WIDTH/2 + 400, (HEIGHT*3 / 4) - 20,100,20),
                 (WIDTH/2 + 600, (HEIGHT*3 / 4) -5,100,20),
                 (WIDTH/2, HEIGHT/2, 100,20)
                 ]


# define colors
DARK = (89, 89, 89)
GRAY = (225, 234, 234)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BGCOLOR = (0, 66, 124)