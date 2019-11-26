import cv2

img = cv2.imread("img/imgGris.jpg", 1)
img2 = cv2.imread("img/img2Gris.jpg", 1)


cv2.imshow("a", img)
cv2.waitKey(0)