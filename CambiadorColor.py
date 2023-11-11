from PIL import Image

# Abre la imagen
imagen = Image.open("Imagenes/mapa.PNG")

# Convierte la imagen a blanco y negro
imagen_bn = imagen.convert("1")

# Guarda la imagen en blanco y negro
imagen_bn.save("../Imagenes/convertida.png")