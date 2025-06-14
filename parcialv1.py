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
            nombre_paciente = input("Nombre del paciente: ")
            edad = input("Edad del paciente: ")
            genero = input("Género del paciente: ")
            paciente = Paciente(nombre_paciente, edad, genero)
            pacientes[nombre_paciente] = paciente
            print('Paciente ingresado:', nombre_paciente)

    

