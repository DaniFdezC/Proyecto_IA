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


"""def print_explored_area(mapaGlobal, mapaLocal):
    
    for row in range(len(mapaGlobal)):
        for col in range(len(mapaGlobal[0])):
            if mapaLocal[row][col].tipo is TipoCasilla.VISITADO:
                print("V", end=" ")  # Visited
            else:
                print("X" if mapaGlobal[row][col].tipo == TipoCasilla.PARED else " ", end=" ")  # Wall or free space
        print()"""


ruta_imagen = "./Imagenes/mapaDefinitivo.png"
mapaGlobal = convertirImagenAMatriz(ruta_imagen)
mapaGlobal[3][98].tipoObjetivo = TipoObjetivo.LIBRE

filas = len(mapaGlobal)
columnas = len(mapaGlobal[0])

tamano_casilla = 5

pantalla = pygame.display.set_mode((columnas*tamano_casilla, filas*tamano_casilla))
pygame.display.set_caption("Matriz de Casillas")

campoVision = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]
campoVisionParaVerOtroRobot = 10

# robot1 = Robot(matriz_resultante, (27, 27), campoVision, niebla)
# robot2 = Robot(matriz_resultante, (7, 92), campoVision, niebla)
# robot3 = Robot(matriz_resultante, (9, 147), campoVision, niebla)
# robot4 = Robot(matriz_resultante, (43, 96), campoVision, niebla)
# robot5 = Robot(matriz_resultante, (43, 98), campoVision, niebla)
# robot6 = Robot(matriz_resultante, (78, 27), campoVision, niebla)
# robot7 = Robot(matriz_resultante, (67, 94), campoVision, niebla)
# robot8 = Robot(matriz_resultante, (97, 86), campoVision, niebla)

robot1 = Robot(mapaGlobal, (27, 27), campoVision)
robot2 = Robot(mapaGlobal, (92, 7), campoVision)
robot3 = Robot(mapaGlobal, (147, 9), campoVision)
robot4 = Robot(mapaGlobal, (96, 43), campoVision)
robot5 = Robot(mapaGlobal, (98, 43), campoVision)
robot6 = Robot(mapaGlobal, (27, 78), campoVision)
robot7 = Robot(mapaGlobal, (94, 67), campoVision)
robot8 = Robot(mapaGlobal, (86, 97), campoVision)

robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8]
# robots = [robot1]
iteraciones = 0
robotsAcabados = 0
nTotalRobots = len(robots)

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
        # Limpiar la pantalla
        pantalla.fill((255, 255, 255))

        # Dibujar la matriz en la pantalla
        for y in range(len(mapaGlobal)):
            for x in range(len(mapaGlobal[y])):
                casilla = mapaGlobal[y][x]

                if casilla.tipo is TipoCasilla.PARED:
                    color = BLACK
                elif (x, y) == robot.coordenadas and mapaGlobal[y][x].tipoObjetivo is TipoObjetivo.LIBRE:
                    mapaGlobal[y][x].tipoObjetivo = TipoObjetivo.CAPTURADO
                    color = BLUE
                elif (x, y) == robot.coordenadas:
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

                pygame.draw.rect(pantalla, color, (x * tamano_casilla, y * tamano_casilla, tamano_casilla, tamano_casilla))

        # Actualizar la pantalla
        pygame.display.flip()
        # time.sleep(0.1)
    iteraciones += 1
    print(iteraciones)

    robotsIntercambiadoMapas: Set[Tuple[Robot, Robot]] = set()

    for robot in robots:
        for otroRobot in robots:
            if ((robot, otroRobot) in robotsIntercambiadoMapas
                    or (otroRobot, robot) in robotsIntercambiadoMapas):
                continue

            distancia = abs(robot.coordenadas[0] - otroRobot.coordenadas[0]) + abs(robot.coordenadas[1] - otroRobot.coordenadas[1])
            if distancia <= campoVisionParaVerOtroRobot:
                otroRobot.intercambiarMapa(robot)
                robot.intercambiarMapa(robot)

                robotsIntercambiadoMapas.add((robot, otroRobot))
                robotsIntercambiadoMapas.add((otroRobot, otroRobot))


"""while True:
    for robot in robots:
        sePuedeMover = robot.moverse()
        if sePuedeMover is False:
            print_explored_area(robot.mapaGlobal, robot.mapaLocal)
            exit(1)"""
