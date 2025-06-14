#importo las librerias necesarias
import pydicom
import os
from pydicom.data import get_testdata_file
from pydicom import dcmread
import dicom2nifti
import matplotlib.pyplot as plt
from nilearn import plotting, image 
import numpy as np


#creo la clase dicom para manejar los archivos DICOM
class Dicom:
    def __init__(self, archivo, DS, Imagen):
        self.archivo = archivo
        self.DS = DS
        self.Imagen = Imagen 

    # Método para leer el archivo DICOM
    def leer(self):
        self.DS = pydicom.dcmread(self.archivo)
        return self.DS

    # Método para extraer la imagen del archivo DICOM y mostrala
    def extraer_imagen(self):
        self.Imagen = self.DS.pixel_array
        plt.imshow(self.Imagen, cmap='gray')
        plt.axis('off')

    #Método para convertir el archivo DICOM a NIfTI
    def planos(self, ruta_nifti):
        nifti = dicom2nifti.convert_directory(self.archivo,ruta_nifti)
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        #plano axial solo tres cortes
        plotting.plot_anat(nifti, display_mode='z', cut_coords=[-10, 0, 10], title='Plano axial',axes=axes[0],figure=fig)
        #plano sagital solo tres cortes
        plotting.plot_anat(nifti, display_mode='x', cut_coords=[-10, 0, 10], title='Plano sagital',axes=axes[1],figure=fig)
        #plano coronal solo tres cortes
        plotting.plot_anat(nifti, display_mode='y', cut_coords=[-10, 0, 10],title='Plano coronal',axes=axes[2],figure=fig)
        plt.show()

    def reconstruccion_3d(self):
        pass

    def datos_pac(self):
        if self.DS is None:
            print("No hay datos cargados")
        else:
            try:
                Nombre = self.DS.PatientName
                edad = self.DS.PatientAge
                ID = self.DS.PatientID
                print ( "Nombre del paciente: " , Nombre)
                print ( "Edad del paciente : " , edad)
                print ( "ID paciente: " , ID)
            except KeyError:
                print("No se encontró al paciente en el archivo.")


    def guardar_datos(self, ruta):
        pass

    class Paciente:
        def __init__(self, archivo_dicom):
            self.dicom= Dicom(archivo_dicom)

        def mostrar_datos(self):
            self.dicom.datos_pac()
        
        def mostrar_imagen(self):
            self.dicom.reconstruccion_3d()

