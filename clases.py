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
    def __init__(self, archivo, DS=None, Imagen=None):
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
        self.leer()
        self.dicoms = []
        imagenes = []
        lista = sorted(os.listdir(self.archivo))
        for archivo in lista:
            ruta = os.path.join(self.archivo, archivo)
            archivos_dicom = pydicom.dcmread(ruta)
            self.dicoms.append(archivos_dicom)
            imagenes.append(archivos_dicom.pixel_array)
        self.volumen = np.array(imagenes)
        return self.volumen

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
        self.imagen = cv2.imread(os.getcwd() + '/'+ self.imagen)
        self.imagen = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
        plt.imshow(self.imagen)
        plt.axis('off')
        plt.show()

    def binarizar_imagen(self, umbral=127, tipo_bin=cv2.THRESH_BINARY, dibujarfig = 'circulo'):
        self.cargar_imagen()
        img = self.imagen
        imgB = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        umbral, imgBin = cv2.threshold(imgB, umbral, 255, tipo_bin)
        copiaimgBin = imgBin.copy()
        if dibujarfig == 'circulo':
            ImgBdibuj = cv2.circle(copiaimgBin,(255,255), 100, (0,0,255), 3)
            ImgBdibujycontext = cv2.putText(ImgBdibuj,f'Imagen binarizada\nUmbral: {umbral}',(255,255), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,0),2,cv2.LINE_AA)
        else:
            ImgBdibuj =  cv2.rectangle(copiaimgBin,(300,500),(210,360),(255,0,0), 3)
            ImgBdibujycontext = cv2.putText(ImgBdibuj,f'Imagen binarizada\nUmbral: {umbral}',(250,250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,0),2,cv2.LINE_AA)
        plt.imshow(ImgBdibujycontext, cmap='gray')
        plt.axis('off')
        plt.show()

    def transformacion_morfologica(self, tamaño_kernel= (5,5), umbral = 127, tipo_bin=cv2.THRESH_BINARY, TransMorf = cv2.erode):
        self.cargar_imagen()
        img = self.imagen
        imgB = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        umbral, imgBin = cv2.threshold(imgB, umbral, 255, tipo_bin)
        kernel = np.ones(tamaño_kernel, np.uint8)
        TM = TransMorf(imgBin, kernel)
        plt.imshow(TM, cmap='gray')
        plt.axis('off')
        plt.show()

    def guardar_imagen(self, ruta):
        cv2.imwrite(ruta, self.imagen)
