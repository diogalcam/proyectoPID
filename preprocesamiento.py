import cv2
import os

directory= r"C:\Users\dioni\git\proyectoPID\img"

img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)

img = cv2.resize(img, (320, 320)) 

imgGris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img2Gris = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

medianaImgGris = cv2.medianBlur(imgGris, 3)
medianaImg2Gris = cv2.medianBlur(img2Gris, 3)

os.chdir(directory)
print("Before saving image:")   
print(os.listdir(directory)) #muestra directorio antes de guardar imagen

filename = "medianaImgGris.jpg"
filename2 = "medianaImg2Gris.jpg"
cv2.imwrite(filename, medianaImgGris)
cv2.imwrite(filename2,medianaImg2Gris)

print("After saving image:")   
print(os.listdir(directory))


#cv2.imshow("Mango de frente en escala de grises", imgGris)
#cv2.imshow("Mango desde arriba en escala de grises", img2Gris)
#cv2.imshow("Mango de frente en escala de grises con la mediana", medianaImgGris)
#cv2.imshow("Mango desde arriba en escala de grises con la mediana", medianaImg2Gris)

#cv2.waitKey(0)