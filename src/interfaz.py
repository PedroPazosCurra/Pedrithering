"""
    Fichero del código que genera la interfaz
    
    @author: pedropazoscurra
"""

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPoint, QSize, QTimer, QCoreApplication
from PIL import ImageQt
from gestion_recursos import importar_imagen_en_QImage
import sys
from datetime import datetime
import math



LIMITE_SUPERIOR_ANCHO = 1920 # TODO: Tomar dimensiones de la pantalla en lugar de hardcodear esto
LIMITE_SUPERIOR_ALTO = 1080
LIMITE_INFERIOR_ANCHO = 0
LIMITE_INFERIOR_ALTO = 0
ANCHO_VENTANA = 180 # TODO: Tomar dimensiones del png en lugar de hardcodear esto
ALTO_VENTANA = 100
FILENAME_MASCARA_VENTANA = "mascara_ventana.png"

MENSAJE_DESCONOCIDO = "Error desconocido hasta que se demuestre lo contrario"

BOCADILLO_X_RELATIVA = 280
BOCADILLO_Y_RELATIVA = 120

PERIODO_ACTUALIZACION_MOVIMIENTO = 20 # Calculo cada 20 ms
VENTANA_PERIODO_ACTUALIZACION_INERCIA = 20 # Calculo cada 20 ms
UPTIME_BOCADILLO = 1000 # En ms

# Debug
#LIMITE_SUPERIOR_ANCHO = 600
#LIMITE_SUPERIOR_ALTO = 400

# TODO: Todas las clases de la interfaz comparten métodos y atributos - Crear una clase padre Ventana_Custom que las otras hereden/implementen
class Ventana_Personalizada_Madre(QtWidgets.QWidget):
    """Clase madre con comportamientos comunes que comparten otras ventanas"""

    def __init__(self, ancho_pantalla, alto_pantalla):
        super().__init__()
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # Ventana sin bordes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Fondo transparente (permite alfa en el PNG)

        # Animacion de movimiento
        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.loop_movimiento)
        self.timer_movimiento.start(PERIODO_ACTUALIZACION_MOVIMIENTO)

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
        
        self.resize(LIMITE_SUPERIOR_ANCHO - LIMITE_INFERIOR_ANCHO, LIMITE_SUPERIOR_ANCHO - LIMITE_INFERIOR_ALTO) # Redimensionar ventana a la imagen
        

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

        self.bocadillo = Ventana_Bocadillo_Mensaje(screen.size().width(), screen.size().height())
        self.bocadillo.ensenha()

        self.qimage_mascara = QtGui.QPixmap.fromImage(importar_imagen_en_QImage(nombre_archivo="mascara_ventana.png", ratio_tamanho=2))
        self.qimage_mascara_2 = QtGui.QPixmap.fromImage(importar_imagen_en_QImage(nombre_archivo="mascara_ventana_abollada.png", ratio_tamanho=2))
        self.pixmap = self.qimage_mascara

        # Error cargando pixmap
        if self.pixmap.isNull():

            self.aviso = Aviso_Personalizado(titulo="Error cargando imagen", 
                                             mensaje=   f"No se pudo crear QPixmap.\n"
                                                        f"Formatos soportados: "
                                                        f"{', '.join(fmt.data().decode() for fmt in QtGui.QImageReader.supportedImageFormats())}")
            self.aviso.ensenha()
            return

        
        self.resize(self.ancho_pantalla - LIMITE_INFERIOR_ANCHO, self.alto_pantalla - LIMITE_INFERIOR_ALTO) # Redimensionar ventana a la imagen

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
                self.pixmap = self.qimage_mascara_2
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



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    ventana = Ventana_Custom(screen.size().width(), screen.size().height())
    ventana.show()

    sys.exit(app.exec())