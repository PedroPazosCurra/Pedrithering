"""
    Fichero Ventana_Personalizada_Madre
    
    @author: pedropazoscurra
"""

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QUrl
from config.constantes import CT_VOLUMEN_AUDIO, CT_PERIODO_ACTUALIZACION_MOVIMIENTO
from PyQt6.QtMultimedia import QSoundEffect

class Ventana_Personalizada_Madre(QtWidgets.QWidget):
    """Clase madre con comportamientos comunes que comparten otras ventanas"""

    def __init__(self, ancho_pantalla, alto_pantalla):
        super().__init__()
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.alto_ventana = 0
        self.ancho_ventana = 0

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint) # Ventana sin bordes y siempre arriba
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Fondo transparente (permite alfa en el PNG)

        # Animacion de movimiento
        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.loop_movimiento)
        self.timer_movimiento.start(CT_PERIODO_ACTUALIZACION_MOVIMIENTO)

    def paintEvent(self, event):
        """Evento de actualizacion"""

        # Pinta el png actual
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.drawPixmap(0, 0, self.pixmap)

    def loop_movimiento(self):
        """Calculo de movimiento de widget"""
        """Cada clase implementa el suyo, lo que importa aquí es que self.timer pueda enlazarse a self.loop_movimiento"""
        print("{0} no implementa loop_movimiento. Por defecto, queda sin implementacion.".format(type(self).__name__))

    def reproducir_sonido(self, nombre_archivo_sonido : str):
        "Reproduce un sonido con un nombre dado usando un QMediaPlayer dado"

        ruta_archivo_sonido = "rsc/sonidos/" + nombre_archivo_sonido 
        self.efecto_sonido = QSoundEffect(self)
        self.efecto_sonido.setSource(QUrl.fromLocalFile(ruta_archivo_sonido))
        self.efecto_sonido.setVolume(CT_VOLUMEN_AUDIO)
        self.efecto_sonido.play()