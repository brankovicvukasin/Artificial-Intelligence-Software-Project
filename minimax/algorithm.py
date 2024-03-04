from copy import deepcopy #deep copy kopira ne samo referencu vec i ceo objekat
import pygame
from blockade.igrac import *

RED = (255,0,0) #MAX
BLUE = (0,0,255) #MIN

tablica = [] #pamti prethodne poteze ai-a
brojac = 0
prethodni_potez = 0

def prethodni_potez(tabla1, cena): 
    
    global tablica, brojac
    tablica.append((tabla1, cena))
    brojac+=1

 
  
    

def minimax(tabla, dubina, max_igrac, figura, alpha, beta): 
    global tablica

    if dubina == 0:
        return tabla.proceni_stanje_igrac(figura, tablica), tabla #vraca tablu sa procenom trenutne vrednosti
        
    if max_igrac == True:
        maxProcena = float('-inf') 
        najbolji_potez = None
        for potez in vrati_sve_poteze(tabla, RED):
            evaluation, desk = minimax(potez[0], dubina-1, False, potez[1], alpha, beta)
            najbolji_igrac = potez[1]

            maxProcena = max(maxProcena, evaluation)
            alpha = max(alpha, maxProcena)
            if beta <= alpha:
                break

            if maxProcena == evaluation:
                najbolji_igrac = potez[1]
                najbolji_potez = potez
               
        
        return maxProcena, najbolji_potez, najbolji_igrac
    else:
        minEval = float('inf')
        best_move = None
        for move in vrati_sve_poteze(tabla, BLUE):
            evaluation, desk, najbolji = minimax(move[0], dubina-1, True, move[1], alpha, beta)
            minEval = min(minEval, evaluation)
            beta = min(beta, minEval)
            if beta <= alpha:
                break
            if minEval == evaluation:
                best_move = move
        return minEval, best_move


def vrati_sve_poteze(tabla, boja):
    moves = [] #lista svih mogucih poteza za sve igrace odredjene boje
    for igrac in tabla.get_all_pieces(boja):
        moguci_potezi = tabla.get_valid_moves(igrac)
        for potez in moguci_potezi:
            privremena_tabla = deepcopy(tabla) 
  
            privremena_figura = privremena_tabla.vrati_igraca(igrac.vrsta, igrac.kolona)         
            nova_tabla = simuliraj_potez(privremena_figura, potez, privremena_tabla) 
            moves.append((nova_tabla, privremena_figura))

    return moves

def simuliraj_potez(figura, move, tabla): 
    tabla.move(figura, move[0] , move[1])
    return tabla

def da_li_je_bio_potez(figura):
    for ai in tablica:
        if ai == figura:   
            return None
    
    return True

