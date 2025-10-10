"""
    Módulo que abstrae la obtención de recursos
    
    @author: pedropazoscurra
"""

from PIL import Image, ImageQt, ImageFile
import os, sys

def sugerir_archivo_coincidente(nombre_incompleto : str) -> str:
    """Dado un nombre de archivo parcial, sugiere un archivo completo que sí existe en /rsc"""

    # TODO: Implementación: Algoritmo de búsqueda de similaridad (¿cómo haré esto dios mio?) + printear << Hice esta suposicion: foo.png >>
    pass


def ruta_recursos(nombre_archivo : str) -> str:
    """Abstrae la obtención de la ruta de recursos"""
    try:
        ruta_base = sys._MEIPASS # type: ignore
    except Exception:
        ruta_base = os.path.abspath("./rsc")

    return os.path.join(ruta_base, nombre_archivo)


def ruta_imagen(nombre_archivo : str) -> str:
    """Abstrae la obtención de la ruta de las imagenes"""
    return os.path.join(ruta_recursos("./imagenes"), nombre_archivo)


def ruta_sonido(nombre_archivo : str) -> str:
    """Abstrae la obtención de la ruta de los sonidos"""
    return os.path.join(ruta_recursos("./sonidos"), nombre_archivo)


def importar_imagen(nombre_imagen : str) -> ImageFile.ImageFile:
    """Devuelve la imagen dado el nombre del archivo, buscándola en los recursos del programa"""

    ruta_recurso = ruta_imagen(nombre_imagen)
    
    try:
        return Image.open(ruta_recurso)
    except:
        raise Exception("Error accediendo a {}".format(ruta_recurso))
    

def importar_imagen_en_QImage(nombre_archivo : str, ratio_tamanho : float = 1.0):
    """Devuelve una QImage dado el nombre del archivo, buscando en los recursos del programa"""

    redimension_manteniendo_aspecto = lambda ratio, size: (round(ratio*size[0]), round(ratio*size[1])) # Funcion auxiliar float -> tuple -> tuple 
    
    imagen = importar_imagen(nombre_archivo).convert("RGBA")

    nuevo_tamanho = redimension_manteniendo_aspecto (ratio_tamanho, imagen.size)
    imagen = imagen.resize(nuevo_tamanho)

    return ImageQt.ImageQt(imagen)