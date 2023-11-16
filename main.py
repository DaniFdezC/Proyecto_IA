import sys
import time

from CreadorMapa import convertirImagenAMatriz
from Robot import Robot
import matplotlib.pyplot as plt
import pygame
import numpy as np
from collections import deque
from Casilla import *

HEIGHT = 500
WIDTH = 750


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


"""def print_explored_area(mapaGlobal, mapaLocal):
    
    for row in range(len(mapaGlobal)):
        for col in range(len(mapaGlobal[0])):
            if mapaLocal[row][col].tipo is TipoCasilla.VISITADO:
                print("V", end=" ")  # Visited
            else:
                print("X" if mapaGlobal[row][col].tipo == TipoCasilla.PARED else " ", end=" ")  # Wall or free space
        print()"""


ruta_imagen = "./Imagenes/mapaDefinitivo.png"
matriz_resultante = convertirImagenAMatriz(ruta_imagen)
matriz_resultante[3][98].tipoObjetivo = TipoObjetivo.LIBRE

filas = len(matriz_resultante)
columnas = len(matriz_resultante[0])

tamano_casilla = 5
niebla =[[Casilla(TipoCasilla.NIEBLA) for _ in range(columnas)] for _ in range(filas)]

pantalla = pygame.display.set_mode((columnas*tamano_casilla, filas*tamano_casilla))
pygame.display.set_caption("Matriz de Casillas")

campoVision = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]

robot1 = Robot(matriz_resultante, (27, 27), campoVision, niebla)
robot2 = Robot(matriz_resultante, (7, 92), campoVision, niebla)
robot3 = Robot(matriz_resultante, (9, 147), campoVision, niebla)
robot4 = Robot(matriz_resultante, (43, 96), campoVision, niebla)
robot5 = Robot(matriz_resultante, (43, 98), campoVision, niebla)
robot6 = Robot(matriz_resultante, (78, 27), campoVision, niebla)
robot7 = Robot(matriz_resultante, (67, 94), campoVision, niebla)
robot8 = Robot(matriz_resultante, (97, 86), campoVision, niebla)

#robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8]
robots = [robot1]
iteraciones = 0
while True:
    for robot in robots:
        robot.moverse()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Limpiar la pantalla
        pantalla.fill((255, 255, 255))

        # Dibujar la matriz en la pantalla
        for i, fila in enumerate(niebla):
            for j, casilla in enumerate(fila):

                if casilla.tipo is TipoCasilla.PARED:
                    color = BLACK
                elif (i, j) == robot.coordenadas and matriz_resultante[i][j].tipoObjetivo is TipoObjetivo.LIBRE:
                    matriz_resultante[i][j].tipoObjetivo = TipoObjetivo.CAPTURADO
                    color = BLUE
                elif (i, j) == robot.coordenadas:
                    color = BLUE
                elif casilla.tipoObjetivo is TipoObjetivo.LIBRE:
                    color = RED
                elif casilla.tipo is TipoCasilla.NIEBLA:
                    color = GREY
                elif casilla.tipoObjetivo is TipoObjetivo.CAPTURADO:
                    color=GREEN
                elif casilla.tipo is TipoCasilla.VISITADO:
                    color = YELLOW
                else:
                    color = WHITE

                pygame.draw.rect(pantalla, color, (j * tamano_casilla, i * tamano_casilla, tamano_casilla, tamano_casilla))

        # Actualizar la pantalla
        pygame.display.flip()
        time.sleep(0.1)
    iteraciones += 1
    print(iteraciones)



"""while True:
    for robot in robots:
        sePuedeMover = robot.moverse()
        if sePuedeMover is False:
            print_explored_area(robot.mapaGlobal, robot.mapaLocal)
            exit(1)"""
