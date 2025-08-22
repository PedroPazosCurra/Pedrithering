"""
    Proyecto personal de implementación de diferentes algoritmos de Dithering
    
    @author: pedropazoscurra
"""

from PIL import ImageOps
import numpy as np
import sys
from gestion_recursos import importar_imagen
from dithering import floyd_steinberg_dithering
from operaciones import a_greyscale, histograma, ecualizar_imagen


def probar_floyd_steinberg(nombre_imagen: str, num_grises : int):

    imagen = ImageOps.equalize(importar_imagen(nombre_imagen))
    imagen_dithered = floyd_steinberg_dithering(imagen, num_grises)
    imagen_dithered.show("Dither")


def main(num_grises : int = 2):

    imagen = a_greyscale(importar_imagen("minino_dormilon.jpg"))
    imagen_array = np.array(imagen)
    histograma1 = histograma(imagen)
    histograma2, _ = np.histogram(imagen_array.flatten(), 256, [0,256])
    assert(np.equal(histograma1, histograma2))

    imagen = ecualizar_imagen(importar_imagen("amiguito_adorable.jpg"))
    imagen.show()

    #imagen = importar_imagen("minino_dormilon.jpg")
    #imagen = importar_imagen("bestia_abominable.jpg")
    #imagen = ImageOps.equalize(importar_imagen("bestia_abominable.jpg"))

    #imagen_greyscale = a_greyscale(imagen)
    #imagen_cuantizada, _ = cuantizar_imagen(imagen_greyscale, num_grises)
    #imagen_dithered = floyd_steinberg_dithering(imagen, num_grises)

    #imagen_greyscale.show("greyscale")
    #imagen_cuantizada.show("cuantizada")
    #imagen_dithered.show("dither")


if __name__ == '__main__':
    sys.exit(main())