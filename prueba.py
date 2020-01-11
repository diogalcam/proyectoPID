import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
 
def cambiaFondoBlanco(img):
    for x in range(len(img)):
        for y in range(len(img[0])):
            if img[x][y][0]==0:
                img[x][y] = 255 
    return img
 
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


# Cargamos la imagen
img = cv2.imread("img/naranja1-frente.jpg", 1)
img2 = cv2.imread("img/naranja1-arriba.jpg",1)
img3 = cv2.imread("img/naranja--frente.jpg",1)
img4 = cv2.imread("img/naranja--arriba.jpg", 1)
img = cv2.resize(img, (800, 600))
img2 = cv2.resize(img2, (800, 600))
img3 = cv2.resize(img3, (800, 600))
img4 = cv2.resize(img4, (800, 600))
naranja = cv2.imread("img/manzana-frente.jpg", 1)
manzana = cv2.imread("img/manzana-arriba.jpg",1)

cv2.imshow("img", img)
cv2.imshow("img2", img2)
#cv2.imshow("orange", img3) 
#cv2.imshow("orange arriba", img4) 
#cv2.imshow("manzana",manzana)


gris =  convierteEscalaGrises(img)
gris2 = convierteEscalaGrises(img2)
#gris3 = convierteEscalaGrises(img3)
#gris4 = convierteEscalaGrises(img4)
#grisManzana = convierteEscalaGrises(manzana)

ret,thresh = binarizaImagen(gris, 244, 255, 0)
ret2,thresh2 = binarizaImagen(gris2, 244, 255, 0)
#ret3,thresh3 = binarizaImagen(gris3, 244, 255, 0)
#ret4,thresh4 = binarizaImagen(gris4, 244, 255, 0)
#retM,threshManzana = binarizaImagen(grisManzana, 220, 255, 0)



cv2.imshow("thresh", thresh) 
cv2.imshow("thresh2", thresh2)
#cv2.imshow("thresh3", thresh3)
#cv2.imshow("thresh4", thresh4)
#cv2.imshow("threshManzana", threshManzana)


gauss = filtroGaussiano(thresh, (5,5), 0)
gauss2 = filtroGaussiano(thresh2, (5,5), 0)
#gauss3 = filtroGaussiano(thresh3, (7,7), 0)
#gauss4 = filtroGaussiano(thresh4, (7,7), 0)
#gaussManzana = filtroGaussiano(threshManzana, (5,5), 0)


cv2.imshow("suavizado", gauss)
cv2.imshow("suavizado2", gauss2)
#cv2.imshow("suavizado3", gauss3)
#cv2.imshow("suavizado4", gauss4)
#cv2.imshow("suavizadoManzana", gaussManzana)



canny = detectaBordes(gauss, 0, 255)
canny2 = detectaBordes(gauss2, 0, 255)
#canny3 = detectaBordes(gauss3, 0, 255)
#canny4 = detectaBordes(gauss4, 0, 255)
#cannyManzana = detectaBordes(gaussManzana, 0, 255)



cv2.imshow("canny", canny)
cv2.imshow("canny2", canny2)
#cv2.imshow("canny3", canny3)
#cv2.imshow("canny4", canny4)
#cv2.imshow("cannyManzana", cannyManzana)

(contornos,_) = buscaContornos(canny)
(contornos2,_) = buscaContornos(canny2)
#(contornos3,_) = buscaContornos(canny3)
#(contornos4,_) = buscaContornos(canny4)
#(contornosManzana,_) = buscaContornos(cannyManzana)


dibujaContornos(img, contornos, -1, (0,0,255), 2)
dibujaContornos(img2, contornos2, -1, (0,0,255), 2)
#dibujaContornos(img3, contornos3, -1, (0,0,255), 2)
#dibujaContornos(img4, contornos4, -1, (0,0,255), 2)
#dibujaContornos(manzana, contornosManzana, -1, (0,0,255), 2)

cv2.imshow("contornos", img)
cv2.imshow("contornos2", img2)
#cv2.imshow("contornos3", img3)
#cv2.imshow("contornos4", img4)
#cv2.imshow("contornosManzana", manzana)



#momentos y centroide de la imagen de frente
#m = cv2.moments(thresh)
#print(m)
#cX = int(m["m10"] / m["m00"])
#cY = int(m["m01"] / m["m00"])

#momentos y centroide de la imagen de arriba
#m2 = cv2.moments(thresh2)
#print(m2)
#cX2 = int(m2["m10"] / m2["m00"])
#cY2 = int(m2["m01"] / m2["m00"])
 
#centroide=cv2.circle(canny, (cX, cY), 5, (255, 255, 255), -1)
#cv2.circle(canny2, (cX2, cY2), 5, (255, 255, 255), -1)
#cv2.imshow("Image", canny)
#cv2.imshow("Image2", canny2)






cnt = contornos[0]
area = cv2.contourArea(cnt)
print("Area",area)
ellipse = cv2.fitEllipse(cnt)
imagene=cv2.ellipse(img,ellipse,(0,255,0),2)
cv2.imshow("Imagen del mango con elipse",imagene)
print("Eje mayor y eje menor",ellipse[1])
print("(x,y)",ellipse[0])

