import cv2

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
        if(img4[x][y][0] < umbral2-4):
            img4[x][y] = 0


cv2.imshow("ff", img3)
cv2.imshow("ff2", img4)
cv2.waitKey(0)
