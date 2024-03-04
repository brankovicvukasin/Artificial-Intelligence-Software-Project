from copy import deepcopy #deep copy kopira ne samo referencu vec i ceo objekat
import pygame

RED = (255,0,0) #MAX
BLUE = (0,0,255) #MIN
GREEN = (0,255,0)



def minimax2(tabla, dubina, max_igrac, game, potez2, boja, alpha, beta): 

    if dubina == 0:
        return tabla.proceni_stanje_zid(potez2, boja), tabla 
        
    if max_igrac == True:
        maxProcena = float('-inf') 
        najbolji_potez = None
        najbolji_zid = None
        for potez in vrati_sve_poteze(tabla):
            evaluation = minimax2(potez[0], dubina-1, False, game, potez[1], potez[2], alpha, beta)[0]
            prethodni_max = maxProcena

            maxProcena = max(maxProcena, evaluation)
            alpha = max(alpha, maxProcena)
            if beta <= alpha:
                break
            if maxProcena == evaluation:
                if ne_zatvara_put(potez):
                   najbolji_potez = potez[0]
                   najbolji_zid = potez[1]
                else:
                    #print('Zatvara')
                    maxProcena = prethodni_max
                    najbolji_zid = potez[1]


        return maxProcena, najbolji_potez, najbolji_zid
    else:
        minEval = float('inf')
        best_move = None
        for move in vrati_sve_poteze(tabla):
            evaluation = minimax2(move[0], dubina-1, True, game, move[1], move[2], alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, minEval)
            if beta <= alpha:
                break
            if minEval == evaluation:
                best_move = move[0]
        return minEval, best_move


def ne_zatvara_put(tabla):

    if tabla[0].pronadji_put(tabla[0]):
        return True
    else:
        return False
  



def vrati_sve_poteze(tabla):
    tabla1 = tabla
    moves = [] 

    for zeleni_zid in tabla1.sve_kombinacije_zidova_zelenih():
            privremena_tabla = deepcopy(tabla1) 
            nova_tabla = simuliraj_potez(zeleni_zid, privremena_tabla, GREEN) 
            if ima_zidova(nova_tabla, GREEN):

                nova_tabla.igracOksZeleni-=1
                moves.append((nova_tabla, zeleni_zid, GREEN))
                  

    for plavi_zid in tabla1.sve_kombinacije_zidova_plavih():
            privremena_tabla = deepcopy(tabla1) 
            nova_tabla2 = simuliraj_potez(plavi_zid, privremena_tabla, BLUE) 
            if ima_zidova(nova_tabla2, BLUE):

                nova_tabla2.igracOksPlavi-=1
                moves.append((nova_tabla2, plavi_zid, BLUE))
                            
    return moves

def simuliraj_potez(zeleni_zid, tabla, boja):

    if boja == GREEN:
        tabla.dodaj_zeleni_zid(zeleni_zid) 

    elif boja == BLUE:
        tabla.dodaj_plavi_zid(zeleni_zid)
           
    return tabla 

def ima_zidova(tabla, boja):
        if boja == GREEN:
            if tabla.igracOksZeleni>0:
                return True
        elif boja == BLUE:
            if tabla.igracOksPlavi>0:
                return True
        else:
            return False