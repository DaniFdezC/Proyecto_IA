from PIL import Image

# Abre la imagen
imagen = Image.open("./Imagenes/mapaFinal.png")

# Convierte la imagen a blanco y negro
imagen_bn = imagen.convert("1")

# Guarda la imagen en blanco y negro
imagen_bn.save("./Imagenes/mapaDefinitivo.png")