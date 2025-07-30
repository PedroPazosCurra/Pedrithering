"""
    Módulo que abstrae la obtención de recursos
    
    @author: pedropazoscurra
"""

from PIL import Image
import os
import sys

def ruta_recursos(nombre_archivo : str) -> str:
    """Abstrae la obtención de la ruta de recursos"""
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath("./rsc")
    return os.path.join(ruta_base, nombre_archivo)


def importar_imagen(nombre_archivo : str):
    """Devuelve la imagen indicada, buscándola en los recursos del programa"""

    try:
        ruta_recurso = ruta_recursos(nombre_archivo)
        return Image.open(ruta_recurso)
    except:
        raise Exception("No se encuentra el archivo {}".format(nombre_archivo))