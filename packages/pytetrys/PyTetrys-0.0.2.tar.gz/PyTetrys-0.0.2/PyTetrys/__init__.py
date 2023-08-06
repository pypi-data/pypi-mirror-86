import pygame
from pecas import *
from constantes import *
import random
import sys
 

pygame.font.init()


pos_x = (LARGURA_TELA - LARGURA_JOGO) // 2
pos_y = (ALTURA_TELA - ALTURA_JOGO) // 2

cores_pecas = [VERMELHO, ROXO, AZUL_CLARO, AZUL_ESCURO, AMARELO, ROSA, VERDE]
formatos = [S, Z, I, O, J, L, T]

class Pecas(object):
    def __init__(self, x, y, formato):
        self.x = x
        self.y = y
        self.formato = formato
        self.cor = cores_pecas[formatos.index(formato)]
        self.rotation = 0

def gerar_grid(tela):
    for j in range(0, 9):
        for i in range(0, 19):
            retang = pygame.Rect(j*30 + pos_x, i*30 + 50, 60, 60)
            pygame.draw.rect(tela, AZUL_CLARO, retang, 2)


def exibir_tela():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Pytetris')
    return tela

def loop(tela):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gerar_grid(tela)
        pygame.display.update()



def main():
    tela = exibir_tela()
    loop(tela)
        

if __name__ == "__main__":
    main()
