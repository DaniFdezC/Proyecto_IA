import math
import sys
import time

from CreadorMapa import convertirImagenAMatriz
from Robot import Robot
import matplotlib.pyplot as plt
import pygame
import numpy as np
from collections import deque
from Casilla import *
from typing import *

HEIGHT = 500
WIDTH = 750

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (105, 105, 105)


ruta_imagen = "./Imagenes/mapaDefinitivo.png"
mapaGlobal = convertirImagenAMatriz(ruta_imagen)

filas = len(mapaGlobal)
columnas = len(mapaGlobal[0])

tamano_casilla = 5
campo_vision = 20

pantalla = pygame.display.set_mode((columnas*tamano_casilla, filas*tamano_casilla))
pygame.display.set_caption("Matriz de Casillas")
vecinos = [(-1,-1), (-1, 0), (-1, 1), (0, 0), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]

radioVision = []
for i in range(-campo_vision, campo_vision):
    for j in range(-campo_vision, campo_vision, 1):
        # Evita agregar el punto (0, 0) a la lista de direcciones
        if (i, j) != (0, 0):
            # Calcula la distancia desde el punto central (0, 0) hasta el punto actual (i, j)
            distance = math.sqrt(i ** 2 + j ** 2)
            # Si la distancia es menor o igual al radio
            if distance < campo_vision:
                radioVision.append((i, j))

robot1 = Robot(mapaGlobal, (27, 27), radioVision)
robot2 = Robot(mapaGlobal, (92, 7), radioVision)
robot3 = Robot(mapaGlobal, (147, 9), radioVision)
robot4 = Robot(mapaGlobal, (96, 43), radioVision)
robot5 = Robot(mapaGlobal, (98, 43), radioVision)
robot6 = Robot(mapaGlobal, (27, 78), radioVision)
robot7 = Robot(mapaGlobal, (94, 67), radioVision)
robot8 = Robot(mapaGlobal, (86, 97), radioVision)

mapaGlobal[1][92].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[21][16].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[1][58].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[6][108].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[29][94].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[55][55].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[66][97].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[79][131].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[83][61].tipoObjetivo = TipoObjetivo.LIBRE
mapaGlobal[85][1].tipoObjetivo = TipoObjetivo.LIBRE

robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8]

iteraciones = 0
robotsAcabados = 0
nTotalRobots = len(robots)
contadorObjetivos = 0

while True:
    for robot in robots:
        if robot.moverse() is False:
            robots.remove(robot)
            robotsAcabados += 1

            if robotsAcabados == nTotalRobots:
                time.sleep(100)
                exit(1)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # Dibujar la matriz en la pantalla
        for y in range(len(mapaGlobal)):
            for x in range(len(mapaGlobal[y])):
                casilla = mapaGlobal[y][x]

                if casilla.tipo is TipoCasilla.PARED:
                    color = BLACK
                elif (x, y) == robot.coordenadas and mapaGlobal[y][x].tipoObjetivo is TipoObjetivo.LIBRE:
                    mapaGlobal[y][x].tipoObjetivo = TipoObjetivo.CAPTURADO
                    contadorObjetivos +=1
                    color = BLUE
                elif casilla.tipoObjetivo is TipoObjetivo.LIBRE:
                    color = RED
                elif casilla.tipoObjetivo is TipoObjetivo.CAPTURADO:
                    color=GREEN
                elif casilla.tipo is TipoCasilla.VISITADO or casilla.tipo is TipoCasilla.VISIONADA:
                    color = YELLOW
                else:
                    color = WHITE

                pygame.draw.rect(pantalla, color, (x * tamano_casilla, y * tamano_casilla, tamano_casilla, tamano_casilla))

        # Hacer que se pinten los robots en 3x3 
        for robot in robots:
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        pygame.draw.rect(pantalla, BLUE, (x+(robot.coordenadas[0]*tamano_casilla), y+(robot.coordenadas[1]*tamano_casilla), tamano_casilla, tamano_casilla))

        # Actualizar la pantalla
        pygame.display.flip()
    iteraciones += 1
    print(iteraciones)

    if contadorObjetivos == 10:
        print("Se han encontrado todos los objetivos")
        break
