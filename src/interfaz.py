"""
    Fichero del código que genera la interfaz
    
    @author: pedropazoscurra
"""

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPoint, QSize, QTimer
from PIL import ImageQt
from gestion_recursos import importar_imagen_a_QImage
import sys
from threading import Thread
from time import sleep
import math


FILENAME_MASCARA_VENTANA = "mascara_ventana.png"
ANCHO_VENTANA = 600
ALTO_VENTANA = 400


class Aviso_Personalizado(QtWidgets.QMessageBox):
    """Clase de alert personalizado cuya pinta en terminos esteticos queda por el momento relegada a mis futuras sinapsis"""

    def __init__(self, titulo : str = "ERROR", mensaje : str = "Error desconocido hasta que se demuestre lo contrario"):
        super().__init__()
        self.titulo = titulo
        self.mensaje = mensaje
        self.icono = self.Icon.Critical

    def ensenha(self):
            """Abstrae QMessageBox.show()"""

            self.setWindowTitle(self.titulo)
            self.setText(self.mensaje)
            self.setIcon(self.icono)
            self.show()


class Ventana_Custom(QtWidgets.QWidget):
    """Clase de ventana personalizada con forma no ortodoxa"""

    def __init__(self):
        super().__init__()

        # DEBUG Aviso personalizado
        #self.aviso = Aviso_Personalizado()
        #self.aviso.ensenha()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # Ventana sin bordes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Fondo transparente (permite alfa en el PNG)

        qimage_mascara = importar_imagen_a_QImage("mascara_ventana.png")
        self.pixmap = QtGui.QPixmap.fromImage(qimage_mascara)

        if self.pixmap.isNull():

            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("Error cargando imagen")
            msg.setText(
                f"No se pudo crear QPixmap.\n"
                f"Formatos soportados: "
                f"{', '.join(fmt.data().decode() for fmt in QtGui.QImageReader.supportedImageFormats())}"
            )
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.show()
            return

        
        self.resize(ANCHO_VENTANA, ALTO_VENTANA) # Redimensionar ventana a la imagen

        # Animacion de movimiento
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_movimiento)
        self.timer.start(50)


    def paintEvent(self, event):
        """Evento de actualizacion"""

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.drawPixmap(0, 0, self.pixmap)

    
    def mousePressEvent(self, event):
        """Callback de boton izquierdo mouse"""
        if event.button() == Qt.MouseButton.LeftButton:

            print("¡Oye! Me haces cosquillas")

            self._drag = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()


    def mouseMoveEvent(self, event):
        """Callback de mover mouse en la pantalla"""

        if event.buttons() & Qt.MouseButton.LeftButton:
            
            self.move(event.globalPosition().toPoint() - self._drag)
            event.accept()
        
        event.accept()


    def loop_movimiento(self):
        """Animacion de la ventana"""

        x = self.x() + 1
        y = self.y() + 1
        self.move(x, y) 

 


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana_Custom()
    ventana.show()
    sys.exit(app.exec())