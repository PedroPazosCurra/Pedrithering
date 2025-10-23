from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer
from rsc.gestion_recursos import importar_imagen_en_QImage
from config.constantes import *
from src.ui.widgets.ventana_personalizada_madre import Ventana_Personalizada_Madre
from src.ui.widgets.aviso_personalizado import Aviso_Personalizado


class Ventana_Bocadillo_Mensaje(Ventana_Personalizada_Madre):
    """Bocadillo que soltará la ventana principal en determinadas ocasiones"""

    def __init__(self, ancho_pantalla, alto_pantalla, mensaje : str = MENSAJE_DESCONOCIDO):
        super().__init__(ancho_pantalla, alto_pantalla)

        self.x_actual = 0
        self.y_actual = 0

        # Label con texto
        # TODO Parametrizar posicion label con tamanho de bocadillo
        # TODO Echar un ojo a fuente, color, alinear, ...
        self.label_mensaje = QtWidgets.QLabel(self)
        self.label_mensaje.setText(mensaje)
        self.label_mensaje.move(self.x_actual, self.y_actual+50) 
    
        qimage_bocadillo = importar_imagen_en_QImage("bocadillo.png", 0.3)
        self.pixmap = QtGui.QPixmap.fromImage(qimage_bocadillo)
        self.alto_ventana = self.pixmap.height()
        self.ancho_ventana = self.pixmap.width()

        # Error cargando pixmap
        if self.pixmap.isNull():

            self.aviso = Aviso_Personalizado(titulo="Error cargando imagen", 
                                             mensaje=   f"No se pudo crear QPixmap.\n"
                                                        f"Formatos soportados: "
                                                        f"{', '.join(fmt.data().decode() for fmt in QtGui.QImageReader.supportedImageFormats())}")
            self.aviso.ensenha()
            return
        
        # Redimensionar ventana a la imagen
        self.resize(self.ancho_pantalla, self.alto_pantalla) 


    def paintEvent(self, event):
        """Evento de actualizacion"""

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.drawPixmap(0, 0, self.pixmap)


    def loop_movimiento(self):
        """Calculo de movimiento de widget"""
        self.move(self.x_actual, self.y_actual) 


    def actualiza_posicion(self, x, y):
        """Método expuesto a clase padre para mover el widget con él"""
        self.x_actual = x - self.ancho_ventana
        self.y_actual = y - self.alto_ventana


    def ensenha(self, mensaje = MENSAJE_DESCONOCIDO):
        """Abstrae y expone a padre QWidget.show()"""
        self.label_mensaje.setText(mensaje)
        self.show()

        QTimer.singleShot(UPTIME_BOCADILLO, self.hide)