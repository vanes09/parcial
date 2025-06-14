#importo las librerias necesarias
import pydicom
import os
import cv2
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

    def transformacion_de_traslación(self, dx=210, dy=210):
        self.extraer_imagen()
        img = self.Imagen
        plt.figure(figsize=(10, 10))
        plt.subplot(1, 2, 1)
        plt.imshow(img, cmap='gray')
        plt.title('Imagen Original')
        MT =  np.float32([[1,0,dx],[0,1,dy]])
        tras = cv2.warpAffine(img, MT, (img.shape[1], img.shape[0]))
        plt.subplot(1, 2, 2)
        plt.title('Imagen Transformada')
        plt.imshow(tras, cmap='gray')

    def guardar_datos(self, ruta):
        pass


#Clase paciente, no se crearon los tributos solicitados, porque existe un método dentro de la clase Dicon que extrae los datos que se piden
class Paciente:
    def __init__(self, archivo_dicom):
        self.dicom= Dicom(archivo_dicom)

    def mostrar_datos(self):
        self.dicom.datos_pac()
    
    #def mostrar_imagen(self):
        #self.dicom.reconstruccion_3d()

class manejo_imagencv:
    def __init__(self, imagen):
        self.imagen = imagen

    def cargar_imagen(self):
        img = cv2.imread(os.getcwd() + '/'+ self.imagen)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
        plt.axis('off')
        plt.show()

    def binarizar_imagen(self, umbral=127):

    def guardar_imagen(self, ruta):
        cv2.imwrite(ruta, self.imagen)
