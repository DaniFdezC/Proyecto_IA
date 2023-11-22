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
    COMUNICATION_RADIUS = 10
    NEAR_FOG_THRESHOLD = 1

    def __init__(self, mapaGlobal, coordenadas, campoVision, niebla,pantalla , pygame, robots):
        self.robots = robots
        self.objetivos = []
        self.objetivos_ignorados = []
        
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
            self.comunicar()
            return
        
        if self.siguiendoAEstrella:
            self.seguirRuta()

        if self.siguiendoAEstrella is False:
            #Hay victima ? Ir a victima : Ir a niebla
            if len(self.objetivos) > 0:
                for objetivo in self.objetivos:
                    print("Objetivo: ", objetivo)
                    self.rutaAEstrella = astar(self.coordenadas, objetivo, self.mapaLocal, self.pygame, self.pantalla, "victima")
                    for (x, y) in self.rutaAEstrella:
                        self.pygame.draw.rect(self.pantalla, (0, 255, 0), (y * 5, x * 5, 5, 5))
                        self.pygame.display.flip()
                    if self.rutaAEstrella != None:
                        self.siguiendoAEstrella = True
                        break
                    else:
                        self.objetivos.pop(0)
                        self.objetivos_ignorados.extend(objetivo)
            else:
                self.find_nearest_fog()
                # Pintar puntos cercanos de amarillo
                for (x, y) in self.nearest_fog:
                    self.pygame.draw.rect(self.pantalla, (225, 255, 0), (y * 5, x * 5, 5, 5))
                    self.pygame.display.flip()
                self.explorar_niebla()
            
            if (self.rutaAEstrella != None and len(self.rutaAEstrella) > 0):
                self.seguirRuta()
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
                    if (self.mapaGlobal[i][j].tipo == TipoCasilla.VICTIMA and (i, j) not in self.objetivos):
                        self.objetivos.append((i, j))
                        print("Victima encontrada en ", (i, j), self.objetivos)
                        continue
                    elif (i, j) in self.nearest_fog:
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
                        
        nearest_fog.sort(key=lambda x: abs(x[0] - self.coordenadas[0]) + abs(x[1] - self.coordenadas[1]))
        if len(nearest_fog) > 30:
            print("Cuting down")
            # Filter nearest fog +1 higher tham min_distance
            # nearest_fog = list(filter(lambda x: abs(x[0] - robot_x) + abs(x[1] - robot_y) <= min_distance + 2, nearest_fog))
            # Use only the first half of the list
            nearest_fog = nearest_fog[:len(nearest_fog)//2]
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
       
    def explorar_niebla(self):
        while True:
            if not self.nearest_fog:
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
            self.rutaAEstrella = astar(self.coordenadas, niebla_mas_cercana, self.mapaLocal, self.pygame, self.pantalla, "explorar")
            if self.rutaAEstrella != None:
                # Sort nearest fog by distance
                self.siguiendoAEstrella = True
                break
        self.nearest_fog.extend(self.fog_buffer)
        self.fog_buffer = []

        
    def seguirRuta(self):
        self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.NADA
        self.mapaLocal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.NADA
        self.coordenadas = self.rutaAEstrella.pop(0)
        self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.ROBOT
        self.quitar_niebla()
        self.comunicar()
        if len(self.rutaAEstrella) == 0:
            if self.coordenadas in self.objetivos:
                self.objetivos.remove(self.coordenadas)
                self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.RESCATADO
            self.siguiendoAEstrella = False
            
    def comunicar(self):
        robot_x, robot_y = self.coordenadas
        vecinos = [self.coordenadas]
        # Comunicar con los robots cercanos en el radio de comunicacion
        for i in range(max(0, robot_x - self.COMUNICATION_RADIUS), min(self.alto, robot_x + self.COMUNICATION_RADIUS + 1)):
            for j in range(max(0, robot_y - self.COMUNICATION_RADIUS), min(self.ancho, robot_y + self.COMUNICATION_RADIUS + 1)):
                #if distance <= self.COMUNICATION_RADIUS:
                if self.mapaGlobal[i][j].tipo == TipoCasilla.ROBOT and (i, j) != self.coordenadas:
                    # Agregar a vecinos
                    vecinos.append((i, j))
        # Compartir mapa local
        if len(vecinos) > 1:
                #print("Vecinos: ",vecinos)
                self.compartir_con(vecinos)

    def compartir_con(self, vecinos):
        print("Compartiendo mapa con ", vecinos)
        mapa_compartido = self.mapa_vacio(self.alto, self.ancho)

        robots_vecinos = [self.buscar_robots_vecinos(vecino, self.robots) for vecino in vecinos]
        
        for i in range(self.alto):
            for j in range(self.ancho):
                for robot in robots_vecinos:
                    if robot.mapaLocal[i][j].tipo != TipoCasilla.NIEBLA:
                        mapa_compartido[i][j].tipo = self.mapaGlobal[i][j].tipo
                        break

        for robot in robots_vecinos:
            robot.mapaLocal = copy.deepcopy(mapa_compartido)

    def buscar_robots_vecinos(self, coordenadas, robots):
        for robot in robots:
            if robot.coordenadas == coordenadas:
                return robot
        return None
    
    def mapa_vacio(self, filas, columnas):
        return [[Casilla(TipoCasilla.NIEBLA) for _ in range(columnas)] for _ in range(filas)]