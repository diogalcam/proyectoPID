import cv2

img = cv2.imread("img/gaussImgGris.jpg", 1)
img2 = cv2.imread("img/gaussImg2Gris.jpg", 1)

for x in range(len(img)):
    for y in range(len(img[0])):
        if(img[x][y] != 255):
            img[x][y] = 0


cv2.imshow("Umbralización fondo blanco img1", img)
cv2.waitKey(0)
    