from CreadorMapa import convertirImagenAMatriz
from Robot import Robot

ruta_imagen = "Imagenes/convertida.png"
matriz_resultante = convertirImagenAMatriz(ruta_imagen)

campoVision = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]

tortajeitor = Robot(matriz_resultante, (3,3), campoVision)
masieitor = Robot(matriz_resultante, (6,6), campoVision)

listaRobots = [tortajeitor, masieitor]

for robot in listaRobots:
    robot.moverse()