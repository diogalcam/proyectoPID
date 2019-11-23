import cv2

print(cv2.__version__)

img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)

cv2.imshow("Mango de frente",img)
cv2.imshow("Mango desde arriba",img2)
cv2.waitKey(0)