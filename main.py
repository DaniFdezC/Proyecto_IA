import sys
from CreadorMapa import convertirImagenAMatriz
from Robot import Robot
import pygame
from Casilla import *

HEIGHT = 500
WIDTH = 750

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

rutaImagen = "Imagenes/mapaDefinitivo.png"
matrizResultante = convertirImagenAMatriz(rutaImagen)
matrizResultante[3][98].tipoObjetivo = TipoObjetivo.LIBRE

filas = len(matrizResultante)
columnas = len(matrizResultante[0])
tamano_casilla = 7

pantalla = pygame.display.set_mode((columnas*tamano_casilla, filas*tamano_casilla))
pygame.display.set_caption("Matriz de Casillas")

campoVision = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]

robot1 = Robot(matrizResultante, (27, 27), campoVision)
robot2 = Robot(matrizResultante, (7, 92), campoVision)
robot3 = Robot(matrizResultante, (9, 147), campoVision)
robot4 = Robot(matrizResultante, (43, 96), campoVision)
robot5 = Robot(matrizResultante, (43, 98), campoVision)
robot6 = Robot(matrizResultante, (78, 27), campoVision)
robot7 = Robot(matrizResultante, (67, 94), campoVision)
robot8 = Robot(matrizResultante, (97, 86), campoVision)

matrizResultante[1][92].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[21][16].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[1][58].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[6][108].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[29][94].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[55][55].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[66][97].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[79][131].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[83][61].tipoObjetivo = TipoObjetivo.LIBRE
matrizResultante[85][1].tipoObjetivo = TipoObjetivo.LIBRE

robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8]
iteraciones = 0
objetivosTotales = 10
contadorObjetivos = 0

while True:
    for robot in robots:
        if robot.moverse() is False:
            robots.remove(robot)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Limpiar la pantalla
        pantalla.fill((255, 255, 255))

        # Dibujar la matriz en la pantalla
        for i, fila in enumerate(matrizResultante):
            for j, casilla in enumerate(fila):

                if casilla.tipo is TipoCasilla.PARED:
                    color = BLACK
                elif (i, j) == robot.coordenadas and matrizResultante[i][j].tipoObjetivo is TipoObjetivo.LIBRE:
                    matrizResultante[i][j].tipoObjetivo = TipoObjetivo.CAPTURADO
                    contadorObjetivos += 1
                    color = BLUE
                elif (i, j) == robot.coordenadas:
                    color = BLUE
                elif casilla.tipoObjetivo is TipoObjetivo.LIBRE:
                    color = RED
                elif casilla.tipoObjetivo is TipoObjetivo.CAPTURADO:
                    color=GREEN
                elif casilla.tipo is TipoCasilla.VISITADO:
                    color = YELLOW
                else:
                    color = WHITE

                pygame.draw.rect(pantalla, color, (j * tamano_casilla, i * tamano_casilla, tamano_casilla, tamano_casilla))

        # Actualizar la pantalla
        pygame.display.flip()
        #time.sleep(0.1)
    if (contadorObjetivos >= objetivosTotales):
        break

    iteraciones += 1
    print(iteraciones)