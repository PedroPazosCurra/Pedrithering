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

    # print("{} , {}   ->   {}".format(valor_sin_cuantizar, valor_cuantizado, error_cuantizacion))

    return valor_cuantizado, error_cuantizacion


def cuantizar_imagen(imagen, num_niveles_negro : int = 2) -> tuple[Image.Image, np.ndarray]:

    imagen_array = np.array(imagen)
    array_errores_cuantizacion = np.zeros([imagen_array.shape[0], imagen_array.shape[1]])

    for i, fila in enumerate(imagen_array):
        for j, valor_gris_sin_cuantizar in enumerate(fila):

            valor_gris_cuantizado, error_cuantizacion = encuentra_valor_paleta_proximo(valor_gris_sin_cuantizar, num_niveles_negro)
            
            imagen_array[i,j] = valor_gris_cuantizado
            array_errores_cuantizacion[i,j] = error_cuantizacion

    imagen_salida = Image.fromarray(imagen_array)
    
    return imagen_salida, array_errores_cuantizacion


def grayscale(imagen) -> Image.Image:
    """Convierte una imagen dada a escala de grises."""

    imagen_array = np.array(imagen)
    imagen_grayscale = np.zeros([imagen_array.shape[0], imagen_array.shape[1]])

    for i, fila in enumerate(imagen_array):
        for j, pixel in enumerate(fila):

            valor_gris = round(np.sum(pixel) / 3)
            
            imagen_grayscale[i,j] = valor_gris

    imagen_salida = Image.fromarray(imagen_grayscale)
    
    return imagen_salida


def floyd_steinberg_dithering(imagen, num_niveles_negro : int = 2):

    imagen_grayscale = grayscale(imagen)
    imagen_cuantizada_array = np.array(imagen_grayscale)

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
    
    #imagen = ImageOps.equalize(importar_imagen("amiguito_adorable.jpg"))
    #imagen = importar_imagen("minino_dormilon.jpg")
    #imagen = importar_imagen("bestia_abominable.jpg")

    imagen = ImageOps.equalize(importar_imagen(nombre_imagen))

    #imagen_grayscale = grayscale(imagen)
    #imagen_cuantizada, _ = cuantizar_imagen(imagen_grayscale, num_grises)
    imagen_dithered = floyd_steinberg_dithering(imagen, num_grises)

    #imagen_grayscale.show("greyscale")
    #imagen_cuantizada.show("cuantizada")
    imagen_dithered.show("dither")


def main(num_grises : int = 2):

    imagen = ImageOps.equalize(importar_imagen("amiguito_adorable.jpg"))
    #imagen = importar_imagen("minino_dormilon.jpg")
    #imagen = importar_imagen("bestia_abominable.jpg")
    #imagen = ImageOps.equalize(importar_imagen("bestia_abominable.jpg"))

    #imagen_grayscale = grayscale(imagen)
    #imagen_cuantizada, _ = cuantizar_imagen(imagen_grayscale, num_grises)
    imagen_dithered = floyd_steinberg_dithering(imagen, num_grises)

    #imagen_grayscale.show("greyscale")
    #imagen_cuantizada.show("cuantizada")
    imagen_dithered.show("dither")


if __name__ == '__main__':
    sys.exit(main())