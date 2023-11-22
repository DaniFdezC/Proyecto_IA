import sys
import copy
import pygame
from CreadorMapa import convertirImagenAMatriz
from Casilla import *
from Robot import Robot

HEIGHT = 500
WIDTH = 750

GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Main:
    pass
    def __init__(self):
        self.ruta_imagen = "./Imagenes/mapaDefinitivo.png"
        self.matriz_resultante = convertirImagenAMatriz(self.ruta_imagen)
        self.matriz_resultante[3][98].tipoObjetivo = TipoObjetivo.LIBRE

        self.filas = len(self.matriz_resultante)
        self.columnas = len(self.matriz_resultante[0])

        self.tamano_casilla = 5
        self.iteraciones = 0

        self.niebla = self.mapa_vacio(self.filas, self.columnas)

        self.pantalla = pygame.display.set_mode((self.columnas*self.tamano_casilla, self.filas*self.tamano_casilla))
        pygame.display.set_caption("Matriz de Casillas")

        self.campoVision = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.robots = list()

        self.robot1 = Robot(self.matriz_resultante, (27, 27), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        self.robot2 = Robot(self.matriz_resultante, (7, 92), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        self.robot3 = Robot(self.matriz_resultante, (9, 147), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        self.robot4 = Robot(self.matriz_resultante, (43, 96), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        self.robot5 = Robot(self.matriz_resultante, (43, 98), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        self.robot6 = Robot(self.matriz_resultante, (78, 27), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        self.robot7 = Robot(self.matriz_resultante, (67, 94), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        self.robot8 = Robot(self.matriz_resultante, (97, 86), self.campoVision, self.niebla, self.pantalla, pygame, self.robots)
        
        self.robots.extend([self.robot1, self.robot2, self.robot3, self.robot4, self.robot5, self.robot6, self.robot7, self.robot8])
        
        #self.robots = [ self.robot3, self.robot4, self.robot5, self.robot6, self.robot7, self.robot8]

    def mapa_vacio(self, filas, columnas):
        return [[Casilla(TipoCasilla.NIEBLA) for _ in range(columnas)] for _ in range(filas)]

    def run(self):
        while True:
            for robot in self.robots:
                robot.moverse()
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()


            for i, fila in enumerate(self.niebla):
                for j, casilla in enumerate(fila):
                    if casilla.tipo is TipoCasilla.PARED:
                        color = BLACK
                    elif (i, j) == robot.coordenadas and self.matriz_resultante[i][j].tipoObjetivo is TipoObjetivo.LIBRE:
                        self.matriz_resultante[i][j].tipoObjetivo = TipoObjetivo.CAPTURADO
                        color = BLUE
                    elif (i, j) in map(lambda x: x.coordenadas, self.robots):
                        color = BLUE
                    elif casilla.tipoObjetivo is TipoObjetivo.LIBRE:
                        color = RED
                    elif casilla.tipo is TipoCasilla.NIEBLA:
                        color = GREY
                    elif casilla.tipoObjetivo is TipoObjetivo.CAPTURADO:
                        color = GREEN
                    elif casilla.tipo is TipoCasilla.VISITADO:
                        color = YELLOW
                    else:
                        color = WHITE

                    pygame.draw.rect(self.pantalla, color, (j * self.tamano_casilla, i * self.tamano_casilla, self.tamano_casilla, self.tamano_casilla))

                pygame.display.flip()
            self.iteraciones += 1
            print(self.iteraciones)

if __name__ == "__main__":
    main = Main()
    main.run()
