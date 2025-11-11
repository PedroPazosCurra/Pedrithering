"""
    Fichero del código que genera la interfaz
    
    @author: pedropazoscurra
"""

from PyQt6 import QtWidgets
import sys
from rsc.gestion_recursos import importar_imagen_en_QImage
from config.constantes import *
from src.ui.widgets.ventana_principal import Ventana_Principal


def setup_interfaz():
    """Punto de entrada expuesto"""

    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    ventana = Ventana_Principal(screen.size().width(), screen.size().height())
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    ventana = Ventana_Principal(screen.size().width(), screen.size().height())
    ventana.show()

    sys.exit(app.exec())