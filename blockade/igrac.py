import pygame
from .constants import *

class Igrac:


    def __init__(self, vrsta, kolona, boja, polje_height, polje_width):
        self.vrsta = vrsta - 1 
        self.kolona = kolona - 1
        self.boja = boja
        self.polje_height = polje_height
        self.polje_width = polje_width
        self.padding = self.polje_height/9

        self.x = 0
        self.y = 0
        self.calc_pos()


    def calc_pos(self):                                             #poluprecnik kurga
        self.x = self.polje_height * self.vrsta + 2/10 * height + self.polje_height // 2 #duplo deljenje, vraca ceo broj bez ostatka
        self.y = self.polje_width * self.kolona + 1/10* width + self.polje_width // 2


    def draw(self, win):  
        radius = self.polje_height//2 - self.padding
        pygame.draw.circle(win, self.boja, (self.x, self.y), radius)
       


    def pomeri(self, vrsta, kolona):   
        self.vrsta = vrsta
        self.kolona = kolona
        self.calc_pos()

    def move(self, vrsta, kolona):
        self.vrsta = vrsta
        self.kolona = kolona
        self.calc_pos()
    
    def __repr__(self):
        return str((self.kolona, self.vrsta))