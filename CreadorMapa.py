from PIL import Image
import numpy as np
from Casilla import *



# def convertirImagenAMatriz(ruta_imagen):
#     try:
#         imagen = Image.open(ruta_imagen)
#         # Convertir la imagen a escala de grises
#         imagen_gris = imagen.convert('L')
#         # Obtener los píxeles como una secuencia de valores
#         valores_pixeles = list(imagen_gris.getdata())

#         # Obtener las dimensiones de la imagen
#         ancho, alto = rgb_im.size

#         # Crear la matriz
#         matriz = [valores_pixeles[i:i+ancho] for i in range(0, len(valores_pixeles), ancho)]

#         # Convertir valores a 0 (blanco) o 1 (negro)
#         matriz_binaria = [[Casilla(TipoCasilla.NADA) if valor == 255 else Casilla(TipoCasilla.PARED) for valor in fila] for fila in matriz]

#         return matriz_binaria

#     except Exception as e:
#         print(f"Error al procesar la imagen: {e}")
#         return None


def convertirImagenAMatriz(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen)
        rgb_im = imagen.convert('RGB')
        # Obtener los píxeles como una secuencia de valores (RGB)
        valores_pixeles = list(rgb_im.getdata())

        # Obtener las dimensiones de la imagen
        ancho, alto = imagen.size

        # Crear la matriz
        matriz = [valores_pixeles[i:i+ancho] for i in range(0, len(valores_pixeles), ancho)]

        # Convertir valores a TipoCasilla basado en los colores
        matriz_resultante = []
        for i in range(0, len(matriz)):
            nueva_fila = []
            for j in range(0, len(matriz[0])):
                # Obtener los valores RGB del píxel
                r, g, b = rgb_im.getpixel((j, i))
                # Asignar TipoCasilla según el color
                if (r, g, b) == (255, 255, 255):  # Blanco
                    nueva_fila.append(Casilla(TipoCasilla.NADA))
                elif (r, g, b) == (0, 0, 0):  # Negro
                    nueva_fila.append(Casilla(TipoCasilla.PARED))
                elif (r, g, b) == (255, 0, 0):  # Azul (Victima)
                    nueva_fila.append(Casilla(TipoCasilla.VICTIMA))
                else:
                    # Otros colores (tratar como PARED por defecto o manejar según necesidad)
                    nueva_fila.append(Casilla(TipoCasilla.PARED))  
            matriz_resultante.append(nueva_fila)

        return matriz_resultante

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None
