"""
    Fichero Ventana_Principal
    
    @author: pedropazoscurra
"""

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime
import math
from rsc.gestion_recursos import importar_imagen_en_QImage
from config.constantes import *
from src.ui.widgets.ventana_personalizada_madre import Ventana_Personalizada_Madre
from src.ui.widgets.aviso_personalizado import Aviso_Personalizado
from src.ui.widgets.ventana_bocadillo_mensaje import Ventana_Bocadillo_Mensaje



class Ventana_Principal(Ventana_Personalizada_Madre):
    """Clase de ventana personalizada con forma no ortodoxa"""

    def __init__(self, ancho_pantalla, alto_pantalla):
        super().__init__(ancho_pantalla, alto_pantalla)

        # DEBUG Aviso personalizado
        #self.aviso = Aviso_Personalizado()
        #self.aviso.ensenha()

        self.choques = 0
        self.inercia = 0
        self.direccion_movimiento = 0
        self.agarrado = False
        self.ultima_medida_posicion_inercia = (self.x(), self.y())

        self.bocadillo = Ventana_Bocadillo_Mensaje(ancho_pantalla, alto_pantalla)
        self.bocadillo.ensenha()

        self.qimage_mascara_normal = QtGui.QPixmap.fromImage(importar_imagen_en_QImage(nombre_archivo="mascara_ventana.png", ratio_tamanho=2))
        self.qimage_mascara_abollada = QtGui.QPixmap.fromImage(importar_imagen_en_QImage(nombre_archivo="mascara_ventana_abollada.png", ratio_tamanho=2))

        self.pixmap = self.qimage_mascara_normal
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

        # Calculo de inercia
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_calcular_inercia)
        self.timer.start(CT_VENTANA_PERIODO_ACTUALIZACION_INERCIA)

    
    def mousePressEvent(self, event):
        """Callback de boton izquierdo mouse"""
        if event.button() == Qt.MouseButton.LeftButton:

            print("Click!")
            self.agarrado = True
            self._drag = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()


    def mouseMoveEvent(self, event):
        """Callback de arrastrar ventana por la pantalla"""

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

            # TODO: Limpiar magic numbers en el calculo o bien usar una formula no calculada a ojo (parametrizada..)
            valor_bamboleo = round(self.inercia <= 1 and (2*math.sin(round(datetime.now().microsecond / 150000, 2))))

            escalar_vector_movimiento_x = round(math.sin(self.direccion_movimiento) * self.inercia)
            escalar_vector_movimiento_y = round(math.cos(self.direccion_movimiento) * self.inercia)
            nuevo_x = self.x() + escalar_vector_movimiento_x
            nuevo_y = self.y() + escalar_vector_movimiento_y + valor_bamboleo

            # Rebote en esquinas
            choque_horizontal = (nuevo_x <= 0 or nuevo_x >= self.ancho_pantalla - self.ancho_ventana)
            choque_vertical = (nuevo_y <= 0 or nuevo_y >= self.alto_pantalla - self.alto_ventana)

            if choque_horizontal or choque_vertical:

                # Cambio png
                if self.choques >= 10:
                    self.pixmap = self.qimage_mascara_abollada
                    self.alto_ventana = self.pixmap.height()
                    self.ancho_ventana = self.pixmap.width()
                    self.update()


                if self.choques >= 30:
                    self.bocadillo.ensenha("¡...Regenerando...!")
                    QTimer.singleShot(CT_UPTIME_ABOLLADURA, self.recuperar_forma)

                # Sonido de rebote
                self.reproducir_sonido("rebote.wav")

                # Bocadillo dice boing
                self.bocadillo.ensenha("Boing !")
                self.choques += 1

                # Cambio de direccion
                if choque_vertical:
                    nuevo_y = self.y() - escalar_vector_movimiento_y
                elif choque_horizontal:
                    nuevo_x = self.x() - escalar_vector_movimiento_x


            self.direccion_movimiento = math.atan2(nuevo_x - self.x(), nuevo_y - self.y())

            x = max(min(nuevo_x, self.ancho_pantalla - self.ancho_ventana), 1)
            y = max(min(nuevo_y, self.alto_pantalla - self.alto_ventana), 1)

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


    def recuperar_forma(self):
        """Funcion llamada por el timer despues de chocar. Recupera la forma original"""

        # Cambio png
        self.pixmap = self.qimage_mascara_normal
        self.alto_ventana = self.pixmap.height()
        self.ancho_ventana = self.pixmap.width()
        self.update()
