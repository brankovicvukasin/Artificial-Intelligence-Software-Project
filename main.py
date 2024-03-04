import pygame
import sys
pygame.font.init()
from blockade.constants import *
from blockade.igrac import *
from blockade.tabla import *
from blockade.game import *
from minimax.algorithm import * 
from minimax.algorithmZid import * 


#MAX JE CRVENI IGRA PRVI I TO JE AI

pygame.init()
#__INIT__PY fajl se koristi kako bi govorio da je folder package i da moze da se importuje


pygame.display.set_caption("BLOCKADE_V1.0.0")


def main():
    clock = pygame.time.Clock()
    game = Game(WIN)

    def pozicija_misa(pos):
        x, y = pos
        x = x - 2/10 * width
        y = y - 1/10 * height
        kolona = y  // game.tabla.polje_width
        vrsta = x // game.tabla.polje_height
        return int(vrsta), int(kolona)

    run =True
    while run: #run petlja
        
        game.update()
        

        if game.turn == RED:
  
            vrednost, nova_tabla, figura = minimax(game.tabla, 1 , True, None, float('-inf'), float('inf'))
            
            game.ai_potez(nova_tabla)
            prethodni_potez(nova_tabla[1], 0)


            vrednost, nova_tabla2, zid = minimax2(game.tabla, 1 , True, game, None, None, float('-inf'), float('inf'))
            
            if nova_tabla2 != None: #ako se desi da je nestalo zidova, da ne bi doslo do pucanja igre kad minimax vrati None
                game.ai_potez_zid(nova_tabla2)
                
            else:     
                game.ai_potez(nova_tabla)
                game.promeni_potez()

            print('AI je pomerio pesaka na polje: ', 'VRSTA' ,(figura.kolona) ,'KOLONA' , (figura.vrsta+2))
            if zid != None:
                print('POSTAVIO JE ZID NA', 'VRSTA', zid[0]+1, 'KOLONA' ,zid[1]+1)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:  #Quit event. Kada korisnik iskljuci prozor
               run=False 

            if event.type == pygame.MOUSEBUTTONDOWN:  
                pos = pygame.mouse.get_pos()
                vrsta, kolona = pozicija_misa(pos)
                game.select(vrsta, kolona)

                if keys_pressed[pygame.K_z]:
                  pos = pygame.mouse.get_pos()
                  vrsta, kolona = pozicija_misa(pos)
                  game.select2(int(vrsta), int(kolona))

                elif keys_pressed[pygame.K_p]:
                   pos = pygame.mouse.get_pos()
                   vrsta, kolona = pozicija_misa(pos)
                   game.select3(int(vrsta), int(kolona))


        keys_pressed = pygame.key.get_pressed() #svaki taster koji se pritisne ce biti upisan ovde       
        
        
        pygame.display.update()

    pygame.quit()    
    


if __name__ == "__main__":
    main()


