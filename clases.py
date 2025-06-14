#importo las librerias necesarias
import pydicom
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
    def reconstruccion_3D(self, ruta_nifti):
        apilar = np.stack(self.Imagen, axis=-1)
        nifti = dicom2nifti.convert_directory(self.archivo,ruta_nifti)
        plotting.plot_anat(nifti, display_mode='ortho', title='Planos Axial, Sagital y Coronal')
        plt.show()
        

    
        
