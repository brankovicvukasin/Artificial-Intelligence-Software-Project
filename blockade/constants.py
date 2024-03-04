import pygame
import os

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BLUE2 = (0,191,255)
GREY = (128,128,128)
GREEN = (0,255,0)
ORANGE = (255,140,0)
GOLD = (255,215,0)

width, height = 1000, 1000

WIN = pygame.display.set_mode((width, height))
FONT1 = pygame.font.SysFont('comicsans', 20)
FONT2 = pygame.font.SysFont('comicsans', 15)
FPS=60
