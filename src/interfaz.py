"""
    Fichero del código que genera la interfaz
    
    @author: pedropazoscurra
"""

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPoint, QSize, QTimer, QCoreApplication
from PIL import ImageQt
from gestion_recursos import importar_imagen_a_QImage
import sys
from datetime import datetime
import math



LIMITE_SUPERIOR_ANCHO = 1920 # TODO: Tomar dimensiones de la pantalla en lugar de hardcodear esto
LIMITE_SUPERIOR_ALTO = 1080
LIMITE_INFERIOR_ANCHO = 0
LIMITE_INFERIOR_ALTO = 0
ANCHO_VENTANA = 100 # TODO: Tomar dimensiones del png en lugar de hardcodear esto
ALTO_VENTANA = 100
FILENAME_MASCARA_VENTANA = "mascara_ventana.png"

# Debug
#LIMITE_SUPERIOR_ANCHO = 600
#LIMITE_SUPERIOR_ALTO = 400



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


class Ventana_Bocadillo_Mensaje(QtWidgets.QWidget):
    """Bocadillo que soltará la ventana principal en determinadas ocasiones"""

    def __init__(self, mensaje : str = "Error desconocido hasta que se demuestre lo contrario"):
        super().__init__()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # Ventana sin bordes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Fondo transparente (permite alfa en el PNG)

        self.mensaje = mensaje

        qimage_mascara = importar_imagen_a_QImage("aviso.png")
        self.pixmap = QtGui.QPixmap.fromImage(qimage_mascara)

        # Error cargando pixmap
        if self.pixmap.isNull():

            self.aviso = Aviso_Personalizado(titulo="Error cargando imagen", 
                                             mensaje=   f"No se pudo crear QPixmap.\n"
                                                        f"Formatos soportados: "
                                                        f"{', '.join(fmt.data().decode() for fmt in QtGui.QImageReader.supportedImageFormats())}")
            self.aviso.ensenha()
            return


    def ensenha(self):
            """Aparece esta ventana en las coordenadas de la ventana principal"""

            #self.setText(self.mensaje)
            self.show()


class Ventana_Custom(QtWidgets.QWidget):
    """Clase de ventana personalizada con forma no ortodoxa"""

    def __init__(self, ancho_pantalla, alto_pantalla):
        super().__init__()

        # DEBUG Aviso personalizado
        #self.aviso = Aviso_Personalizado()
        #self.aviso.ensenha()

        self.ultima_medida_posicion_inercia = (self.x(), self.y())
        self.inercia = 0
        self.direccion_movimiento = 0
        self.agarrado = False

        self.bocadillo = Ventana_Bocadillo_Mensaje()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # Ventana sin bordes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Fondo transparente (permite alfa en el PNG)

        qimage_mascara = importar_imagen_a_QImage("mascara_ventana.png")
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

        # Animacion de movimiento
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_movimiento)
        self.timer.start(20)

        # Calculo de inercia
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_calcular_inercia)
        self.timer.start(20)


    def paintEvent(self, event):
        """Evento de actualizacion"""

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.drawPixmap(0, 0, self.pixmap)

    
    def mousePressEvent(self, event):
        """Callback de boton izquierdo mouse"""
        if event.button() == Qt.MouseButton.LeftButton:

            print("¡Oye! Me haces cosquillas")
            self.agarrado = True
            self._drag = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()


    def mouseMoveEvent(self, event):
        """Callback de mover mouse en la pantalla"""

        if event.buttons() & Qt.MouseButton.LeftButton:
            
            self.move(event.globalPosition().toPoint() - self._drag)
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
            if nuevo_x <= LIMITE_INFERIOR_ANCHO or nuevo_x >= LIMITE_SUPERIOR_ANCHO - ANCHO_VENTANA:
                nuevo_x = self.x() - escalar_vector_movimiento_x
                # TODO: Cambio de png cuando rebote
                #self.bocadillo.ensenha()
            elif  nuevo_y <= LIMITE_INFERIOR_ALTO or nuevo_y >= LIMITE_SUPERIOR_ALTO - ALTO_VENTANA:
                nuevo_y = self.y() - escalar_vector_movimiento_y + valor_bamboleo
                # TODO: Cambio de png cuando rebote
                #self.bocadillo.ensenha()

            self.direccion_movimiento = math.atan2(nuevo_x - self.x(), nuevo_y - self.y())

            x = max(min(nuevo_x, LIMITE_SUPERIOR_ANCHO-ANCHO_VENTANA), LIMITE_INFERIOR_ANCHO+1)
            y = max(min(nuevo_y, LIMITE_SUPERIOR_ALTO-ALTO_VENTANA), LIMITE_INFERIOR_ALTO+1)

            print(str(x) + " , " + str(y) + " / " + str(self.direccion_movimiento))

            self.move(x, y) 

    
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
    ventana = Ventana_Custom(screen.size().width, screen.size().height)
    ventana.show()
    sys.exit(app.exec())