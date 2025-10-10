"""
    Modulo que alberga implementaciones de los algoritmos de dithering. 

    @author: pedropazoscurra
"""

from PIL import Image
import numpy as np
from src.operaciones import a_greyscale, encuentra_valor_paleta_proximo, cuantizar_imagen

def floyd_steinberg_dithering(imagen : Image.Image, num_niveles_negro : int = 2):
    """Algoritmo de dithering Floyd-Steinberg, que propaga el error de cuantización a razón de 7/16, 5/16, 3/16 y 1/15 según la posición del pixel en orden de iteración"""

    assert(isinstance(imagen, Image.Image))
    assert(isinstance(num_niveles_negro, int))
    assert num_niveles_negro > 0, "El numero de grises de la escala debe ser igual o mayores que 1."

    imagen_greyscale = a_greyscale(imagen)
    imagen_cuantizada_array = np.array(imagen_greyscale)

    num_filas, num_columnas = imagen_cuantizada_array.shape

    imagen_dithered = np.zeros([num_filas, num_columnas])

    for i in range(num_filas):
        for j in range(num_columnas):

            if (i in range(1, num_filas-2)) and (j in range(1, num_columnas-2)): 

                pixel_cuantizado, error_cuantizacion = encuentra_valor_paleta_proximo(imagen_dithered[i,j], num_niveles_negro)
                imagen_dithered[i,j] = pixel_cuantizado

                imagen_dithered[i,j+1] = imagen_cuantizada_array[i,j+1] + (error_cuantizacion * (7/16))
                imagen_dithered[i+1,j+1] = imagen_cuantizada_array[i+1,j+1] + (error_cuantizacion * (1/16))
                imagen_dithered[i+1,j] = imagen_cuantizada_array[i+1,j] + (error_cuantizacion * (5/16))
                imagen_dithered[i+1,j-1] = imagen_cuantizada_array[i+1,j-1] + (error_cuantizacion * (3/16))

    imagen_dithered, _ = cuantizar_imagen(Image.fromarray(imagen_dithered), num_niveles_negro)

    return imagen_dithered


def dithering_ordenado(imagen : Image.Image, num_niveles_negro : int = 2):

    assert(isinstance(imagen, Image.Image))
    assert(isinstance(num_niveles_negro, int))
    assert num_niveles_negro > 0, "El numero de grises de la escala debe ser igual o mayores que 1."

    imagen_greyscale = a_greyscale(imagen)
    imagen_cuantizada_array = np.array(imagen_greyscale)

    num_filas, num_columnas = imagen_cuantizada_array.shape

    imagen_dithered = np.zeros([num_filas, num_columnas])

    # TODO: Algoritmo

    return imagen_dithered