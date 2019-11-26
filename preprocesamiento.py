import cv2

img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)

img = cv2.resize(img, (320, 320)) 

imgGris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img2Gris = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

medianaImgGris = cv2.medianBlur(imgGris, 3)
medianaImg2Gris = cv2.medianBlur(img2Gris, 3)

cv2.imwrite('/../img/medianaImgGris.jpg', medianaImgGris)
cv2.imwrite('/../img/medianaImg2Gris.jpg', medianaImg2Gris)

cv2.imshow("Mango de frente en escala de grises", imgGris)
cv2.imshow("Mango desde arriba en escala de grises", img2Gris)
cv2.imshow("Mango de frente en escala de grises con la mediana", medianaImgGris)
cv2.imshow("Mango desde arriba en escala de grises con la mediana", medianaImg2Gris)

cv2.waitKey(0)