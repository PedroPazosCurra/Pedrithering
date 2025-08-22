"""
    Módulo que abstrae la obtención de recursos
    
    @author: pedropazoscurra
"""
# TODO: Anhadir funcion que se encargue de comprobar extensión y añadir una en caso de no haberla + printear << Hice esta suposicion: foo.png >>

from PIL import Image, ImageQt
import os, sys

def ruta_recursos(nombre_archivo : str) -> str:
    """Abstrae la obtención de la ruta de recursos"""
    try:
        ruta_base = sys._MEIPASS # type: ignore
    except Exception:
        ruta_base = os.path.abspath("./rsc")
    return os.path.join(ruta_base, nombre_archivo)


def importar_imagen(nombre_archivo : str) -> Image:
    """Devuelve la imagen dado el nombre del archivo, buscándola en los recursos del programa"""

    try:
        ruta_recurso = ruta_recursos(nombre_archivo)
        return Image.open(ruta_recurso)
    except:
        raise Exception("No se encuentra en /rsc el archivo {}".format(nombre_archivo))
    

def importar_imagen_a_QImage(nombre_archivo : str):
    """Devuelve una QImage dado el nombre del archivo, buscando en los recursos del programa"""
    
    return ImageQt.ImageQt(importar_imagen(nombre_archivo).convert("RGBA"))