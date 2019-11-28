import cv2

print(cv2.__version__)

img = cv2.imread("img/mango-de-frente.png", 1)
img2 = cv2.imread("img/mango-top.jpg",1)

img3 = cv2.imread("img/gaussImgGris.jpg", 1)
img4 = cv2.imread("img/gaussImg2Gris.jpg", 1)

for x in range(len(img3)):
    for y in range(len(img3[0])):
        if(img3[x][y][0] < 240):
            img3[x][y] = 0


for x in range(len(img4)):
    for y in range(len(img4[0])):
        if(img4[x][y][0] < 240):
            img4[x][y] = 0


cv2.imshow("ff", img3)
cv2.imshow("ff2", img4)
cv2.waitKey(0)

print(img2.shape)