import pydicom
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from pydicom.data import get_testdata_file
from pydicom import dcmread
from clases import Dicom, Paciente, Manejo_imagencv

archivos_dicom = {}
pacientes = {}
imagenes = {}

while True:
    menu = input("""
    MENU PRINCIPAL
    a) Procesar archivos DICOM 
    b) Ingresar paciente 
    c) Añadir imagen JPG o PNG 
    d) Procesar imagen DICOM
    e) Binarizar y transformar imagen 
    f) Salir
    > """)
    if menu.lower() == 'a':
            ruta = input("Ruta del archivo DICOM (.dcm): ")
            if not os.path.exists(ruta):
                print("Archivo no encontrado.")
                continue
            dicom = Dicom(ruta)
            dicom.leer()
            nombre = os.path.basename(ruta)
            archivos_dicom[nombre] = dicom
            print('Archivo DICOM procesado:', nombre)
            break
    
    elif menu.lower() == 'b':
            ruta = input("Ruta del archivo DICOM (.dcm): ")
            nombre_paciente = input("Nombre del paciente: ")
            edad = input("Edad del paciente: ")
            ID = input("ID del paciente: ")
            paciente = Paciente(ruta,nombre_paciente, edad, ID)
            pacientes[nombre_paciente] = paciente
            dicom = Dicom(ruta)
            nombre = os.path.basename(ruta)
            archivos_dicom[nombre] = dicom
            paciente.guardar_pac(ruta, nombre_paciente, edad, ID)
            print('El archivo dicom usado fue guardado en el diccionario con éxito')
            print('Paciente guardado en el diccionario con éxito' )
            break
    
    elif menu.lower() == 'c':
          
    


    

