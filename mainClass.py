import cv2

print(cv2.__version__)

img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)


print(img2.shape)