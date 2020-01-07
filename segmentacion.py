import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)

img3 = cv2.imread("img/gaussImgGris.jpg", 1)
img4 = cv2.imread("img/gaussImg2Gris.jpg", 1)

def buscaMinimoBlanco(imagen):
    filas,columnas,d = imagen.shape
    for i in range(filas):
        for j in range(columnas):
            pixel = imagen[i,j]
            minimo= min(pixel)
    return minimo



umbral = buscaMinimoBlanco(img3)
for x in range(len(img3)):
    for y in range(len(img3[0])):  
        if(img3[x][y][0] < umbral-4):
            img3[x][y] = 0

umbral2 = buscaMinimoBlanco(img4)
for x in range(len(img4)):
    for y in range(len(img4[0])):
        if(img4[x][y][0] < umbral2-15):
            img4[x][y] = 0
        
print(umbral)
print(umbral2)

def contorno(imagen):
    imagenCopia = imagen.copy()
    for x in range(len(imagen)):
        for y in range(len(imagen[0])):
            if(imagen[x][y][0] == 0):
                if(imagen[x-1][y-1][0] != 0 or imagen[x-1][y][0] != 0 or imagen[x-1][y+1][0] != 0 or imagen[x][y-1][0] != 0 
                   or imagen[x][y+1][0] != 0 or imagen[x+1][y-1][0] != 0 or imagen[x+1][y][0] != 0 or imagen[x+1][y+1][0] != 0 ):
                    imagenCopia[x][y] = 0
                else:
                    imagenCopia[x][y] = 255    
    
    for x in range(len(imagenCopia)):
        for y in range(len(imagenCopia[0])):
            if(imagenCopia[x][y][0] == 0):
                imagenCopia[x][y] = 255
            else:
                imagenCopia[x][y] = 0
    return imagenCopia
        
        
contornoImg1 = contorno(img3)
contornoImg2 = contorno(img4)



def centroide(imagen):
    sumaX = 0
    sumaY = 0
    cont = 0
    listaResultado = []
    for x in range(len(imagen)):
        for y in range(len(imagen[0])):
            if(imagen[x][y][0] == 255):
                sumaX += x
                sumaY += y
                cont += 1
                
    sumaX = int((sumaX / cont))
    sumaY = int((sumaY / cont))
    
    listaResultado.append(sumaX)
    listaResultado.append(sumaY)
    return listaResultado

def dibujaCentroide(imagen, lista):
    imagen[lista[0], lista[1]] = 255
    return imagen

contornoImg1 = dibujaCentroide(contornoImg1, centroide(contornoImg1))
contornoImg2 = dibujaCentroide(contornoImg2, centroide(contornoImg2))


def distanciaEuclidea(lista1,lista2):
    return math.sqrt((lista2[0]-lista1[0])**2+(lista2[1]-lista1[1])**2)


listaAux = []
for x in range(len(contornoImg1)):
    for y in range(len(contornoImg1[0])):
        if contornoImg1[x][y][0] >= 240:
            listaAux.append([x,y])
            
c1=centroide(contornoImg1)





#cv2.imshow("Contorno Dibujado 1", contornoImg1)
#cv2.imshow("Contorno Dibujado 2", contornoImg2)
#cv2.waitKey(0)
