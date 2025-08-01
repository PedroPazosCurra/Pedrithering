"""
    Proyecto personal de implementación de diferentes algoritmos de Dithering
    
    @author: pedropazoscurra
"""

from PIL import Image, ImageOps
import numpy as np
import os
import sys
import math
from gestion_recursos import importar_imagen


def encuentra_valor_paleta_proximo(valor_sin_cuantizar, num_niveles_negro : int) -> tuple[int,int]:
    """Encuentra el valor mas proximo de un valor de gris en la escala de grises conformada por un numero de grises dado"""

    # Entre 0 y 255
    valor_sin_cuantizar = max(0, min(255, valor_sin_cuantizar))

    umbral_nivel_gris = 255 / num_niveles_negro
    paso_nivel = 255 / (num_niveles_negro-1)

    nivel_correspondiente = round(valor_sin_cuantizar / umbral_nivel_gris) 
    valor_cuantizado = round(paso_nivel * nivel_correspondiente)

    error_cuantizacion = valor_sin_cuantizar - valor_cuantizado

    return valor_cuantizado, error_cuantizacion


def cuantizar_imagen(imagen : Image.Image, num_niveles_negro : int = 2) -> tuple[Image.Image, np.ndarray]:

    imagen_array = np.array(imagen)
    array_errores_cuantizacion = np.zeros([imagen_array.shape[0], imagen_array.shape[1]])

    for i, fila in enumerate(imagen_array):
        for j, valor_gris_sin_cuantizar in enumerate(fila):

            valor_gris_cuantizado, error_cuantizacion = encuentra_valor_paleta_proximo(valor_gris_sin_cuantizar, num_niveles_negro)
            
            imagen_array[i,j] = valor_gris_cuantizado
            array_errores_cuantizacion[i,j] = error_cuantizacion

    imagen_salida = Image.fromarray(imagen_array)
    
    return imagen_salida, array_errores_cuantizacion


def histograma(imagen : Image.Image):
    """Devuelve el histograma y los binarios de una imagen dada"""

    assert(isinstance(imagen, Image.Image))

    imagen_array = np.array(imagen)

    try:
        histograma = np.zeros((imagen_array.shape[2], 256))
    except:
        histograma = np.zeros((256))

    for num_fila in range(imagen_array.shape[0]):
        for num_columna in range(imagen_array.shape[1]):

            pixel = imagen_array[num_fila, num_columna]

            try: 
                for canal, valor in enumerate(pixel):
                        histograma[canal, valor] += 1

            except:
                histograma[round(pixel)] += 1

    return histograma


def ecualizar_imagen(imagen : Image.Image) -> Image.Image:
    """Ecualiza una imagen

    Notas
    ------------
    Por ahora, convierte en greyscale. Ten en cuenta que convierte la imagen en greyscale.
    """

    imagen_array = np.array(imagen.convert('L'))
    imagen_ecualizada_array = np.zeros_like(imagen_array)

    # TODO: Implementar yo mismo la funcion de histograma
    histograma_original = histograma(imagen)

    # Calculo de sumatorio acumulativo
    cumsum = np.cumsum(histograma_original)

    # Algoritmo de ecualizacion
    cumsum_masked = np.ma.masked_equal(cumsum, 0)     
    cumsum_masked = (cumsum_masked - cumsum_masked.min())*255 / (cumsum_masked.max() - cumsum_masked.min()) 
    cumsum = np.ma.filled(cumsum_masked, 0).astype('uint8')

    # Listo, tenemos un mapa/aplicación Img. Original -> Img. Ecualizada
    imagen_ecualizada_array = cumsum[imagen_array]
    imagen_salida = Image.fromarray(imagen_ecualizada_array)
    return imagen_salida


def greyscale(imagen : Image.Image) -> Image.Image:
    """Convierte una imagen dada a escala de grises."""

    imagen_array = np.array(imagen)
    imagen_greyscale = np.zeros([imagen_array.shape[0], imagen_array.shape[1]])

    for i, fila in enumerate(imagen_array):
        for j, pixel in enumerate(fila):

            valor_gris = round(np.sum(pixel) / 3)
            
            imagen_greyscale[i,j] = valor_gris

    imagen_salida = Image.fromarray(imagen_greyscale)
    return imagen_salida


def floyd_steinberg_dithering(imagen : Image.Image, num_niveles_negro : int = 2):

    assert(isinstance(imagen, Image.Image))
    assert(isinstance(num_niveles_negro, int))
    assert num_niveles_negro > 0, "El numero de grises de la escala debe ser igual o mayores que 1."

    imagen_greyscale = greyscale(imagen)
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


def probar_floyd_steinberg(nombre_imagen: str, num_grises : int):

    imagen = ImageOps.equalize(importar_imagen(nombre_imagen))
    imagen_dithered = floyd_steinberg_dithering(imagen, num_grises)
    imagen_dithered.show("dither")


def main(num_grises : int = 2):

    imagen = greyscale(importar_imagen("minino_dormilon.jpg"))
    imagen_array = np.array(imagen)
    histograma1 = histograma(imagen)
    histograma2, _ = np.histogram(imagen_array.flatten(), 256, [0,256])
    assert(np.equal(histograma1, histograma2))

    imagen = ecualizar_imagen(importar_imagen("amiguito_adorable.jpg"))
    imagen.show()

    #imagen = importar_imagen("minino_dormilon.jpg")
    #imagen = importar_imagen("bestia_abominable.jpg")
    #imagen = ImageOps.equalize(importar_imagen("bestia_abominable.jpg"))

    #imagen_greyscale = greyscale(imagen)
    #imagen_cuantizada, _ = cuantizar_imagen(imagen_greyscale, num_grises)
    #imagen_dithered = floyd_steinberg_dithering(imagen, num_grises)

    #imagen_greyscale.show("greyscale")
    #imagen_cuantizada.show("cuantizada")
    #imagen_dithered.show("dither")


if __name__ == '__main__':
    sys.exit(main())