"""
    Fichero del código que genera la interfaz
    
    @author: pedropazoscurra
"""

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer
import sys
from datetime import datetime
import math
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
    
        qimage_mascara = importar_imagen_en_QImage("bocadillo.png", 0.3)
        self.pixmap = QtGui.QPixmap.fromImage(qimage_mascara)

        # Error cargando pixmap
        if self.pixmap.isNull():

            self.aviso = Aviso_Personalizado(titulo="Error cargando imagen", 
                                             mensaje=   f"No se pudo crear QPixmap.\n"
                                                        f"Formatos soportados: "
                                                        f"{', '.join(fmt.data().decode() for fmt in QtGui.QImageReader.supportedImageFormats())}")
            self.aviso.ensenha()
            return
        
        # Redimensionar ventana a la imagen
        self.resize(self.ancho_pantalla - LIMITE_INFERIOR_ANCHO, self.alto_pantalla - LIMITE_INFERIOR_ALTO) 


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
        self.x_actual = x - BOCADILLO_X_RELATIVA
        self.y_actual = y - BOCADILLO_Y_RELATIVA


    def ensenha(self, mensaje = MENSAJE_DESCONOCIDO):
        """Abstrae y expone a padre QWidget.show()"""
        self.label_mensaje.setText(mensaje)
        self.show()

        QTimer.singleShot(UPTIME_BOCADILLO, self.hide)



class Ventana_Custom(Ventana_Personalizada_Madre):
    """Clase de ventana personalizada con forma no ortodoxa"""

    def __init__(self, ancho_pantalla, alto_pantalla):
        super().__init__(ancho_pantalla, alto_pantalla)

        # DEBUG Aviso personalizado
        #self.aviso = Aviso_Personalizado()
        #self.aviso.ensenha()

        self.ultima_medida_posicion_inercia = (self.x(), self.y())
        self.inercia = 0
        self.direccion_movimiento = 0
        self.agarrado = False

        self.bocadillo = Ventana_Bocadillo_Mensaje(ancho_pantalla, alto_pantalla)
        self.bocadillo.ensenha()

        self.qimage_mascara = QtGui.QPixmap.fromImage(importar_imagen_en_QImage(nombre_archivo="mascara_ventana.png", ratio_tamanho=2))
        self.qimage_mascara_abollada = QtGui.QPixmap.fromImage(importar_imagen_en_QImage(nombre_archivo="mascara_ventana_abollada.png", ratio_tamanho=2))
        self.pixmap = self.qimage_mascara

        # Error cargando pixmap
        if self.pixmap.isNull():

            self.aviso = Aviso_Personalizado(titulo="Error cargando imagen", 
                                             mensaje=   f"No se pudo crear QPixmap.\n"
                                                        f"Formatos soportados: "
                                                        f"{', '.join(fmt.data().decode() for fmt in QtGui.QImageReader.supportedImageFormats())}")
            self.aviso.ensenha()
            return
        
        # Redimensionar ventana a la imagen
        self.resize(self.ancho_pantalla - LIMITE_INFERIOR_ANCHO, self.alto_pantalla - LIMITE_INFERIOR_ALTO) 

        # Calculo de inercia
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_calcular_inercia)
        self.timer.start(VENTANA_PERIODO_ACTUALIZACION_INERCIA)

    
    def mousePressEvent(self, event):
        """Callback de boton izquierdo mouse"""
        if event.button() == Qt.MouseButton.LeftButton:

            print("Click!")
            self.agarrado = True
            self._drag = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()


    def mouseMoveEvent(self, event):
        """Callback de mover mouse en la pantalla"""

        if event.buttons() & Qt.MouseButton.LeftButton and self.agarrado:

            print("¡Oye! Bájame !! ")
            nueva_posicion = event.globalPosition().toPoint() - self._drag
            self.move(nueva_posicion)
            self.bocadillo.actualiza_posicion(nueva_posicion.x(), nueva_posicion.y())
            event.accept()
        
        event.accept()

    
    def mouseReleaseEvent(self, event):
        """Callback de soltar ratón"""

        self.agarrado = False
        print("Qué alivio, macho...!")



    def loop_movimiento(self):
        """Animacion de bamboleo de la ventana"""

        if not self.agarrado:

            valor_bamboleo = round(self.inercia <= 1 and (2*math.sin(round(datetime.now().microsecond / 150000, 2))))

            escalar_vector_movimiento_x = round(math.sin(self.direccion_movimiento) * self.inercia)
            escalar_vector_movimiento_y = round(math.cos(self.direccion_movimiento) * self.inercia)

            nuevo_x = self.x() + escalar_vector_movimiento_x
            nuevo_y = self.y() + escalar_vector_movimiento_y + valor_bamboleo

            # Rebote en esquinas
            if nuevo_x <= 0 or nuevo_x >= self.ancho_pantalla - ANCHO_VENTANA:

                nuevo_x = self.x() - escalar_vector_movimiento_x

                # Cambio png
                self.pixmap = self.qimage_mascara
                self.update()

                # Bocadillo
                self.bocadillo.ensenha("Boing !")

            elif  nuevo_y <= 0 or nuevo_y >= self.alto_pantalla - ALTO_VENTANA:

                nuevo_y = self.y() - escalar_vector_movimiento_y + valor_bamboleo

                # Cambio png
                self.pixmap = self.qimage_mascara_abollada
                self.update()

                # Bocadillo
                self.bocadillo.ensenha("Boooing ...!")

            self.direccion_movimiento = math.atan2(nuevo_x - self.x(), nuevo_y - self.y())

            x = max(min(nuevo_x, self.ancho_pantalla - ANCHO_VENTANA), 1)
            y = max(min(nuevo_y, self.alto_pantalla - ALTO_VENTANA), 1)

            print(str(x) + " , " + str(y) + " / " + str(self.direccion_movimiento))

            self.move(x, y) 
            self.bocadillo.actualiza_posicion(x,y)

    
    def loop_calcular_inercia(self):
        """Bucle de calculo de inercia"""

        ultimo_x, ultimo_y = self.ultima_medida_posicion_inercia
        self.ultima_medida_posicion_inercia = (self.x(), self.y())

        if self.agarrado:

            self.direccion_movimiento = math.atan2(self.x() - ultimo_x, self.y() - ultimo_y) # (radianes)
            self.inercia = math.dist([ultimo_x, ultimo_y], [self.x(), self.y()])

        else: 
            if self.inercia > 0:
                self.inercia -= self.inercia/10
            else:
                self.inercia = 0

        #print("Inercia actual =" + str(self.inercia) + "  Direccion = " + str(self.direccion_movimiento))


def setup_interfaz():
    """Punto de entrada expuesto"""

    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    ventana = Ventana_Custom(screen.size().width(), screen.size().height())
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    ventana = Ventana_Custom(screen.size().width(), screen.size().height())
    ventana.show()

    sys.exit(app.exec())