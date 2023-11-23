from enum import Enum
import copy
import random
from Casilla import *
from Aestrella import *
class Robot:
    pass
    VIEWPORT_RADIUS = 20
    VIEWPORT_RADIUS_POW_2 = VIEWPORT_RADIUS ** 2
    
    COMUNICATION_RADIUS = 10
    UNIGNORE_COUTDOWN = 10

    def __init__(self, mapaGlobal, coordenadas, rescatados, niebla,pantalla , pygame, robots):
        self.robots = robots
        self.objetivos_conocidos = set()
        self.objetivos_rescatados = set()
        self.objetivos_ignorados = set()
        self.unignore_countdown = self.UNIGNORE_COUTDOWN
        
        self.mapaGlobal = mapaGlobal
        self.niebla = niebla
        self.rescatados_totales = rescatados
        self.coordenadas = coordenadas
        self.pantalla = pantalla
        self.pygame = pygame

        self.alto = len(mapaGlobal)
        self.ancho = len(mapaGlobal[0])

        self.mapaLocal = copy.deepcopy(niebla)
        self.nearest_fog = []
        self.fog_buffer = []
        self.siguiendoAEstrella = False
        self.rutaAEstrella = None
        self.quieto = False
        
        self.mapaGlobal[coordenadas[0]][coordenadas[1]].tipo = TipoCasilla.ROBOT

    def moverse(self):
        if self.quieto:
            self.comunicar()
            return

        self.find_nearest_fog()
        #Pintar puntos cercanos de amarillo
        # for (x, y) in self.nearest_fog:
        #     self.pygame.draw.rect(self.pantalla, (225, 255, 0), (y * 5, x * 5, 5, 5))
        #     self.pygame.display.flip()
            
        if self.siguiendoAEstrella:
            self.seguirRuta()
            return True
        #Hay victima ? Ir a victima : Ir a niebla
        if len(self.objetivos_conocidos) != len(self.objetivos_ignorados):
            for objetivo in self.objetivos_conocidos:
                print("Objetivo: ", objetivo)
                self.rutaAEstrella = astar(self.coordenadas, objetivo, self.mapaLocal, self.pygame, self.pantalla, "victima")
                if self.rutaAEstrella == None:
                    self.objetivos_ignorados.add(objetivo)
                else:
                    self.siguiendoAEstrella = True
                    break
        else:
            self.explorar_niebla()
        
        if (self.rutaAEstrella != None and len(self.rutaAEstrella) > 0):
            self.seguirRuta()
        return True

    # def pintar_ruta(self):
    #     for (x, y) in self.rutaAEstrella:
    #         self.pygame.draw.rect(self.pantalla, (0, 255, 0), (y * 5, x * 5, 5, 5))
    #         self.pygame.display.flip()

    def quitar_niebla(self):
        robot_x, robot_y = self.coordenadas
        
        self.evaluar_objetivos_ignorados()
        for i in range(max(0, robot_x - self.VIEWPORT_RADIUS), min(self.alto, robot_x + self.VIEWPORT_RADIUS + 1)):
            for j in range(max(0, robot_y - self.VIEWPORT_RADIUS), min(self.ancho, robot_y + self.VIEWPORT_RADIUS + 1)):
                distance = (i - robot_x) ** 2 + (j - robot_y) ** 2
                if distance <= self.VIEWPORT_RADIUS_POW_2:
                    #
                    if self.mapaLocal[i][j].tipo in [TipoCasilla.PARED, TipoCasilla.RESCATADO]:
                        continue
                    # 
                    self.niebla[i][j].tipo = self.mapaGlobal[i][j].tipo
                    self.mapaLocal[i][j].tipo = self.mapaGlobal[i][j].tipo
                    if (self.mapaGlobal[i][j].tipo == TipoCasilla.RESCATADO and (i, j) not in self.objetivos_rescatados):
                        if (i, j) in self.objetivos_conocidos:
                            self.objetivos_conocidos.remove((i, j))
                        self.objetivos_rescatados.add((i, j))
                        self.rescatados_totales.add((i, j))
                        continue
                    elif (self.mapaGlobal[i][j].tipo == TipoCasilla.VICTIMA and (i, j) not in self.objetivos_conocidos):
                        self.objetivos_conocidos.add((i, j))
                        print("Victima encontrada en ", (i, j), self.objetivos_conocidos)
                        continue
                    elif (i, j) in self.nearest_fog:
                        self.nearest_fog.remove((i, j))

    def evaluar_objetivos_ignorados(self):
        self.unignore_countdown -= 1
        if self.unignore_countdown == 0:
            self.objetivos_ignorados.clear()
            self.unignore_countdown = self.UNIGNORE_COUTDOWN

    def find_nearest_fog(self):
        robot_x, robot_y = self.coordenadas
        nearest_fog = []
        min_distance = float('inf')
        
        nearest_fog = self.Viewport_Check(robot_x, robot_y, nearest_fog, min_distance)
        self.nearest_fog.extend(nearest_fog)
        return

    def Viewport_Check(self, robot_x, robot_y, nearest_fog, min_distance):
        for i in range(max(0, robot_x - self.VIEWPORT_RADIUS), min(self.alto, robot_x + self.VIEWPORT_RADIUS + 1)):
            for j in range(max(0, robot_y - self.VIEWPORT_RADIUS), min(self.ancho, robot_y + self.VIEWPORT_RADIUS + 1)):
                if self.mapaLocal[i][j].tipo == TipoCasilla.NIEBLA:
                    distance = abs(i - robot_x) + abs(j - robot_y)
                    if distance <= min_distance+1:
                        min_distance = distance
                        nearest_fog.append((i, j))
                        
        nearest_fog.sort(key=lambda x: abs(x[0] - self.coordenadas[0]) + abs(x[1] - self.coordenadas[1]))
        if len(nearest_fog) > 80:
            #print("Cuting down")
            nearest_fog = nearest_fog[:len(nearest_fog)//5]
        return nearest_fog
       
    def explorar_niebla(self):
        while True:
            if not self.nearest_fog:
                self.quieto = True
                return
            niebla_mas_cercana = self.nearest_fog.pop(random.randint(0, len(self.nearest_fog)-1))
            #niebla_mas_cercana = self.nearest_fog.pop(-1)
            self.fog_buffer.append(niebla_mas_cercana)
            if (self.coordenadas in self.nearest_fog):
                self.nearest_fog = []
                self.fog_buffer = []
                self.rutaAEstrella = [self.coordenadas]
                break
            # Pintar punto de niebla mas cercano de color
            # self.pygame.draw.rect(self.pantalla, (0, 255, 255), (niebla_mas_cercana[1] * 5, niebla_mas_cercana[0] * 5, 5, 5))
            # self.pygame.display.flip()
            self.rutaAEstrella = astar(self.coordenadas, niebla_mas_cercana, self.mapaLocal, self.pygame, self.pantalla, "explorar")
            if self.rutaAEstrella != None:
                self.siguiendoAEstrella = True
                break                
        self.nearest_fog.extend(self.fog_buffer)
        self.fog_buffer = []

        
    def seguirRuta(self):
        self.comprobar_rescate()
        self.coordenadas = self.rutaAEstrella.pop(0)
        if (self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo not in [TipoCasilla.RESCATADO, TipoCasilla.VICTIMA]):
            self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.ROBOT
        self.quitar_niebla()
        self.comunicar()
        if len(self.rutaAEstrella) == 0:
            self.siguiendoAEstrella = False

    def comprobar_rescate(self):
        if self.coordenadas in self.objetivos_conocidos:
            self.objetivos_conocidos.remove(self.coordenadas)
            self.objetivos_rescatados.add(self.coordenadas)
            self.rescatados_totales.add(self.coordenadas)
            self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.RESCATADO
            self.mapaLocal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.RESCATADO
        elif self.coordenadas in self.objetivos_rescatados:
            self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.RESCATADO
            self.mapaLocal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.RESCATADO
        else:
            self.mapaGlobal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.NADA
            self.mapaLocal[self.coordenadas[0]][self.coordenadas[1]].tipo = TipoCasilla.NADA
        # Evitar que busque un punto ya rescatado
        if self.rutaAEstrella[-1] in self.objetivos_rescatados:
            self.rutaAEstrella = [self.coordenadas] 
            
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
        objetivos_compartidos = set()
        objetivos_salvados = set()
        robots_vecinos = []
        niebla_cercana = []
        
        for vecino in vecinos:
            robot_vecino = self.buscar_robots_vecinos(vecino, self.robots)
            objetivos_salvados.update(robot_vecino.objetivos_rescatados)
            objetivos_compartidos.update(robot_vecino.objetivos_conocidos.difference(objetivos_salvados))
            niebla_cercana.extend(robot_vecino.nearest_fog)
            robots_vecinos.append(robot_vecino)
        
        for i in range(self.alto):
            for j in range(self.ancho):
                for robot in robots_vecinos:
                    if robot.mapaLocal[i][j].tipo != TipoCasilla.NIEBLA:
                        mapa_compartido[i][j].tipo = self.mapaGlobal[i][j].tipo
                        if (i, j) in niebla_cercana:
                            niebla_cercana.remove((i, j))
                        break

        for robot in robots_vecinos:
            robot.mapaLocal = copy.deepcopy(mapa_compartido)
            robot.niebla_cercana = copy.deepcopy(niebla_cercana)                
            robot.objetivos_conocidos.update(objetivos_compartidos)
            robot.objetivos_rescatados.update(objetivos_salvados)

    def buscar_robots_vecinos(self, coordenadas, robots):
        for robot in robots:
            if robot.coordenadas == coordenadas:
                return robot
        return None
    
    def mapa_vacio(self, filas, columnas):
        return [[Casilla(TipoCasilla.NIEBLA) for _ in range(columnas)] for _ in range(filas)]