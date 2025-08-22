"""
    Modulo que alberga implementaciones de las operaciones auxiliares necesarias para los algoritmos realizados. 

    @author: pedropazoscurra
"""

from PIL import Image
import numpy as np

def encuentra_valor_paleta_proximo(valor_sin_cuantizar, num_niveles_negro : int, valor_inferior : int = 0, valor_superior : int = 255) -> tuple[int,int]:
    """Dado un pixel en greyscale, encuentra el valor de gris mas proximo en la escala de grises conformada por un numero de grises dado"""

    # Entre max y min
    valor_sin_cuantizar = max(valor_inferior, min(valor_superior, valor_sin_cuantizar))

    umbral_nivel_gris = valor_superior / num_niveles_negro
    paso_nivel = valor_superior / (num_niveles_negro-1)

    nivel_correspondiente = round(valor_sin_cuantizar / umbral_nivel_gris) 
    valor_cuantizado = round(paso_nivel * nivel_correspondiente)

    error_cuantizacion = valor_sin_cuantizar - valor_cuantizado

    return valor_cuantizado, error_cuantizacion


def cuantizar_imagen(imagen : Image.Image, num_niveles_negro : int = 2) -> tuple[Image.Image, np.ndarray]:
    """Dada una imagen, comprime la paleta de grises"""

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
    """Ecualiza el histograma de una imagen

    Notas
    ------------
    Por ahora, ten en cuenta que convierte la imagen dada en greyscale.
    """

    imagen_array = np.array(imagen.convert('L'))
    imagen_ecualizada_array = np.zeros_like(imagen_array)
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


def a_greyscale(imagen : Image.Image) -> Image.Image:
    """Convierte una imagen dada a escala de grises."""

    imagen_array = np.array(imagen)
    imagen_greyscale = np.zeros([imagen_array.shape[0], imagen_array.shape[1]])

    for i, fila in enumerate(imagen_array):
        for j, pixel in enumerate(fila):

            valor_gris = round(np.sum(pixel) / 3)
            
            imagen_greyscale[i,j] = valor_gris

    imagen_salida = Image.fromarray(imagen_greyscale)
    return imagen_salida