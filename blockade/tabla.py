import pygame
from .constants import *
from .igrac import *
from .zid import *
from minimax.algorithm import * 
import queue


class Tabla:
    
    def __init__(self):

        self.kolona = 11 
        self.vrsta = 14

        self.igrac1vrsta = 4 #pocetne pozicije igrac
        self.igrac1kolona = 4
        self.igrac2vrsta = 4
        self.igrac2kolona = 8
        self.igrac3vrsta = 11
        self.igrac3kolona = 4
        self.igrac4vrsta = 11
        self.igrac4kolona = 8

        self.igracIksZeleni = 3 #koliko koji igrac ima plavih i zelenih zidova
        self.igracIksPlavi = 3
        self.igracOksZeleni = 3
        self.igracOksPlavi = 3

        #self.ucitaj_vrstu_kolonu()
        #self.ucitaj_igrace()
        #self.ucitaj_zidove()       
        print('CESTITAMO, USPESNO STE UNELI POCETNE PARAMETRE, MOZETE POCETI SA IGROM')

        self.polje_height = 6/10 * height//self.vrsta #sirina i visina sivih kockica na tabli
        self.polje_width = 6/10 * width//self.kolona

        self.tabla = []  #tu se pamti gde se svaki igrac nalazi
        self.zidVertikalni = [] #lista zidova zelenih
        self.zidHorizontalni = [] #lista plavih zidova

        self.pocetni1 = Igrac(self.igrac1vrsta, self.igrac1kolona, ORANGE, self.polje_height, self.polje_width)
        self.pocetni2 = Igrac(self.igrac2vrsta, self.igrac2kolona, ORANGE, self.polje_height, self.polje_width)
        self.pocetni3 = Igrac(self.igrac3vrsta, self.igrac3kolona, GOLD, self.polje_height, self.polje_width)
        self.pocetni4 = Igrac(self.igrac4vrsta, self.igrac4kolona, GOLD, self.polje_height, self.polje_width)
        
        self.pobednik = 0

        self.create_tablu() #popunjavanje liste tabla, gde je prazno polje upisuje se nula gde ima igraca upisuje se Igrac
        self.kreiraj_zidove() # isto samo za zidove



    def pronadji_put(self, tabla):
        
        igraci_crveni = tabla.get_all_pieces(RED)
        igraci_plavi = tabla.get_all_pieces(BLUE)
        

        igrac1vrsta = igraci_crveni[0].vrsta
        igrac1kolona = igraci_crveni[0].kolona
        igrac2vrsta = igraci_crveni[1].vrsta
        igrac2kolona = igraci_crveni[1].kolona

        igrac3vrsta = igraci_plavi[0].vrsta
        igrac3kolona = igraci_plavi[0].kolona
        igrac4vrsta = igraci_plavi[1].vrsta
        igrac4kolona = igraci_plavi[1].kolona

        
        if self.pronadji_putDFS((igrac1vrsta, igrac1kolona), (tabla.pocetni3.vrsta, tabla.pocetni3.kolona), RED, tabla):
            if self.pronadji_putDFS((igrac1vrsta, igrac1kolona), (tabla.pocetni4.vrsta, tabla.pocetni4.kolona), RED, tabla):
                if self.pronadji_putDFS((igrac2vrsta, igrac2kolona), (tabla.pocetni3.vrsta, tabla.pocetni3.kolona), RED, tabla):
                    if self.pronadji_putDFS((igrac2vrsta, igrac2kolona), (tabla.pocetni4.vrsta, tabla.pocetni4.kolona), RED, tabla):

                        if self.pronadji_putDFS((igrac3vrsta, igrac3kolona), (tabla.pocetni1.vrsta, tabla.pocetni1.kolona), BLUE, tabla):
                           if self.pronadji_putDFS((igrac3vrsta, igrac3kolona), (tabla.pocetni2.vrsta, tabla.pocetni2.kolona), BLUE, tabla):
                               if self.pronadji_putDFS((igrac4vrsta, igrac4kolona), (tabla.pocetni1.vrsta, tabla.pocetni1.kolona), BLUE, tabla):
                                    if self.pronadji_putDFS((igrac4vrsta, igrac4kolona), (tabla.pocetni2.vrsta, tabla.pocetni2.kolona), BLUE, tabla): 
                                        return True 
        
        return False

    def prazna_tabla(self): 
        self.tabla.clear()    
        self.zidVertikalni.clear() 
        self.zidHorizontalni.clear() 

    def pronadji_putDFS(self, start, end, boja, tabla):  #start, end je tuple (vrsta, kolona)
        if(start == end):
            path = list()
            path.append(start)
            return path

        #privremeni_igrac = tabla.tabla[start[1]][start[0]] 
        #tabla.tabla[start[1]][start[0]] = 0

        stack_nodes = queue.LifoQueue(100)
        visited = set()

        prev_nodes = dict()
        prev_nodes[start] = None
   
        found_dest = False

        visited.add(start)
        stack_nodes.put(start)

        while (not found_dest) and (not stack_nodes.empty()):
            node = stack_nodes.get()          
            for dest in tabla.get_valid_moves(Igrac(node[0]+1, node[1]+1, boja, self.polje_height, self.polje_width)):                
                if dest not in visited:
                    prev_nodes[dest] = node
                    
                    if dest == end:
                        found_dest = True
                        break
                    
                    visited.add(dest)
                    stack_nodes.put(dest)
                    
        path = list()
        if found_dest:
            
            path.append(end)         
            prev = prev_nodes[end] 
            while prev != None:   
                path.append(prev)
                prev = prev_nodes[prev]

            path.reverse()

        #tabla.tabla[start[1]][start[0]] = privremeni_igrac                  
        return found_dest

    def nacrtaj_put(self, win, lista): #metoda se koristila kada se implemetirao DFS algoritam kako bi se vizualno video put
        nova_lista = []
        for put in lista:
            nova_lista.append(Igrac(put[0]+1, put[1]+1, GREEN, self.polje_height, self.polje_width))


        for zelena in nova_lista:
            zelena.draw(win)
       
    def dodaj_zeleni_zid(self, zeleni_zid):


        kolona = zeleni_zid[0]
        vrsta = zeleni_zid[1]
        self.zidVertikalni[kolona][vrsta] = Zid(vrsta, kolona, GREEN, self.polje_height, self.polje_width)
        self.zidVertikalni[kolona+1][vrsta] = Zid(vrsta, kolona+1, GREEN, self.polje_height, self.polje_width)

    def dodaj_plavi_zid(self, plavi_zid):
        kolona = plavi_zid[0]
        vrsta = plavi_zid[1]
        self.zidHorizontalni[kolona][vrsta] = Zid(vrsta-1, kolona+1, BLUE2, self.polje_height, self.polje_width)
        self.zidHorizontalni[kolona][vrsta+1] = Zid(vrsta, kolona+1, BLUE2, self.polje_height, self.polje_width)
        
    def proceni_stanje_zid(self, pozicija, boja):
        kolona = pozicija[0]
        vrsta = pozicija [1] 
        suma = float('-inf')
        for row in self.tabla:
            for igrac in row:
                if igrac != 0 and igrac.boja == BLUE:
                    igrac_kolona = igrac.kolona
                    igrac_vrsta = igrac.vrsta-1

                    if boja == GREEN:
                        if igrac.vrsta == vrsta+1:
                            suma1 = -abs(abs(kolona - igrac_kolona) + abs(vrsta - igrac_vrsta)) + 0.1
                            suma = max(suma1, suma)
                        else:
                            suma1 = -abs(abs(kolona - igrac_kolona) + abs(vrsta - igrac_vrsta)) 
                            suma = max(suma1, suma)
                    else:
                        suma1 = -abs(abs(kolona - igrac_kolona) + abs(vrsta - igrac_vrsta)) 
                        suma = max(suma1, suma)
        return suma
        
    def proceni_stanje_igrac(self, figura, tablica_prethodnih_stanja):
        global tablica

        kolona = figura.kolona
        vrsta = figura.vrsta

        for index , stanje in enumerate(tablica_prethodnih_stanja[-5:]):

            if tablica_prethodnih_stanja == None:
                pass
            
            elif stanje[0].vrsta == vrsta and stanje[0].kolona == kolona:
                cena = stanje[1]
                cena-=500 
                tablica[index] = (stanje[0], cena)                     
                return -abs(abs(kolona - self.pocetni4.kolona) + abs(vrsta - self.pocetni4.vrsta)) - abs(cena) 


        procena1 = -abs(abs(kolona - self.pocetni3.kolona) + abs(vrsta - self.pocetni3.vrsta))
        procena2 = -abs(abs(kolona - self.pocetni4.kolona) + abs(vrsta - self.pocetni4.vrsta))

        if procena1 > procena2:
            return procena1
        else:
            return procena2

    def sve_kombinacije_zidova_zelenih(self):
        kombinacije_zelenih = []
        for kolona in range(self.kolona-1):
            for vrsta in range (self.vrsta-1):
                if kolona +1 < self.kolona:
                    if self.zidVertikalni[kolona][vrsta] == 0 and self.zidVertikalni[kolona+1][vrsta] == 0:  
                        if self.zidHorizontalni[kolona][vrsta] != 0 and self.zidHorizontalni[kolona][vrsta+1] != 0:
                            pass
                        else:
                            kombinacije_zelenih.append((kolona,vrsta))  

        return(kombinacije_zelenih)

    def sve_kombinacije_zidova_plavih(self):
        kombinacije_plavih = []
        for kolona in range(self.kolona-1):
            for vrsta in range (self.vrsta-1):
                if vrsta+1 < self.vrsta:
                    if self.zidHorizontalni[kolona][vrsta] == 0 and self.zidHorizontalni[kolona][vrsta+1] == 0:  
                        if self.zidVertikalni[kolona][vrsta] != 0 and self.zidVertikalni[kolona+1][vrsta] != 0:
                            pass
                        else:
                            kombinacije_plavih.append((kolona,vrsta))  

        return(kombinacije_plavih)
                     
    def get_all_pieces(self, boja): #radii
        pieces = []
        for row in self.tabla:
            for piece in row:
                if piece != 0 and piece.boja == boja:
                    pieces.append(piece)
        return pieces

    def ucitaj_zidove(self): #metoda za unos broja zidova iz konzole, oba igraca imaju isti broj zidova
        while True:
            self.igracIksZeleni =  self.igracOksZeleni = int(input("Unesite broj Zelenih(vertikalnih) zidova:")) 
            self.igracIksPlavi =  self.igracOksPlavi = int(input("Unesite broj Plavih(horizontalnih) zidova:")) 
            break

    def stanje_sa_zidovima(self, win):

        pygame.draw.rect(win, BLACK, (width/10,height*8/10, width*8/10, height*2/10))
        pozicije = FONT2.render('IGRAC OKS(PLAVI)_COVEK IMA JOS' + '     ' + str(self.igracIksZeleni) + '     ' + 'ZELENIH ZIDOVA' + '     ' + 'I' + '     ' + str(self.igracIksPlavi) + '     ' 'PLAVIH ZIDOVA', 100, WHITE)
        win.blit(pozicije,(width/10 ,height*8/10)) 
        pozicije = FONT2.render('IGRAC IKS(CRVENI)_AI IMA JOS' + '     ' + str(self.igracOksZeleni) + '     ' + 'ZELENIH ZIDOVA' + '     ' + 'I' + '     ' + str(self.igracOksPlavi) + '     ' 'PLAVIH ZIDOVA', 100, WHITE)
        win.blit(pozicije,(width/10,height*9/10)) 

    def ucitaj_igrace(self): #metoda za ucitavanje pozicija igraca iz konzole
        while True:      
           self.igrac1kolona= int(input("Unesite vrstu iks1 igrača:")) 
           self.igrac1vrsta= int(input("Unesite kolonu iks1 igrača:")) 

           self.igrac2kolona= int(input("Unesite vrstu iks2 igrača:")) 
           self.igrac2vrsta= int(input("Unesite kolonu iks2 igrača:")) 

           self.igrac3kolona= int(input("Unesite vrstu oks1 igrača:")) 
           self.igrac3vrsta= int(input("Unesite kolonu oks1 igrača:")) 

           self.igrac4kolona= int(input("Unesite vrstu oks2 igrača:")) 
           self.igrac4vrsta= int(input("Unesite kolonu oks2 igrača:")) 
           break
        
    def ucitaj_vrstu_kolonu(self): #ucitavanje vrste i kolone iz terminala
        while True: 
           self.kolona = int(input("Unesite broj vrsta table: "))     
           self.vrsta = int(input("Unesite broj kolona table: "))
           break
       
    def nacrtaj_pocetne_poz(self,win): #metoda za isrtavanje pocetnih pozicija igraca(narandzasti i zuti krug)
    
        self.pocetni1.draw(win)
        self.pocetni2.draw(win)
        self.pocetni3.draw(win)
        self.pocetni4.draw(win)

    def move(self, igrac, vrsta, kolona): #metoda koja u listi menja mesta stare i nove pozicije igraca, 
        self.tabla[igrac.kolona][igrac.vrsta], self.tabla[kolona][vrsta] = self.tabla[kolona][vrsta], self.tabla[igrac.kolona][igrac.vrsta] #ovakav nacin zamene sam video na youtube kanalu TechWithTim
        igrac.move(vrsta, kolona)

    def create_tablu(self): #metoda koja u listi tabla za svaku kolonu apenduje listu i onda u tu listu ako se vrsta/kolona poklapa sa pocetnim pozicijama nekog igraca ona apenduje listu i u nju Igraca ako ne apenduje nulu
        for kolona in range(self.kolona +1):
            self.tabla.append([])
            for vrsta in range (self.vrsta +1): 
                if  (self.igrac1vrsta == vrsta+1  and self.igrac1kolona == kolona+1):
                    self.tabla[kolona].append(Igrac(self.igrac1vrsta, self.igrac1kolona, RED, self.polje_height, self.polje_width))

                elif(self.igrac2vrsta == vrsta+1 and self.igrac2kolona == kolona+1):
                    self.tabla[kolona].append(Igrac(self.igrac2vrsta, self.igrac2kolona, RED, self.polje_height, self.polje_width))

                elif(self.igrac3vrsta == vrsta+1 and self.igrac3kolona == kolona+1):
                    self.tabla[kolona].append(Igrac(self.igrac3vrsta, self.igrac3kolona, BLUE, self.polje_height, self.polje_width))

                elif(self.igrac4vrsta == vrsta+1 and self.igrac4kolona == kolona+1):
                    self.tabla[kolona].append(Igrac(self.igrac4vrsta, self.igrac4kolona, BLUE, self.polje_height, self.polje_width))

                else:
                    self.tabla[kolona].append(0)

    def draw_squares(self, win): #crta crna i siva polja na tabli

        for kolona in range(self.kolona):
            for vrsta in range(self.vrsta):     #2/10 height kako se ne bi crtalo od skroz leve pozicije
                pygame.draw.rect(win, BLACK, (vrsta*self.polje_height + 2/10* height, kolona * self.polje_width + 1/10* width, self.polje_height, self.polje_width)) 

        for kolona in range(self.kolona):
            for vrsta in range(kolona % 2, self.vrsta, 2):
                pygame.draw.rect(win, GREY, (vrsta*self.polje_height + 2/10* height, kolona * self.polje_width + 1/10* width, self.polje_height, self.polje_width))
 
    def draw(self, win): #konstantno se poziva i na osnovu stanja u listama crta igrace i zidove
        self.nacrtaj_text()
        for kolona in range (self.kolona):
            for vrsta in range (self.vrsta):
                igrac = self.tabla[kolona][vrsta]
                zidVertikalni = self.zidVertikalni[kolona][vrsta]
                zidHorizontalni = self.zidHorizontalni[kolona][vrsta]
                if igrac != 0:
                    igrac.draw(win)
                if zidVertikalni != 0:
                    zidVertikalni.drawVertikalni(win)
                if zidHorizontalni !=0:
                    zidHorizontalni.drawHorizontalni(win)

    def kreiraj_zidove(self):  #slicno kao za listu tabla. Cilj je da svako polje sadrzi listu u kojoj bi se upisao Zid ako se on nalazi na toj pozociji
        for kolona in range(self.kolona):
            self.zidVertikalni.append([])
            self.zidHorizontalni.append([])
            for vrsta in range (self.vrsta):
                self.zidVertikalni[kolona].append(0)
                self.zidHorizontalni[kolona].append(0)
        
    def nacrtaj_text(self):  
         for number in range (self.vrsta): #TOP-TEXT
             okvir = pygame.Rect(number * self.polje_height + 2/10* height + 1/4 * self.polje_height , height * 6/100, self.polje_width, self.polje_width )
             pozicije = FONT1.render(str(number+1), 1, WHITE)
             WIN.blit(pozicije,okvir) #KOLIKO kolone toliko kvadratica


            
         for number in range (self.kolona): #LEFT-TEXT
             okvir = pygame.Rect(width * 17/100, number * self.polje_width + 1/10* width + 1/6 * self.polje_width  , self.polje_width, self.polje_width )
             pozicije = FONT1.render(str(number+1), 1, WHITE)
             WIN.blit(pozicije,okvir) 



         for number in range (self.kolona): #RIGHT-TEXT
             okvir = pygame.Rect(width * 81/100, number * self.polje_width + 1/10* width + 1/6 * self.polje_width  , self.polje_width, self.polje_width )
             pozicije = FONT1.render(str(number+1), 1, WHITE)
             WIN.blit(pozicije,okvir) 

         for number in range (self.vrsta): #BOT-TEXT
             okvir = pygame.Rect(number * self.polje_height + 2/10* height + 1/4 * self.polje_height , height * 69/100, self.polje_width, self.polje_width )
             pozicije = FONT1.render(str(number+1), 1, WHITE)
             WIN.blit(pozicije,okvir) #KOLIKO kolone toliko kvadratica

    def vrati_igraca(self, vrsta, kolona):

        return self.tabla[kolona][vrsta] 
        
    def get_valid_moves(self, igrac):

        moves = []
        
        if igrac.boja == RED or igrac.boja == BLUE:
        
          self.ispitaj_dole(igrac, moves)

          self.ispitaj_gore(igrac, moves)
        
          self.ispitaj_levo(igrac, moves)

          self.ispitaj_desno(igrac, moves)

          self.ispitaj_dijagonala1(igrac, moves)
          
          self.ispitaj_dijagonala2(igrac, moves)

          self.ispitaj_dijagonala3(igrac, moves)

          self.ispitaj_dijagonala4(igrac, moves)

          self.ispitaj_zavrsni_potez(igrac, moves)
                  
    
        return moves

    def ispitaj_dole(self, igrac, moves):

        if igrac.kolona+1 < self.kolona-1:
            if self.tabla[igrac.kolona+2][igrac.vrsta] == 0:  #DOLE DVA
               if self.zidHorizontalni[igrac.kolona][igrac.vrsta]== 0 and self.zidHorizontalni[igrac.kolona+1][igrac.vrsta] == 0:

                  moves.append((igrac.vrsta, igrac.kolona+2))

            elif self.tabla[igrac.kolona+1][igrac.vrsta] == 0 and self.zidHorizontalni[igrac.kolona][igrac.vrsta]== 0 and self.zidHorizontalni[igrac.kolona+1][igrac.vrsta] == 0:  
               moves.append((igrac.vrsta, igrac.kolona+1))

    def ispitaj_gore(self, igrac, moves):
        if igrac.kolona-1 > 0:
           if self.tabla[igrac.kolona-2][igrac.vrsta] == 0:
               if self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0 and self.zidHorizontalni[igrac.kolona-2][igrac.vrsta] == 0:  #GORE DVA
                  moves.append((igrac.vrsta, igrac.kolona-2))

           elif self.tabla[igrac.kolona-1][igrac.vrsta] == 0 and self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0 and self.zidHorizontalni[igrac.kolona-2][igrac.vrsta] == 0:  #GOREjedno
                moves.append((igrac.vrsta, igrac.kolona-1))
    
    def ispitaj_levo(self, igrac, moves):
        if igrac.vrsta-1 > 0:
          if self.tabla[igrac.kolona][igrac.vrsta-2] == 0: 
              if self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta-2]== 0 : #ako levo od njega, i polje dalje nema vertikalni
                 moves.append((igrac.vrsta-2, igrac.kolona))
          elif self.tabla[igrac.kolona][igrac.vrsta-1] == 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0 and  self.zidVertikalni[igrac.kolona][igrac.vrsta-2]== 0:  
                moves.append((igrac.vrsta-1, igrac.kolona))

    def ispitaj_desno(self, igrac, moves):
        if igrac.vrsta+1 < self.vrsta-1:
           if self.tabla[igrac.kolona][igrac.vrsta+2] == 0: #ako na drugo polje desno nema igraca
               if self.zidVertikalni[igrac.kolona][igrac.vrsta+1]== 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta]== 0 : #ako desno od njega, i polje dalje nema vertikalni
                  moves.append((igrac.vrsta+2, igrac.kolona))
           elif self.tabla[igrac.kolona][igrac.vrsta+1] == 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta] == 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta+1] == 0:  #desno jedan
              moves.append((igrac.vrsta+1, igrac.kolona))

    def ispitaj_dijagonala1(self, igrac, moves):
        if igrac.kolona > 0 and igrac.vrsta-1 >= 0:
           if self.tabla[igrac.kolona-1][igrac.vrsta-1] == 0: 
               if self.zidVertikalni[igrac.kolona-1][igrac.vrsta-1]== 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0 and self.zidHorizontalni[igrac.kolona-1][igrac.vrsta-1]== 0 and self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta-1, igrac.kolona-1))

    def ispitaj_dijagonala2(self, igrac, moves):
        if igrac.kolona > 0 and igrac.vrsta+1 < self.vrsta:
           if self.tabla[int(igrac.kolona-1)][int(igrac.vrsta+1)] == 0: 
               if self.zidVertikalni[igrac.kolona-1][igrac.vrsta]== 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta]== 0 and self.zidHorizontalni[igrac.kolona-1][igrac.vrsta+1]== 0 and self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta+1, igrac.kolona-1))

    def ispitaj_dijagonala3(self, igrac, moves):
        if igrac.kolona+1 < self.kolona and igrac.vrsta-1 >= 0:
           if self.tabla[int(igrac.kolona+1)][int(igrac.vrsta-1)] == 0: 
               if self.zidVertikalni[igrac.kolona+1][igrac.vrsta-1]== 0 and self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0 and self.zidHorizontalni[igrac.kolona][igrac.vrsta-1]== 0 and self.zidHorizontalni[igrac.kolona][igrac.vrsta]== 0 :
                  moves.append((igrac.vrsta-1, igrac.kolona+1))

    def ispitaj_dijagonala4(self, igrac, moves):
        if igrac.kolona+1 < self.kolona and igrac.vrsta+1 < self.vrsta:
           if self.tabla[int(igrac.kolona+1)][int(igrac.vrsta+1)] == 0: 
               if self.zidVertikalni[igrac.kolona][igrac.vrsta]== 0 and self.zidVertikalni[igrac.kolona+1][igrac.vrsta]== 0 and self.zidHorizontalni[igrac.kolona][igrac.vrsta]== 0 and self.zidHorizontalni[igrac.kolona][igrac.vrsta+1]== 0 :
                  moves.append((igrac.vrsta+1, igrac.kolona+1))
     
    def ispitaj_zavrsni_potez(self, igrac, moves):
        

        if igrac.boja == RED:

            if igrac.kolona == self.pocetni3.kolona and igrac.vrsta+1 == self.pocetni3.vrsta: #desno
                if self.zidVertikalni[igrac.kolona][igrac.vrsta]== 0:
                   moves.append((igrac.vrsta+1, igrac.kolona))

            if igrac.kolona == self.pocetni3.kolona and igrac.vrsta-1 == self.pocetni3.vrsta: #levo
               if self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0:
                  moves.append((igrac.vrsta-1, igrac.kolona))

            if igrac.kolona-1 == self.pocetni3.kolona and igrac.vrsta == self.pocetni3.vrsta: #gore
               if self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta, igrac.kolona-1))

            if igrac.kolona+1 == self.pocetni3.kolona and igrac.vrsta == self.pocetni3.vrsta: #dole
                if self.zidHorizontalni[igrac.kolona][igrac.vrsta] == 0:
                   moves.append((igrac.vrsta, igrac.kolona+1))


            if igrac.kolona == self.pocetni4.kolona and igrac.vrsta+1 == self.pocetni4.vrsta:
                if self.zidVertikalni[igrac.kolona][igrac.vrsta]== 0:
                   moves.append((igrac.vrsta+1, igrac.kolona))

            if igrac.kolona == self.pocetni4.kolona and igrac.vrsta-1 == self.pocetni4.vrsta:
                if self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0:  
                   moves.append((igrac.vrsta-1, igrac.kolona))

            if igrac.kolona-1 == self.pocetni4.kolona and igrac.vrsta == self.pocetni4.vrsta:
               if self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta, igrac.kolona-1))

            if igrac.kolona+1 == self.pocetni4.kolona and igrac.vrsta == self.pocetni4.vrsta:
               if self.zidHorizontalni[igrac.kolona][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta, igrac.kolona+1))

        elif igrac.boja == BLUE:

            if igrac.kolona == self.pocetni1.kolona and igrac.vrsta+1 == self.pocetni1.vrsta: #desno
                if self.zidVertikalni[igrac.kolona][igrac.vrsta]== 0:
                   moves.append((igrac.vrsta+1, igrac.kolona))

            if igrac.kolona == self.pocetni1.kolona and igrac.vrsta-1 == self.pocetni1.vrsta: #levo
               if self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0:
                  moves.append((igrac.vrsta-1, igrac.kolona))

            if igrac.kolona-1 == self.pocetni1.kolona and igrac.vrsta == self.pocetni1.vrsta: #gore
               if self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta, igrac.kolona-1))

            if igrac.kolona+1 == self.pocetni1.kolona and igrac.vrsta == self.pocetni1.vrsta: #dole
                if self.zidHorizontalni[igrac.kolona][igrac.vrsta]== 0:
                   moves.append((igrac.vrsta, igrac.kolona+1))


            if igrac.kolona == self.pocetni2.kolona and igrac.vrsta+1 == self.pocetni2.vrsta:
                if self.zidVertikalni[igrac.kolona][igrac.vrsta]== 0:
                   moves.append((igrac.vrsta+1, igrac.kolona))

            if igrac.kolona == self.pocetni2.kolona and igrac.vrsta-1 == self.pocetni2.vrsta:
                if self.zidVertikalni[igrac.kolona][igrac.vrsta-1]== 0:  
                   moves.append((igrac.vrsta-1, igrac.kolona))

            if igrac.kolona-1 == self.pocetni2.kolona and igrac.vrsta == self.pocetni2.vrsta:
               if self.zidHorizontalni[igrac.kolona-1][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta, igrac.kolona-1))

            if igrac.kolona+1 == self.pocetni2.kolona and igrac.vrsta == self.pocetni2.vrsta:
               if self.zidHorizontalni[igrac.kolona][igrac.vrsta]== 0:
                  moves.append((igrac.vrsta, igrac.kolona+1))
