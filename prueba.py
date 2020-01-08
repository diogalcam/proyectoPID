import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
from pylab import *



# Cargamos la imagen
img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)
img = cv2.resize(img, (320, 320)) 
cv2.imshow("img", img)
 
# Convertimos a escala de grises
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gris2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gris,244,255,0)
ret2,thresh2 = cv2.threshold(gris2,244,255,0)
cv2.imshow("thresh", thresh) 
cv2.imshow("thresh2", thresh2)

# Aplicar suavizado Gaussiano
gauss = cv2.GaussianBlur(thresh, (5,5), 0)
gauss2 = cv2.GaussianBlur(thresh2, (5,5), 0) 
cv2.imshow("suavizado", gauss)
cv2.imshow("suavizado2", gauss2)

 
# Detectamos los bordes con Canny
canny = cv2.Canny(gauss, 0, 255)
canny2 = cv2.Canny(gauss2, 0, 255)
cv2.imshow("canny", canny)
cv2.imshow("canny2", canny2)
 
 
# Buscamos los contornos
(contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
(contornos2,_) = cv2.findContours(canny2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
print("He encontrado {} objetos".format(len(contornos)))
print("He encontrado {} objetos".format(len(contornos2)))
 
cv2.drawContours(img,contornos,-1,(0,0,255), 2)
cv2.drawContours(img2,contornos2,-1,(0,0,255), 2)
cv2.imshow("contornos", img)
cv2.imshow("contornos2", img2)


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
cv2.imshow("imggg",imagene)
print("Eje mayor y eje menor",ellipse[1])
print("(x,y)",ellipse[0])


cv2.waitKey(0)
