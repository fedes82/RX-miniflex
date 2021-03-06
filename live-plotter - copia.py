# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui, uic
import serial
import sys
import glob
import multiprocessing as mp
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from time import sleep
from time import time
from time import gmtime, strftime
from os.path import expanduser
from decimal import *
#//ver esto
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import sin,radians

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('bitacora.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(processName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
# Cargar nuestro archivo .ui
form_class = uic.loadUiType("ui.ui")[0]
logger.info('---------------------------------------------------')
logger.info('Inicio Programa RX')
#eto es para usar 2 decimales
#getcontext.prec=2

# def Comprobar_Conexion(puerto, q_datos,q_cerrar):
    # """ Esta funcion abre el puerto serie, envia una P (comando
    # para que responda el micro si hay conexion) y devuelve true si hay 
    # conexion o false si el micro no responde """
    # ser = serial.Serial(port=puerto, baudrate=9600,timeout=3)
    # sleep(0.1)
    # print 'el puerto se abrio?', ser
    # p = ''
    # ser.flushInput()
    # ser.flushOutput()
    

# def Monitor_Serie(puerto, q_datos,q_cerrar):
    # """Este thread se ocupa de leer el puerto paralelo
        # - loop infinito que blockea hasta que lee una linea del pto serie
        # - cuando llega una nueva linea la pone en la cola q_datos
        # - cuando se pone algo en la cola q_cerrar, cierra todo y sale
        
    # """
    # ser = serial.Serial(port=puerto, baudrate=9600,timeout=1)
    # sleep(0.1)
    # print 'el puerto se abrio?', ser
    # d = 0
    # ser.flushInput()
    # ser.flushOutput()
    # sleep(0.5)
    # #Comprobacion de conexion, envio p, si hay timeout repito 10 veces
    # # si responde algo distinto de 'COM OK' o si no responde, hay error en
    # # comunicacion; aviso al prog principal y cierro puerto serie
    # t = ''
    # for i in range(10):
        # ser.write('P')
        # t = ser.read()
        # if len(t) > 0 :
            # sleep(0.05)
            # t = t + ser.read(ser.inWaiting())
            # break
    # if (len(t)== 0)  or (not t.startswith('COM OK')):
        # print 'error en la comunicacion'
        # q_datos.put('sin conexion')
        # q_cerrar.get()
        # q_cerrar.close()
        # q_datos.close()
        # d =0
        # t =0
        # ser.close()
        # ser.close()
        # print 'COMPROBAR CONEXION'
        # return
    # ser = serial.Serial(port=puerto, baudrate=9600,timeout=10)   
    # print 'envio ', ser.write('I'), ' bytes, comienzo medicion'
    # while(q_cerrar.empty()):
        # t = ser.read()
        # ti = time()
        # if len(t) > 0 :
            # sleep(0.05)
            # print 'quedan ', ser.inWaiting(), ' bytes'
            # print 'recibi' ,t
           # # while not t == '.':
           # #     d = 10 * d + int(t)
           # #     t = ser.read()
           # # print 'tengo punto'
           # # t = ser.read()
           # # d = d + (t*0.1)
           # # t = ser.read()
           # # d = d + (t*0.01)
            # t = t + ser.read(ser.inWaiting())
            # print t
           # # print d
            # q_datos.put(float(t))
            # # avanza a 0.5 grados por minuto, tonces muestreo cada 
            # sleep(0.232)
            # ser.write('1')
            # ser.timeout = 1
        # else:
            # ser.timeout = 1
            # print 'timeout'
        # tf = time()
        # print 'tarde: ', tf-ti, 'en recibir el dato'
    # print 'cierro puerto y proceso comunicacion'
    # q_cerrar.get()
    # q_cerrar.close()
    # q_datos.close()
    # ser.write('T')
    # d =0
    # t =0
    # ser.close()
    # ser.close()

# def Monitor_Serie_con_nl(puerto, q_datos,q_cerrar):
    # """Este thread se ocupa de leer el puerto paralelo
        # - loop infinito que blockea hasta que lee una linea del pto serie
        # - cuando llega una nueva linea la pone en la cola q_datos
        # - cuando se pone algo en la cola q_cerrar, cierra todo y sale
        
    # """
    # ser = serial.Serial(port=puerto, baudrate=9600,timeout=60)
    # sleep(0.1)
    # print 'el puerto se abrio?', ser
    # ser.flushInput()
    # ser.flushOutput()
    # sleep(1)
    # print 'envio ', ser.write('I'), ' bytes'
    # while(q_cerrar.empty()):
        # t = ser.readline()
        # if len(t) > 0 :
            # print 'recibi: ',t
            # q_datos.put(float(t))
                # # avanza a 0.5 grados por minuto, tonces muestreo cada 
            # sleep(0.29)
            # ser.write('1')
            # ser.timeout = 1
        # else:
            # ser.timeout = 1
            # print 'timeout'
    # print 'cierro puerto y proceso comunicacion'
    # q_cerrar.get()
    # q_cerrar.close()
    # q_datos.close()
    # ser.write('T')
    # t =0
    # ser.close()
    # ser.close()

def Monitor_Serie_con_nl_y_mark(puerto, q_datos,q_cerrar):
    """Este thread se ocupa de leer el puerto serie
        - Comprobacion de conexion, envia P 10 veces, si no recibe respuesta
            o la respuesta es distinta de OK COM, avisa al prog principal
            y cierra el puerto y el thread
        - loop infinito que blockea hasta que lee una linea del pto serie
        - cuando llega una nueva linea la pone en la cola q_datos
        - cuando se pone algo en la cola q_cerrar, cierra todo y sale
        
    """
    ser = serial.Serial(port=puerto, baudrate=9600,timeout=1.5)
    sleep(0.1)
    logger.info('Inicio monitor del puerto serie')
    logger.info('Pto Serie: \n{}'.format(ser))
    print 'el puerto se abrio?', ser
    ser.flushInput()
    ser.flushOutput()
    t = ''
    for i in range(10):
        ser.write('P')
        t = ser.read()
        if len(t) > 0 :
            sleep(0.05)
            t = t + ser.read(ser.inWaiting())
            break
        logger.error('timeout de la conexion')
        print 'timeout comprobar conexion'
    if (len(t)== 0)  or (not t.startswith('COM OK')):
        print 'error en la comunicacion'
        logger.error('error en la comunicacion, cierro coenxion y thread del monitor')
        q_datos.put('sin conexion')
        q_cerrar.get()
        q_cerrar.close()
        q_datos.close()
        d =0
        t =0
        ser.close()
        ser.close()
        print 'COMPROBAR CONEXION'
        return
    print 'Conexion OK'
    logger.info('Conexion OK')
    ser.timeout = 30
    print 'envio ', ser.write('I'), ' bytes'
    print 'queue vacia:',q_cerrar.empty()
    while(q_cerrar.empty()):
        t = ser.readline()
        if len(t) > 0 :
            if not t.startswith('f'):
                print 'recibi: ',t
                q_datos.put(float(t))
                    # avanza a 2 grados por minuto, tonces muestreo cada 
                #sleep(0.29)
                #ser.write('1')
                ser.timeout = 1
        else:
            ser.timeout = 1
            print 'timeout'
            logger.warning('Timeout esperando dato')
    print 'cierro puerto y proceso comunicacion'
    q_cerrar.get()
    print 'queue vacia:',q_cerrar.empty()
    q_cerrar.close()
    q_datos.close()
    ser.write('T')
    t =0
    ser.close()
    ser.close()
    logger.info('Cierro conexion y thread del monitor')
    
def serial_ports():
    """Lista los puertos serie
        :raises EnvironmentError:
            Cuando se ejecuta en plataformas no 
            soportadas o desconocidas
        :returns:
            Una lista con los puertos disponibles del sistema
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        logger.error('Error en serial_ports() - Unsuported Plataform')
        raise EnvironmentError('Unsupported platform')
    
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result 

class MyWindowClass(QtGui.QMainWindow, form_class):
    """Este es el main thread, la ventana con el programa principal"""
    #variables globales
    ydatos = []
    xdatos = []
    datos = []
    datos_porcentual = []
    datos_x_espacio = []
    datos_x_espacio = []
    
    def __init__(self, parent=None):
        """inicializacion del programa ppal"""
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # aca indico que ejecuta cuando apreto cada boton
        self.btn_Abrir_conexion.clicked.connect(self.btn_Abrir_conexion_clicked)
        self.btn_cerrar_conexion.clicked.connect(self.btn_cerrar_conexion_clicked)
        self.btn_Salir.clicked.connect(self.btn_salir_clicked)
        self.btn_CargarMedicion.clicked.connect(self.btn_CargarMedicion_clicked)
        self.btn_GuardarMedicion.clicked.connect(self.btn_GuardarMedicion_clicked)
        self.btn_LimpiarPlot.clicked.connect(self.btn_LimpiarPlot_clicked)
        self.btn_XReset.clicked.connect(self.btn_XReset_clicked)
        self.btn_YReset.clicked.connect(self.btn_YReset_clicked)
        self.rbtn_Absoluto.clicked.connect(self.rbtn_Absoluto_clicked)
        self.rbtn_Relativo.clicked.connect(self.rbtn_Relativo_clicked)
        self.rbtn_Espacio.clicked.connect(self.rbtn_Espacio_clicked)
        self.rbtn_Grados.clicked.connect(self.rbtn_Grados_clicked)
        #self.chk_Autoscale.clicked.connect()
        
        #esto es para el grafico, curve es el graf propiamente dicho y timer 
        # es lo que uso para actualizarlo
        self.curve = self.VentanaPlot.plot(pen='y')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        
        #pra el cursor
        #cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.VentanaPlot.addItem(self.vLine, ignoreBounds=True)
        self.VentanaPlot.addItem(self.hLine, ignoreBounds=True)
        self.vb = self.VentanaPlot.plotItem.vb
        # en el proxy este, que hay que ver bien que hace, el ratelimit me sirve para
        # limitar las actualizaciones por segundo, para que no se tare el programa
        self.proxy = pg.SignalProxy(self.VentanaPlot.scene().sigMouseMoved, rateLimit=30, slot=self.mouseMoved)
        
        # Inicializo los widgets
        self.rbtn_Absoluto.setChecked(True)
        self.rbtn_Grados.setChecked(True)
        self.cmb_AnguloInicial.setCurrentIndex(5)
        self.cmb_CPS.setCurrentIndex(3)
        self.lnedit_lambda.setText('1.5405')
        self.lnedit_lambda.setValidator(QDoubleValidator(0.0000,99.9999,4))
        puertos = serial_ports()
        print puertos
        logger.info('Los puertos disponibles son: {}'.format(puertos))
        for puerto in puertos:
            self.combo_puertos.addItem(puerto)
        self.q_datos = mp.Queue()
        self.q_cerrar = mp.Queue()
    
     ###-------------- Acciones de los Botones
     
    def btn_XReset_clicked(self):
        if self.rbtn_Espacio.isChecked():
            if int(self.cmb_AnguloInicial.currentText()):
                min = float(self.lnedit_lambda.text())/(2*sin(radians(int(self.cmb_AnguloInicial.currentText())/2)))
            else:
                min = 0
            max = float(self.lnedit_lambda.text())/(2*sin(radians(int(self.cmb_AnguloInicial.currentText())/2)))
            self.VentanaPlot.setXRange(min,max,update=True)
            self.VentanaPlot.invertX(False)
        else:
            self.VentanaPlot.setXRange(int(self.cmb_AnguloFinal.currentText()),int(self.cmb_AnguloInicial.currentText()),update=True)
            self.VentanaPlot.invertX(True)
    
    
    def btn_YReset_clicked(self):
        if self.rbtn_Absoluto.isChecked():  #Opciones para visualizar eje Y en valor Absoluto
            self.VentanaPlot.setYRange(0,1024,update=True)
        else:
            self.VentanaPlot.setYRange(0,100,update=True)
    
     
    def rbtn_Absoluto_clicked(self):
        """cambia las unidades de las ordenadas al valor absoluto
         y redibuja el plotteo"""
        logger.info('Cambio coordenadas a valor absoluto')
        self.ydatos = np.array(self.datos)
        self.VentanaPlot.setLabel('left','Valor', units='mV')
        self.curve.setData(self.xdatos, self.ydatos)
        self.btn_YReset_clicked()

        
    def rbtn_Relativo_clicked(self):
        """cambia las unidades de las ordenadas, normalizandolas a 100%
        y redibuja el plotteo"""
        logger.info('Cambio coordenadas a valor relativo')
        self.ydatos = np.array(self.datos_porcentual)
        self.VentanaPlot.setLabel('left','Porcentual', units='%')
        self.curve.setData(self.xdatos, self.ydatos)
        self.btn_YReset_clicked()

        
    def rbtn_Espacio_clicked(self):
        """cambia las unidades de la absisa, a espacio interplanar
        y redibuja el plotteo"""
        logger.info('Cambio absisas a espacio interplanar')
        self.VentanaPlot.setLabel('bottom','Espacio Interplanar', units='Armstrong')
        self.xdatos = np.array(self.datos_x_espacio)
        self.curve.setData(self.xdatos, self.ydatos)
        self.btn_XReset_clicked()
    
    def rbtn_Grados_clicked(self):
        """ cambia las unidades de la absisa, a grados
        y redibuja el plotteo"""
        logger.info('Cambio absisas a grados')
        self.xdatos = np.array(self.datos_x_angulo)
        self.VentanaPlot.setLabel('bottom','Angulo', units='grados')
        self.curve.setData(self.xdatos, self.ydatos)
        self.btn_XReset_clicked()
    
    def btn_Abrir_conexion_clicked(self):
        """Crea thread con el monitor del pto serie, setea el timer 
        que actualiza el ploteo y deshabilita los botones que no se
        pueden usar mientras plotea"""
        self.q_datos = mp.Queue()
        self.q_cerrar = mp.Queue()
        if self.lnedit_Muestra.text() == '':
            self.msj_error_nombre_muestra()
            return
        self.lbl_estado.setText ('CONECTADO')
        print self.combo_puertos.currentText()
        logger.info('Abro conexion, utilizo puerto: {}'.format(self.combo_puertos.currentText()))
        self.monitor_serie = mp.Process(target=Monitor_Serie_con_nl_y_mark, name='MonitorPtoSerie', args=(str(self.combo_puertos.currentText()), self.q_datos, self.q_cerrar))
        self.monitor_serie.start()
        #esto dispara el timer que actualiza el plot
        self.timer.start(150)
        self.btn_GuardarMedicion.setEnabled(False)
        self.btn_CargarMedicion.setEnabled(False)
        self.combo_puertos.setEnabled(False)
        self.cmb_AnguloInicial.setEnabled(False)
        self.cmb_AnguloFinal.setEnabled(False)
        self.btn_Abrir_conexion.setEnabled(False)
        self.btn_LimpiarPlot.setEnabled(False)
        self.btn_cerrar_conexion.setEnabled(True)
        self.btn_XReset_clicked()
        self.btn_YReset_clicked()
        
    def btn_cerrar_conexion_clicked(self):
        """ Indica al monitor serie que cierre la conexion y 
           rehabilita los botones que deshabilito iniciar sesion"""
        logger.info('Cierro conexion con adquisidor')
        self.lbl_estado.setText( 'DESCONECTADO')
        self.q_datos
        self.q_cerrar.put('s')
        self.monitor_serie.join()
        self.q_datos.close()
        self.q_cerrar.close()
        #Aca detengo el timer que actualiza el plot
        self.timer.stop()
        self.btn_GuardarMedicion.setEnabled(True)
        self.btn_CargarMedicion.setEnabled(True)
        self.combo_puertos.setEnabled(True)
        self.cmb_AnguloInicial.setEnabled(False)
        self.cmb_AnguloFinal.setEnabled(False)
        self.btn_Abrir_conexion.setEnabled(True)
        self.btn_LimpiarPlot.setEnabled(True)
        
    def btn_CargarMedicion_clicked(self):
        open_filename = QFileDialog.getOpenFileName(self, 'Abrir Archivo', 'c:\\')#,"Image files (*.jpg *.gif)")
        print open_filename
        logger.info('Abro archivo: {}'.format(open_filename))
        try:
            with open(open_filename,'r') as archivo:
                texto = archivo.readlines()
            self.datos = []
            self.datos_x_angulo = []
            if texto[0].startswith('MUESTRA'):
                self.lnedit_Muestra.setText(texto.pop(0).split()[1])
                self.lnedit_lambda.setText(texto.pop(0).split()[1])
                for i in range(6):
                    texto.pop(0)
            for linea in texto:
                self.datos.append(float(linea.split()[1]))
                self.datos_x_angulo.append(float(linea.split()[0]))
            self.datos_porcentual = [valor*100/max(self.datos)  for valor in self.datos]
            self.datos_x_espacio = [ float(self.lnedit_lambda.text())/(2*sin(radians(angulo/2))) for angulo in self.datos_x_angulo]
            self.ydatos = np.array(self.datos)
            self.xdatos = np.array(self.datos_x_angulo)
            self.rbtn_Absoluto.setChecked(True)
            self.rbtn_Relativo.setChecked(False)
            self.rbtn_Espacio.setChecked(False)
            self.rbtn_Grados.setChecked(True)
           # print 'datos: ',self.datos
           # print 'datos angulo ', self.datos_x_angulo
           # print 'espacio inter: ', self.datos_x_espacio
           # print 'datos_porcentual: ', self.datos_porcentual
            self.curve.setData(self.xdatos,self.ydatos)
            self.combo_puertos.setEnabled(False)
            self.cmb_AnguloInicial.setEnabled(False)
            self.cmb_AnguloFinal.setEnabled(False)
            self.btn_Abrir_conexion.setEnabled(False)
            self.cmb_CPS.setEnabled(False)
            self.lnedit_Muestra.setEnabled(False)
            self.btn_cerrar_conexion.setEnabled(False)
            self.lnedit_lambda.setEnabled(False)
            self.VentanaPlot.invertX(True)
        except IOError as e:
            print 'no existe el archivo'
            logger.error('No se pudo abrir archivo: {} - Error {}'.format(open_filename,e))
    
    
    
    
    def btn_GuardarMedicion_clicked(self):
        save_filename = str(QFileDialog.getSaveFileName(self, 'Guardar Archivo', directory=expanduser("~")+'\\desktop\\<'+self.lnedit_Muestra.text()+'-'+self.cmb_CPS.currentText()+'CPS.txt'))
        if not save_filename.lower().endswith('.txt'):
            save_filename = save_filename + '.txt'
        try:
            with open(save_filename,'w') as archivo:
                # ENCABEZADO
                archivo.write('MUESTRA:\t'+self.lnedit_Muestra.text()+'\n')
                archivo.write('LongRx:\t'+self.lnedit_lambda.text()+'\n')
                archivo.write('CPS:\t'+self.cmb_CPS.currentText()+'\n')
                archivo.write('Intervalo:\t'+self.cmb_AnguloFinal.currentText()+'-'+self.cmb_AnguloInicial.currentText()+'\n')
                archivo.write('Fecha:\t'+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\n'+'\n')
                archivo.write('2Theta\tINTENSIDAD\td'+'\n')
                archivo.write('(º)\t(u.a.)\t(Armstrong)'+'\n')
                #TABLA DE DATOS
                for i in range(len(self.datos)):
                    archivo.write( "%.2f" % self.datos_x_angulo[i] + '\t' +  "%.2f" % self.datos[i] +'\t' + "%.4f" % self.datos_x_espacio[i] + '\n')
                logger.info('Se guardo el archivo: {}'.format(save_filename + '.txt'))
        except:
            logger.error('Problemas al guardar archivo: {}'.format(save_filename + '.txt'))
        
    def btn_salir_clicked(self):
        self.btn_cerrar_conexion_clicked()
        logger.info('Cierro Programa RX')
        logger.info('*********************************')
        exit()
        
    def btn_LimpiarPlot_clicked(self):
        logger.info('Limpie plot')
        self.curve.clear()
        self.datos = []
        self.cmb_AnguloInicial.setEnabled(True)
        self.cmb_AnguloFinal.setEnabled(True)
        self.cmb_CPS.setEnabled(True)
        self.combo_puertos.setEnabled(True)
        self.btn_Abrir_conexion.setEnabled(True)
        self.lnedit_Muestra.setEnabled(True)
        self.btn_cerrar_conexion.setEnabled(False)
        self.lnedit_lambda.setEnabled(True)
        self.lnedit_lambda.setText('1.5405')
    
    
    def update_plot(self):
        """ Este es el algoritmo que toma los datos y los formatea
        para mostrarlo en el grafico, 
        se ejecuta en cada timeout del timer y toma los datos de una 
        queue que comparte con el thread del monitor del pto serie.
        Si lee de la queue la cadena 'sin conexion' supone que el adquisidor
        no esta conectado, muestra el mensaje de error y cierra el thread del monitor
        
        """
        if not self.q_datos.empty():
            while not self.q_datos.empty():
                temp = self.q_datos.get()
                if temp == 'sin conexion':
                    self.msj_error_conexion()
                    return
                else:
                    self.datos.append(temp)
            if max(self.datos):
                self.datos_porcentual = [valor*100/max(self.datos)  for valor in self.datos]
            else:
                self.datos_porcentual = [0 for valor in self.datos]
            self.datos_x_angulo = [int(self.cmb_AnguloInicial.currentText())-i*0.02 for i in range(len(self.datos_porcentual))]
            self.datos_x_espacio = [ float(self.lnedit_lambda.text())/(2*sin(radians(angulo/2))) for angulo in self.datos_x_angulo]
            # HABRIA QUE IMPLEMENTAR UN GUARDADO TEMPORAL EN UN ARCHIVO 
            # POR SI OCURRE ALGO, PARA NO PERDER LOS DATOS DE LA MEDICION
            #with open('temporal.txt','a') as archivo_temporal:
            #    archivo_temporal.write( "%.2f" % self.datos_x_angulo[i] + '\t' +  "%.2f" % self.datos[i] +'\t' + "%.4f" % self.datos_x_espacio[i] + '\n')
                
            if self.rbtn_Absoluto.isChecked():  #Opciones para visualizar eje Y en valor Absoluto
                self.ydatos = np.array(self.datos)
                self.VentanaPlot.setLabel('left','Valor', units='mV')
            else:                               #Opciones para visualizar eje Y en valor Relativo
                self.ydatos = np.array(self.datos_porcentual)
                self.VentanaPlot.setLabel('left','Porcentual', units='%')
            if self.rbtn_Espacio.isChecked():   #Opciones para visualizar eje X en espacio interplanar
                self.VentanaPlot.setLabel('bottom','Espacio Interplanar', units='Armstrong')
                self.VentanaPlot.invertX(False)
                self.xdatos = np.array(self.datos_x_espacio)
               # if not self.chk_Autoscale.isChecked():
               #     self.VentanaPlot.setRange(xRange = (float(self.lnedit_lambda.text())/(2*sin(radians( int(self.cmb_AnguloFinal.currentText()) /2))),float(self.lnedit_lambda.text())/(2*sin(radians( int(self.cmb_AnguloFinal.currentText() )/2)))), disableAutoRange=True)
               # else:
               #     self.VentanaPlot.enableAutoRange=True
            else:                               #Opciones para visualizar eje X en grados
                self.xdatos = np.array(self.datos_x_angulo)
                self.VentanaPlot.setLabel('bottom','Angulo', units='grados')
                self.VentanaPlot.invertX(True)
               # if not self.chk_Autoscale.isChecked():
               #     self.VentanaPlot.setRange(xRange=(int(self.cmb_AnguloFinal.currentText()),int(self.cmb_AnguloInicial.currentText())), disableAutoRange=True)
               # else:
                #    self.VentanaPlot.enableAutoRange=True
            self.curve.setData(self.xdatos, self.ydatos)
            
            
                
    def mouseMoved(self,evt):
        """funcion que muestra un cursor en el grafico"""
        #print evt[0]
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
       # print pos
       # print self.VentanaPlot.sceneBoundingRect()
       # print self.VentanaPlot.sceneBoundingRect().contains(pos)
        if self.VentanaPlot.sceneBoundingRect().contains(pos):
            #print 'ventanaplot contiene a pos'
            mousePoint = self.vb.mapSceneToView(pos)
            #index = int(mousePoint.x())
            #print 'indice', index
            #print mousePoint.y() ,mousePoint.x()
            #if index > 0 and index < len(self.ydatos):
            #    print 'indice bien'
                #self.lbl_valX.setText('%0.3f' % mousePoint.x())
                #self.lbl_valY.setText('%0.3f' % self.ydatos[index])
                #self.lbl_valX.setText('%0.3f' % mousePoint.x())
                #label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            self.lbl_valX.setText('%0.3f' % mousePoint.x())
            self.lbl_valY.setText('%0.3f' % mousePoint.y())
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
        #    print self.ydatos        

    def msj_error_conexion(self):
        logger.error('El adquisidor no responde, comprobar conexion y puerto')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error de conexion")
        msg.setInformativeText("El adquisidor no responde.\n Compruebe que el adquisidor este\n encendido y conectado\n y que el puerto seleccionado sea el correcto.")
        msg.setWindowTitle("Error de conexion")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.btn_cerrar_conexion_clicked)
        retval = msg.exec_()
     #  print "value of pressed message box button:", retval
    
    def msj_error_nombre_muestra(self):
        logger.warning('Falta completar campo MUESTRA para iniciar adquisicion')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Datos incompletos")
        msg.setInformativeText("Debe completar el campo MUESTRA \npara poder comenzar con la adquisicion")
        msg.setWindowTitle("Datos incompletos")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        #msg.buttonClicked.connect(self.btn_cerrar_conexion_clicked)
        retval = msg.exec_()
     #  print "value of pressed message box button:", retval
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    MyWindow = MyWindowClass(None)
    MyWindow.show()
    app.exec_()
