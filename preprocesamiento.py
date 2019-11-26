import cv2
import os

directory= r"C:\Users\dioni\git\proyectoPID\img"

img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)

img = cv2.resize(img, (320, 320)) 

imgGris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img2Gris = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#medianaImgGris = cv2.medianBlur(imgGris, 3)
#medianaImg2Gris = cv2.medianBlur(img2Gris, 3)

blur = cv2.GaussianBlur(imgGris,(3,3),0)
blur2 = cv2.GaussianBlur(img2Gris,(3,3),0)

ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("fff",th3)
cv2.waitKey(0)

os.chdir(directory)
print("Before saving image:")   
print(os.listdir(directory)) #muestra directorio antes de guardar imagen

filename = "gaussImgGris.jpg"
filename2 = "gaussImg2Gris.jpg"
cv2.imwrite(filename, blur)
cv2.imwrite(filename2,blur2)

print("After saving image:")   
print(os.listdir(directory))


#cv2.imshow("Mango de frente en escala de grises", imgGris)
#cv2.imshow("Mango desde arriba en escala de grises", img2Gris)
#cv2.imshow("Mango de frente en escala de grises con la mediana", medianaImgGris)
#cv2.imshow("Mango desde arriba en escala de grises con la mediana", medianaImg2Gris)

#cv2.waitKey(0)