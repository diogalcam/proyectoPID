import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
from pylab import *



# Cargamos la imagen
img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)
img3 = cv2.imread("img/orange.jpg",1)
img = cv2.resize(img, (320, 320)) 
cv2.imshow("img", img)
cv2.imshow("naranja", img3) 
 
def convierteEscalaGrises(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


def binarizaImagen(imgGris,u1,u2,y):
    return cv2.threshold(imgGris,u1,u2,y)


def filtroGaussiano(imgBinarizada,mask,y):
    return cv2.GaussianBlur(imgBinarizada,mask,y)

 
def detectaBordes(imgSuavizado,u1,u2):
    return cv2.Canny(imgSuavizado,u1,u2)

 
def buscaContornos(imgBorde):
    return cv2.findContours(imgBorde.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


def dibujaContornos(imgNormal,imgContorno,u1,l,f1):
    return cv2.drawContours(imgNormal,imgContorno,u1,l,f1)


def puntosEje(imagen, ellipse):
    x1,x2,y1,y2,q,p,m,n = 0,0,0,0,0,0,0,0
    puntoCentralX = int(ellipse[0][0])
    puntoCentralY = int(ellipse[0][1])
    for x in range(1000):
        if(imagen[puntoCentralX + x][puntoCentralY] == 255):
            x1 = x
            break
        
    for x in range(1000):
        if(imagen[puntoCentralX - x][puntoCentralY] == 255):
            x2 = x
            break
    
    for y in range(1000):
        if(imagen[puntoCentralX][puntoCentralY + y] == 255):
            y1 = y
            break
        
    for y in range(1000):
        if(imagen[puntoCentralX][puntoCentralY - y] == 255):
            y2 = y
            break 
        
    if(x1>x2):
        m = x1
        n = x2
    else:
        m = x2
        n = x1
        
    if(y1>y2):
        q = y1
        p = y2
    else: 
        q = y2
        p = y1
     
    return (m,n,q,p)

def calculoVolumen(puntos):
    m, n, q, p = puntos[0], puntos[1], puntos[2], puntos[3]
    v1 = (1/6)*math.pi*n*math.pow(p+q, 2)
    v2 = (1/3)*math.pi*m*math.pow(p,2)
    v3 = (1/3)*math.pi*m*math.pow(q,2)
    return (v1+v2+v3)*math.pow(10, -6)

gris =  convierteEscalaGrises(img)
gris2 = convierteEscalaGrises(img2)
gris3 = convierteEscalaGrises(img3)

ret,thresh = binarizaImagen(gris, 244, 255, 0)
ret2,thresh2 = binarizaImagen(gris2, 244, 255, 0)
ret3,thresh3 = binarizaImagen(gris3, 244, 255, 0)

cv2.imshow("thresh", thresh) 
cv2.imshow("thresh2", thresh2)
cv2.imshow("thresh3", thresh3)

gauss = filtroGaussiano(thresh, (5,5), 0)
gauss2 = filtroGaussiano(thresh2, (5,5), 0)
gauss3 = filtroGaussiano(thresh3, (5,5), 0)

cv2.imshow("suavizado", gauss)
cv2.imshow("suavizado2", gauss2)
cv2.imshow("suavizado3", gauss3)

canny = detectaBordes(gauss, 0, 255)
canny2 = detectaBordes(gauss2, 0, 255)
canny3 = detectaBordes(gauss3, 0, 255)

cv2.imshow("canny", canny)
cv2.imshow("canny2", canny2)
cv2.imshow("canny3", canny3)

(contornos,_) = buscaContornos(canny)
(contornos2,_) = buscaContornos(canny2)
(contornos3,_) = buscaContornos(canny3)


dibujaContornos(img, contornos, -1, (0,0,255), 2)
dibujaContornos(img2, contornos2, -1, (0,0,255), 2)
dibujaContornos(img3, contornos3, -1, (0,0,255), 2)

cv2.imshow("contornos", img)
cv2.imshow("contornos2", img2)
cv2.imshow("contornos3", img3)



#momentos y centroide de la imagen de frente
m = cv2.moments(thresh)
print(m)
cX = int(m["m10"] / m["m00"])
cY = int(m["m01"] / m["m00"])

#momentos y centroide de la imagen de arriba
m2 = cv2.moments(thresh2)
print(m2)
cX2 = int(m2["m10"] / m2["m00"])
cY2 = int(m2["m01"] / m2["m00"])
 
centroide=cv2.circle(canny, (cX, cY), 5, (255, 255, 255), -1)
cv2.circle(canny2, (cX2, cY2), 5, (255, 255, 255), -1)
cv2.imshow("Image", canny)
cv2.imshow("Image2", canny2)


cnt = contornos[0]
area = cv2.contourArea(cnt)
print("Area",area)
ellipse = cv2.fitEllipse(cnt)
imagene=cv2.ellipse(img,ellipse,(0,255,0),2)
cv2.imshow("Imagen del mango con elipse",imagene)
print("Eje mayor y eje menor",ellipse[1])
print("(x,y)",ellipse[0])

cnt3 = contornos3[0]
area3 = cv2.contourArea(cnt3)
print("Area3",area3)
ellipse3 = cv2.fitEllipse(cnt3)
imagene3=cv2.ellipse(img3,ellipse3,(0,255,0),2)
cv2.imshow("Imagen de la naranja con elipse",imagene3)
print("Eje mayor y eje menor",ellipse3[1])
print("(x,y)",ellipse3[0])
        
puntos = puntosEje(canny, ellipse)
puntos3 = puntosEje(canny3, ellipse3)

volumen = calculoVolumen(puntos)
volumen3 = calculoVolumen(puntos3)
           
densidadMango = 10.90
masa = densidadMango * volumen
print("La masa estimada del mango esb-->",masa)

densidadNaranja = 11.00
masaNaranja = densidadNaranja * volumen3
print("La masa estimada de la naranja es -->",masaNaranja)

cv2.waitKey(0)
