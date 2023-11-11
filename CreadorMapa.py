from PIL import Image
from Casilla import Casilla


def convertirImagenAMatriz(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen)
        # Convertir la imagen a escala de grises
        imagen_gris = imagen.convert('L')
        # Obtener los píxeles como una secuencia de valores
        valores_pixeles = list(imagen_gris.getdata())

        # Obtener las dimensiones de la imagen
        ancho, alto = imagen_gris.size

        # Crear la matriz
        matriz = [valores_pixeles[i:i+ancho] for i in range(0, len(valores_pixeles), ancho)]

        # Convertir valores a 0 (blanco) o 1 (negro)
        matriz_binaria = [[Casilla(False, 0, None) if valor == 255 else Casilla(False, 1, None) for valor in fila] for fila in matriz]

        return matriz_binaria

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None
