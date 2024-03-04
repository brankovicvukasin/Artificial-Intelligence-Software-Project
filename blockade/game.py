import pygame
from .tabla import *
from .constants import *
from .zid import *
from queue import PriorityQueue
import math



class Game:
    def __init__(self, win):
        self.tabla = Tabla()   #init je inicialising the game
        self.win = win
        self.selected = 0  #vrednost nula ako igrac nije selektovan i vrednost Igrac ako jeste
        self.turn = RED
        self.zid = 0  #kada je nula igrac ne moze da postavlja zid, ocekuje se da se pomeri pesak
        self.zeleni = RED
        self.plavi = RED
        self.valid_moves = [] #lista u kojoj se nalaze svi moguci potezi koje igrac moze da odigra
        self.nema_zidova_plavi = 0 #ako AI ostane bez zidova
        

    def ai_potez(self, tabla):
        self.tabla = tabla[0]
        self.update()
        
        

    def ai_potez_zid(self, tabla):
        self.tabla = tabla
        self.promeni_potez()
        self.update()
        
        
       
    def update(self):
        self.tabla.draw_squares(self.win) #crta kockice
        self.tabla.nacrtaj_pocetne_poz(self.win) #crta pocetne pozicije 
        self.tabla.draw(self.win) #crta igrace i zidove
        self.tabla.stanje_sa_zidovima(self.win) #ispisuje koliko je ostalo zidova igracima
        self.draw_valid_moves(self.valid_moves) #crta validne poteze koje covek moze da odigra
        self.proveri_pobednika()#proverava da li je doslo do pobede

        pygame.display.update()    #izvrsava iscrtavanje na ekranu


    def simuliraj_potez_game(self, zeleni_zid, tabla, boja):

        if boja == GREEN:
            tabla.dodaj_zeleni_zid(zeleni_zid) 

        elif boja == BLUE:
            tabla.dodaj_plavi_zid(zeleni_zid)
            
        return tabla 


    def proveri_da_li_zid_zatvara(self, vrsta, kolona, boja): #sprecava coveka da postavi zid tamo gde zatvara put do odredista
        privremena_tabla = deepcopy(self.tabla) #deepcopy, bilo koje promene se ne reflektuju na trenutnu tablu
        nova_tabla = self.simuliraj_potez_game((kolona, vrsta), privremena_tabla, boja) 
        return self.tabla.pronadji_put(nova_tabla)

        

    def proveri_da_li_ima_slobodnih_zidova(self):
        if self.turn == RED and self.tabla.igracOksZeleni  == 0 and self.tabla.igracOksPlavi == 0:
             self.zid = 0 #ukoliko plavi igrac nema vise zidova 
        elif self.turn == BLUE and self.tabla.igracIksZeleni  == 0 and self.tabla.igracIksPlavi == 0:
             self.zid = 0 #mora i ovo da postavi jer ako ne plavi igrac nece moci selektovati igraca kad ostane bez zidova
             self.nema_zidova_plavi = 1 #kad crveni ostane bez zidova

    def select2(self, vrsta, kolona): #za postavljanje zelenih zidova, ispitivanje da li je moguce

      if self.proveri_da_li_zid_zatvara(vrsta, kolona, GREEN) == False:
          print('Nevalidan potez')
          return True

      if self.tabla.zidHorizontalni[kolona][vrsta] != 0 and self.tabla.zidHorizontalni[kolona][vrsta+1] != 0:
          return True
      
      if self.turn == RED and self.zid == 1 and self.tabla.igracOksZeleni > 0: #plavi kad odigra turn postaje RED
            if self.tabla.zidVertikalni[kolona+1][vrsta] == 0 and self.tabla.zidVertikalni[kolona][vrsta] == 0:    

               self.tabla.zidVertikalni[kolona][vrsta] = Zid(vrsta, kolona, GREEN, self.tabla.polje_height, self.tabla.polje_width)
               self.tabla.zidVertikalni[kolona+1][vrsta] = Zid(vrsta, kolona+1, GREEN, self.tabla.polje_height, self.tabla.polje_width)
               self.tabla.igracOksZeleni-=1
               self.zid = 0
               self.promeni_potez()


      if self.turn == BLUE and self.zid == 1 and self.tabla.igracIksZeleni > 0 and kolona+1 < self.tabla.kolona:
            if self.tabla.zidVertikalni[kolona+1][vrsta] == 0 and self.tabla.zidVertikalni[kolona][vrsta] == 0:   

               self.tabla.zidVertikalni[kolona][vrsta] = Zid(vrsta, kolona, GREEN, self.tabla.polje_height, self.tabla.polje_width)
               self.tabla.zidVertikalni[kolona+1][vrsta] = Zid(vrsta, kolona+1, GREEN, self.tabla.polje_height, self.tabla.polje_width)
               self.tabla.igracIksZeleni-=1
               self.zid = 0
               self.promeni_potez()

      self.update()
 
     
    def select3(self, vrsta, kolona): #metoda za postavljanje plavih zidova, poziva se klikom misa

      if vrsta == self.tabla.vrsta-1:
         return True

      if self.proveri_da_li_zid_zatvara(vrsta, kolona, BLUE) == False:
          print('Nevalidan potez')
          return True

      if self.tabla.zidVertikalni[kolona][vrsta] != 0 and self.tabla.zidVertikalni[kolona+1][vrsta] != 0:
          return True

      if self.turn == RED and self.zid == 1 and self.tabla.igracOksPlavi > 0:

          if self.tabla.zidHorizontalni[kolona][vrsta] == 0 and self.tabla.zidHorizontalni[kolona][vrsta+1] == 0:

                self.tabla.zidHorizontalni[kolona][vrsta] = Zid(vrsta-1, kolona+1, BLUE2, self.tabla.polje_height, self.tabla.polje_width)
                self.tabla.zidHorizontalni[kolona][vrsta+1] = Zid(vrsta, kolona+1, BLUE2,self.tabla.polje_height, self.tabla.polje_width)
                self.tabla.igracOksPlavi-=1
                self.zid = 0
                self.promeni_potez()

      elif self.turn == BLUE and self.zid == 1 and self.tabla.igracIksPlavi > 0 and vrsta+1 < self.tabla.vrsta:

          if self.tabla.zidHorizontalni[kolona][vrsta] == 0 and self.tabla.zidHorizontalni[kolona][vrsta+1] == 0:

                self.tabla.zidHorizontalni[kolona][vrsta] = Zid(vrsta-1, kolona+1, BLUE2, self.tabla.polje_height, self.tabla.polje_width)
                self.tabla.zidHorizontalni[kolona][vrsta+1] = Zid(vrsta, kolona+1, BLUE2,self.tabla.polje_height, self.tabla.polje_width)
                self.tabla.igracIksPlavi-=1
                self.zid = 0
                self.promeni_potez()
      self.update()    

    def select(self, vrsta, kolona):    

        self.proveri_da_li_ima_slobodnih_zidova()

        if self.selected == 0 and self.zid == 0: #ako igrac nije selektovan i ako je zid postavljen
            igrac = self.tabla.vrati_igraca(vrsta, kolona)
            if igrac != 0 and igrac.boja == self.turn:
               self.selected = igrac
               self.valid_moves = self.tabla.get_valid_moves(igrac)
            
        elif self.zid == 0:
                for move in self.valid_moves:
                  vrst, kol = move   

                  if vrst == vrsta and kol == kolona: 
                      self.tabla.move(self.selected, vrst, kol)                     
                      self.selected = 0
                      self.valid_moves.clear()

                      if self.nema_zidova_plavi == 1:
                            self.promeni_potez()
                      self.zid = 1

    def draw_valid_moves(self, moves):
       for move in moves:
           vrsta, kolona = move
           pygame.draw.circle(self.win, WHITE, (self.tabla.polje_height * vrsta + 2/10 * height + self.tabla.polje_height // 2, self.tabla.polje_width * kolona + 1/10* width + self.tabla.polje_width // 2), 15)
 
#    def move(self, vrsta, kolona): #za pomeranje
#        igrac = self.tabla.vrati_igraca(vrsta, kolona)
#        if self.selected and igrac == 0 and (vrsta, kolona) in self.valid_moves:
#            self.tabla.move(self.selected, vrsta, kolona)
#            self.promeni_potez()
#        else:
#            return False
#
#        return True    

    def promeni_potez(self):  
        if self.turn == RED:

           self.turn = BLUE
        else:

            self.turn = RED    

        self.nema_zidova_plavi = 0 

    def proglasi_pobednika(self, boja):
        
        pygame.draw.rect(self.win, boja, (0,0, 1000, 1000 ))
        if boja == RED:
          pygame.draw.rect(self.win, boja, (0,0, 1000, 1000 ))
          pozicije = FONT1.render('CESTITAMO NA POBEDI, POBEDNIK JE CRVENI IGRAC', 100, WHITE)
          WIN.blit(pozicije,(300,500)) 
          self.tabla.pobednik = RED
        else:
          pygame.draw.rect(self.win, boja, (0,0, 1000, 1000 ))
          pozicije = FONT1.render('CESTITAMO NA POBEDI, POBEDNIK JE PLAVI IGRAC', 100, WHITE)
          WIN.blit(pozicije,(300,500)) 
          self.tabla.pobednik = BLUE

    def proveri_pobednika(self):
        igrac1 = self.tabla.vrati_igraca(self.tabla.pocetni1.vrsta, self.tabla.pocetni1.kolona)
        igrac2 = self.tabla.vrati_igraca(self.tabla.pocetni2.vrsta, self.tabla.pocetni2.kolona)
        igrac3 = self.tabla.vrati_igraca(self.tabla.pocetni3.vrsta, self.tabla.pocetni3.kolona)
        igrac4 = self.tabla.vrati_igraca(self.tabla.pocetni4.vrsta, self.tabla.pocetni4.kolona)

        if  igrac1 != 0 and igrac1.boja == BLUE:
            self.proglasi_pobednika(igrac1.boja)
        elif igrac2 !=0 and igrac2.boja == BLUE:
            self.proglasi_pobednika(igrac2.boja)
        elif igrac3 !=0 and igrac3.boja == RED:
            self.proglasi_pobednika(igrac3.boja)
        elif igrac4 !=0 and igrac4.boja == RED:
            self.proglasi_pobednika(igrac4.boja)

