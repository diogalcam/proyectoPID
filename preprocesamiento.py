import cv2

img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)

imgGris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img2Gris = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

cv2.imwrite('/../img/imgGris.jpg', imgGris)
cv2.imwrite('/../img/img2Gris.jpg', img2Gris)

cv2.imshow("Mango de frente en escala de grises", imgGris)
cv2.imshow("Mango desde arriba en escala de grises", img2Gris)

cv2.waitKey(0)