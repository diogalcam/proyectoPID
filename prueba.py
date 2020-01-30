import cv2
import math

 
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

def calculoVolumenes(ejes1, ejes2):
    A = int(ejes1[0])
    B = int(ejes1[1])
    C = int(ejes2[0])
    calculo = 4*math.pi*A*B*C
    return calculo

def redondez(contorno):
    cnt= contorno[0]
    area = cv2.contourArea(cnt)
    perimetro = cv2.arcLength(cnt, True)
    resultado = 4* math.pi *(area / math.pow(perimetro,2))
    return resultado

def excentricidad(ellipse):
    ejeMayor = ellipse[1][0]
    ejeMenor = ellipse[1][1]
    resultado = 0
    if(ejeMenor < ejeMayor):
        resultado = math.sqrt(math.pow(ejeMayor, 2) - math.pow(ejeMenor, 2)) / ejeMayor
    else:
        resultado = math.sqrt(math.pow(ejeMenor, 2) - math.pow(ejeMayor, 2)) / ejeMenor
    return resultado

def tipoDeFruta(redondez, excentricidad):
    media = redondez*excentricidad
    tipo = 0
    if(media > 0.51):
        tipo = "Mango"
    elif(media > 0.31 and media < 0.5):
        tipo = "Naranja"
    else:
        tipo = "Manzana"
    return tipo

def densidadFruta(fruta):
    densidad = 0
    if(fruta == "Naranja"):
        densidad = 2.35*(math.pow(10, -6))
    elif(fruta == "Mango"):
        densidad = 2.32*math.pow(10, -6)
    else:
        densidad = 2.17*math.pow(10, -6)
    return densidad
        
# Cargamos la imagen
img = cv2.imread("img/naranja2-frente.jpg", 1)
img2 = cv2.imread("img/naranja2-arriba.jpg",1)
img = cv2.resize(img, (800, 600))
img2 = cv2.resize(img2, (800, 600))

cv2.imshow("img", img)
cv2.imshow("img2", img2)

gris =  convierteEscalaGrises(img)
gris2 = convierteEscalaGrises(img2)

cv2.imshow("gris", gris)
cv2.imshow("gris2", gris2)

ret,thresh = binarizaImagen(gris, 244, 255, 0)
ret2,thresh2 = binarizaImagen(gris2, 244, 255, 0)

cv2.imshow("thresh", thresh) 
cv2.imshow("thresh2", thresh2)



canny = detectaBordes(thresh, 0, 255)
canny2 = detectaBordes(thresh2, 0, 255)

cv2.imshow("canny", canny)
cv2.imshow("canny2", canny2)

(contornos,_) = buscaContornos(canny)
(contornos2,_) = buscaContornos(canny2)

dibujaContornos(img, contornos, -1, (0,0,255), 2)
dibujaContornos(img2, contornos2, -1, (0,0,255), 2)

cv2.imshow("contornos", img)
cv2.imshow("contornos2", img2)

cnt = contornos[0]
ellipse = cv2.fitEllipse(cnt)
imagene=cv2.ellipse(img,ellipse,(0,255,0),2)
cv2.imshow("Imagen del mango con elipse",imagene)

cnt2 = contornos2[0]
ellipse2 = cv2.fitEllipse(cnt2)
imagene2=cv2.ellipse(img2,ellipse2,(0,255,0),2)
cv2.imshow("Imagen del mango con elipse2",imagene2)
 
redondez1 = redondez(contornos)
excentricidad1 = excentricidad(ellipse)
fruta = tipoDeFruta(redondez1, excentricidad1)
densidad = densidadFruta(fruta)
volumen = calculoVolumenes(ellipse[1], ellipse2[1])
masa = volumen * densidad

media = redondez1 * excentricidad1
print(redondez1, excentricidad1, media)

print("La fruta proporcionada es:", fruta)
print("El volumen es:", volumen, "pixeles cubicos")
print("La densidad es:", densidad, "gramos/pixeles cubicos")
print("La masa de es:", masa,"gramos")
cv2.waitKey(0)
