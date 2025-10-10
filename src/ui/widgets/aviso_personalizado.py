"""
    Fichero Aviso_Personalizado
    
    @author: pedropazoscurra
"""

from PyQt6 import QtGui, QtWidgets
from config.constantes import *
from rsc.gestion_recursos import importar_imagen_en_QImage

class Aviso_Personalizado(QtWidgets.QMessageBox):
    """Clase de alert personalizado cuya pinta en terminos esteticos queda por el momento relegada a mis futuras sinapsis"""

    def __init__(self, titulo : str = "ERROR", mensaje : str = "Error desconocido hasta que se demuestre lo contrario"):
        super().__init__()
        self.titulo = titulo
        self.mensaje = mensaje
        self.icono = self.Icon.Critical

        qimage_mascara = importar_imagen_en_QImage("aviso.png")
        self.pixmap = QtGui.QPixmap.fromImage(qimage_mascara)


    def paintEvent(self, event):
        """Evento de actualizacion"""

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.drawPixmap(0, 0, self.pixmap)


    def ensenha(self):
            """Abstrae QMessageBox.show() con inicialización aparte"""

            self.setWindowTitle(self.titulo)
            self.setText(self.mensaje)
            self.setIcon(self.icono)
            self.show()