cnt2 = contornos2[0]
area2 = cv2.contourArea(cnt2)
print("Area",area2)
ellipse2 = cv2.fitEllipse(cnt2)
imagene2=cv2.ellipse(img2,ellipse2,(0,255,0),2)
cv2.imshow("Imagen del mango con elipse2",imagene2)
print("Eje mayor y eje menor",ellipse2[1])
print("(x,y)",ellipse2[0])

#cnt3 = contornos3[0]
#cnt4 = contornos4[0]
#area3 = cv2.contourArea(cnt3)
#area4 = cv2.contourArea(cnt4)
#print("Area3",area3)
#ellipse3 = cv2.fitEllipse(cnt3)
#imagene3=cv2.ellipse(img3,ellipse3,(0,255,0),2)
#ellipse4 = cv2.fitEllipse(cnt4)
#imagene4=cv2.ellipse(img4,ellipse4,(0,255,0),2)
#cv2.imshow("Imagen de la naranja con elipse",imagene3)
#print("Eje mayor y eje menor",ellipse3[1])
#print("(x,y)",ellipse3[0])
#cv2.imshow("Imagen de la naranja con elipse",imagene4)
#print("Eje mayor y eje menor",ellipse4[1])
#print("(x,y)",ellipse4[0])


def calculoVolumenes(ejes1, ejes2):
    A = int(ejes1[0])
    B = int(ejes1[1])
    C = int(ejes2[0])
    D = int(ejes2[1])
    #C = (B / D) * C
    calculo = 4*math.pi*A*B*C
    print(A,B,C,D)
    return calculo

volumenMango = calculoVolumenes(ellipse[1], ellipse2[1])
print("El volumen en pixeles cubicos es:", volumenMango)


densidadMediaNaranja = 2.34*(math.pow(10, -6))
print("La masa de la naranja es: ", volumenMango * densidadMediaNaranja)

masaMango = 360

print("La densidad del mango es ", masaMango/volumenMango, " gr/pixel cubico")

#volNaranja = calculoVolumenes(ellipse3[1], ellipse4[1])
#print("Volumen de la naranja", volNaranja)
#print("-------------------------------------")

#cntManzana = contornosManzana[0]
#areaManzana = cv2.contourArea(cntManzana)
#print("Area3 de la manzana --> ",areaManzana)
#ellipseManzana = cv2.fitEllipse(cntManzana)
#imagenManzana=cv2.ellipse(manzana,ellipseManzana,(0,255,0),2)
#cv2.imshow("Imagen de la manzana con elipse",imagenManzana)
#print("Eje mayor y eje menor",ellipseManzana[1])
#print("(x,y)",ellipseManzana[0])

def redondez(contorno):
    cnt= contorno[0]
    area = cv2.contourArea(cnt)
    perimetro = cv2.arcLength(cnt, True)
    print(area, perimetro)
    resultado = 4* math.pi *(area / perimetro)
    return resultado

#print("La redondez es", redondez(contornos))

def excentricidad(ellipse):
    ejeMayor = ellipse[1][0]
    ejeMenor = ellipse[1][1]
    resultado = math.sqrt(math.pow(ejeMayor, 2) * math.pow(ejeMenor, 2)) / ejeMayor
    return resultado

#print("La excentricidad es", excentricidad(ellipseManzana))

def tipoDeFruta(redondez, excentricidad):
    tipo = 0
    if(redondez < 680):
        tipo = "Manzana"
    elif(redondez > 680 and redondez < 820):
        tipo = "Mango"
    else:
        tipo = "Naranja"
    return tipo
        
        
#rMango = redondez(contornos)
#eMango = excentricidad(ellipse)
#rNaranja = redondez(contornos3)
#eNaranja = excentricidad(ellipse3)
#rManzana = redondez(contornosManzana)
#eManzana = excentricidad(ellipseManzana)
#print("La fruta es:", tipoDeFruta(rMango, eMango))
#print("La fruta es:", tipoDeFruta(rNaranja, eNaranja))
#print("La fruta es:", tipoDeFruta(rManzana, eManzana))



#puntos = puntosEje(canny, ellipse)
#puntos3 = puntosEje(canny3, ellipse3)
#puntosManzana = puntosEje(cannyManzana,ellipseManzana)


#volumen = calculoVolumen(puntos)
#volumen3 = calculoVolumen(puntos3)
#volumenManzana = calculoVolumen(puntosManzana)
           
#densidadMango = 10.907
#masa = densidadMango * volumen
#print("La masa estimada del mango esb-->",masa)

#densidadNaranja = 11.00
#masaNaranja = densidadNaranja * volumen3
#print("La masa estimada de la naranja es -->",masaNaranja)

#densidadManzana = 10.00
#masaManzana = densidadManzana * volumenManzana
#print("La masa estimada de la manzana es -->",masaManzana)

cv2.waitKey(0)
