from enum import Enum
import copy
import random
from Casilla import *
from Algoritmo import *
from collections import deque
import numpy as np
from Aestrella import *


class Robot:
    pass
    VIEWPORT_RADIUS = 20
    COMUNICATION_RADIUS = 20
    NEAR_FOG_THRESHOLD = 1

    def __init__(self, mapaGlobal, coordenadas, campoVision, niebla,pantalla , pygame, robots):
        self.robots = robots
        
        self.mapaGlobal = mapaGlobal
        self.niebla = niebla
        self.campoVision = campoVision
        self.coordenadas = coordenadas
        self.pantalla = pantalla
        self.pygame = pygame

        self.alto = len(mapaGlobal)
        self.ancho = len(mapaGlobal[0])

        #self.mapaLocal =[[Casilla() for _ in range(self.ancho)] for _ in range(self.alto)]
        self.mapaLocal = copy.deepcopy(niebla)
        self.nearest_fog = []
        self.fog_buffer = []
        self.bfsQueue = deque([coordenadas])
        self.siguiendoAEstrella = False
        self.rutaAEstrella = None
        self.quieto = False
        
        self.mapaGlobal[coordenadas[0]][coordenadas[1]].tipo = TipoCasilla.ROBOT
        
        

    def moverse(self):
        if self.quieto:
            #self.comunicar()
            return
        
        if self.siguiendoAEstrella:
            self.seguirRuta()

        if self.siguiendoAEstrella is False:
        # Hay victima ? Ir a victima : Ir a niebla
        # if self.mapaLocal[self.coordenadas[0]][self.coordenadas[1]].tipoObjetivo is TipoObjetivo.LIBRE:
        #     self.rutaAEstrella = astar(self.coordenadas, self.find_nearest_fog(), self.mapaLocal)
        #     self.siguiendoAEstrella = True
        # else:
        
            self.find_nearest_fog()
            # Pintar puntos cercanos de amarillo
            for (x, y) in self.nearest_fog:
                self.pygame.draw.rect(self.pantalla, (225, 255, 0), (y * 5, x * 5, 5, 5))
                self.pygame.display.flip()
            
            # Do (find A* path to nearest fog) while A* path is empty
            while True:
                # if not self.nearest_fog:
                #     print("No hay niebla")
                #     self.find_nearest_fog(2)
                if not self.nearest_fog:
                  #  print("No hay niebla")
                    self.quieto = True
                    return
                niebla_mas_cercana = self.nearest_fog.pop(random.randint(0, len(self.nearest_fog)-1))
                self.fog_buffer.append(niebla_mas_cercana)
                if (self.coordenadas in self.nearest_fog):
                    self.nearest_fog = []
                    self.fog_buffer = []
                    self.rutaAEstrella = [self.coordenadas]
                    break
                # Pintar punto de niebla mas cercano de verde
                self.pygame.draw.rect(self.pantalla, (0, 255, 0), (niebla_mas_cercana[1] * 5, niebla_mas_cercana[0] * 5, 5, 5))
                self.pygame.display.flip()
                self.rutaAEstrella = astar(self.coordenadas, niebla_mas_cercana, self.mapaLocal, self.pygame, self.pantalla, "victim")
                if self.rutaAEstrella != None:
                    break
            self.nearest_fog.extend(self.fog_buffer)
            self.fog_buffer = []
            # Sort nearest fog by distance
            self.nearest_fog.sort(key=lambda x: abs(x[0] - self.coordenadas[0]) + abs(x[1] - self.coordenadas[1]))
            self.siguiendoAEstrella = True
            self.seguirRuta()
            
        

        
            # if not self.bfsQueue:
            #     return False

            # # Ir haciendo pop hasta que encontremos uno que almenos 1 vecino no este visitado.
            # current_row, current_col = self.bfsQueue.pop()
            # neighbors = [(current_row - 1, current_col), (current_row + 1, current_col),
            #              (current_row, current_col - 1), (current_row, current_col + 1),
            #              (current_row - 1, current_col - 1), (current_row + 1, current_col + 1),
            #              (current_row - 1, current_col +1), (current_row + 1, current_col -1)]

            # if self.mePuedoMoverSinDarSaltos(current_row, current_col):
            #     self.coordenadas = (current_row, current_col)
            # else:
            #     self.rutaAEstrella = astar(self.coordenadas, (current_row, current_col), self.mapaLocal)
            #     self.siguiendoAEstrella = True


            # for neighbor_row, neighbor_col in neighbors:
            #     if self.is_valid_move(neighbor_row, neighbor_col):
            #         self.bfsQueue.append((neighbor_row, neighbor_col))

            #         self.mapaLocal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO
            #         self.mapaGlobal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO
            #         self.quitar_niebla()

            return True

    def mePuedoMoverSinDarSaltos(self, nuevaX, nuevaY):
        difX = abs(self.coordenadas[0] - nuevaX)
        difY = abs(self.coordenadas[1] - nuevaY)

        return difY < 2 and difX < 2

    def is_valid_move(self, row, col):
        rows, cols = self.alto, self.ancho

        # TODO Simplificar
        dentroDeLosLimites = 0 <= row < rows and 0 <= col < cols
        noHayPared = self.mapaGlobal[row][col].tipo is TipoCasilla.NADA
        noLoHeVisitado = self.mapaLocal[row][col].tipo is not TipoCasilla.VISITADO

        return dentroDeLosLimites and noHayPared and noLoHeVisitado
    
    def quitar_niebla(self):
        robot_x, robot_y = self.coordenadas
        
        for i in range(max(0, robot_x - self.VIEWPORT_RADIUS), min(self.alto, robot_x + self.VIEWPORT_RADIUS + 1)):
            for j in range(max(0, robot_y - self.VIEWPORT_RADIUS), min(self.ancho, robot_y + self.VIEWPORT_RADIUS + 1)):
                distance = np.sqrt((i - robot_x) ** 2 + (j - robot_y) ** 2)
                if distance <= self.VIEWPORT_RADIUS:
                    self.niebla[i][j].tipo = self.mapaGlobal[i][j].tipo
                    self.mapaLocal[i][j].tipo = self.mapaGlobal[i][j].tipo
                    if (i, j) in self.nearest_fog:
                        self.nearest_fog.remove((i, j))

    def find_nearest_fog(self, scale = 1):
        robot_x, robot_y = self.coordenadas
        nearest_fog = []
        min_distance = float('inf')
                        
        if scale == 1:
            nearest_fog = self.Viewport_Check(robot_x, robot_y, nearest_fog, min_distance)
            #print("nearest_fog", nearest_fog)
            
        else:
            nearest_fog = self.Wide_Check(robot_x, robot_y, nearest_fog, min_distance, scale)
        
        self.nearest_fog.extend(nearest_fog)
        return

    def Viewport_Check(self, robot_x, robot_y, nearest_fog, min_distance):
        for i in range(max(0, robot_x - self.VIEWPORT_RADIUS-2), min(self.alto, robot_x + self.VIEWPORT_RADIUS+2 + 1)):
            for j in range(max(0, robot_y - self.VIEWPORT_RADIUS-2), min(self.ancho, robot_y + self.VIEWPORT_RADIUS+2 + 1)):
                if self.mapaLocal[i][j].tipo == TipoCasilla.NIEBLA:
                    distance = abs(i - robot_x) + abs(j - robot_y)
                    if distance <= min_distance+1:
                        min_distance = distance
                        nearest_fog.append((i, j))
        if len(nearest_fog) > 10:
            print("Cuting down")
            # Filter nearest fog +1 higher tham min_distance
            nearest_fog = list(filter(lambda x: abs(x[0] - robot_x) + abs(x[1] - robot_y) <= min_distance, nearest_fog))
        return nearest_fog
    
    # def Wide_Check(self, robot_x, robot_y, nearest_fog, min_distance, scale):
    #     for i in range(max(0, robot_x - (self.VIEWPORT_RADIUS * scale)), min(self.alto, robot_x + (self.VIEWPORT_RADIUS * scale) + 1)):
    #         for j in range(max(0, robot_y - (self.VIEWPORT_RADIUS * scale)), min(self.ancho, robot_y + (self.VIEWPORT_RADIUS * scale) + 1)):
    #             if self.mapaLocal[i][j].tipo == TipoCasilla.NIEBLA:
    #                 distance = abs(i - robot_x) + abs(j - robot_y)
    #                 if distance <= min_distance + scale:
    #                     min_distance = distance
    #                     nearest_fog.append((i, j))
    #     return nearest_fog
        
    def seguirRuta(self):
        self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.NADA
        self.coordenadas = self.rutaAEstrella.pop(0)
        self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.ROBOT
        self.quitar_niebla()
       # self.comunicar()
        if len(self.rutaAEstrella) == 0:
            self.siguiendoAEstrella = False
            
    def comunicar(self):
        robot_x, robot_y = self.coordenadas
        vecinos = [self.coordenadas]
        # Comunicar con los robots cercanos en el radio de comunicacion
        for i in range(max(0, robot_x - self.COMUNICATION_RADIUS), min(self.alto, robot_x + self.COMUNICATION_RADIUS + 1)):
            for j in range(max(0, robot_y - self.COMUNICATION_RADIUS), min(self.ancho, robot_y + self.COMUNICATION_RADIUS + 1)):
                distance = np.sqrt((i - robot_x) ** 2 + (j - robot_y) ** 2)
                if distance <= self.COMUNICATION_RADIUS:
                    # Agregar a vecinos
                    vecinos.append((i, j))
        # Compartir mapa local
        self.compartir_con(vecinos)
                    
# from main import compartir_con
    def compartir_con(self, vecinos):
        print("Compartiendo mapa con ", vecinos)
        mapa_compartido = self.mapa_vacio(self.alto, self.ancho)

        robots_vecinos = map(lambda vecino: self.buscar_robot_por_coordenadas(vecino, self.robots).mapaLocal, vecinos)

        for i in range(self.alto):
            for j in range(self.ancho):
                tiene_diferente_a_niebla = False
                for robot in robots_vecinos:
                    if robot.mapaLocal[i][j].tipo != TipoCasilla.NIEBLA:
                        tiene_diferente_a_niebla = True
                        break

                if tiene_diferente_a_niebla:
                    mapa_compartido[i][j].tipo = self.matriz_resultante[i][j].tipo

        for vecino in vecinos:
            vecino.mapaLocal = copy.deepcopy(mapa_compartido)

    def buscar_robot_por_coordenadas(self, coordenadas, robots):
        for robot in robots:
            if robot.coordenadas == coordenadas:
                return robot
        return None
    
    def mapa_vacio(self, filas, columnas):
        return [[Casilla(TipoCasilla.NIEBLA) for _ in range(columnas)] for _ in range(filas)]