import pygame
from .constants import *

class Zid:

    def __init__(self, vrsta, kolona, boja, polje_height, polje_width):
        self.vrsta = vrsta +1
        self.kolona = kolona 
        self.boja = boja
        self.polje_height = polje_height
        self.polje_width = polje_width

        self.x = 0
        self.y = 0
        self.calc_pos()


    def calc_pos(self):
        self.x = self.polje_height * self.vrsta + 2/10 * height
        self.y = self.polje_width * self.kolona + 1/10* width


    def drawVertikalni(self, win):  
        pygame.draw.line(win, self.boja, (self.x, self.y), (self.x , self.y + self.polje_width), width=5)

    def drawHorizontalni(self, win):  
        pygame.draw.line(win, self.boja, (self.x, self.y), (self.x + self.polje_height, self.y ), width=5)

    def pomeri(self, vrsta, kolona):   
        self.vrsta = vrsta
        self.kolona = kolona
        self.calc_pos()
        
    def __repr__(self):
        return str(self.boja)    