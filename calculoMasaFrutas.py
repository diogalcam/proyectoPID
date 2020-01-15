import cv2
import math
import msvcrt

def cambiaFondoBlanco(imgMangoFrente1):
    for x in range(len(imgMangoFrente1)):
        for y in range(len(imgMangoFrente1[0])):
            if imgMangoFrente1[x][y][0]==0:
                imgMangoFrente1[x][y] = 255 
    return imgMangoFrente1
 
def convierteEscalaGrises(imgMangoFrente1):
    return cv2.cvtColor(imgMangoFrente1,cv2.COLOR_BGR2GRAY)

def binarizaImagen(imgMangoFrente1Gris,u1,u2,y):
    return cv2.threshold(imgMangoFrente1Gris,u1,u2,y)

def filtroGaussiano(imgMangoFrente1Binarizada,mask,y):
    return cv2.GaussianBlur(imgMangoFrente1Binarizada,mask,y)

def detectaBordes(imgMangoFrente1Suavizado,u1,u2):
    return cv2.Canny(imgMangoFrente1Suavizado,u1,u2)

def buscaContornos(imgCanny):
    return cv2.findContours(imgCanny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def dibujaContornos(imgMangoFrente1Normal,imgMangoFrente1Contorno,u1,l,f1):
    return cv2.drawContours(imgMangoFrente1Normal,imgMangoFrente1Contorno,u1,l,f1)

def puntosEje(imagen, ellipse):
    x1,x2,y1,y2,q,p,m,n = 0,0,0,0,0,0,0,0
    puntoCentralX = int(ellipse[0][0])
    puntoCentralY = int(ellipse[0][1])
    for x in range(1000):
        if(imagen[puntoCentralX + x][puntoCentralY] == 255):
            x1 = x
            break
        
    for x in range(1000):
        if(imagen[puntoCentralX - x][puntoCentralY] == 255):
            x2 = x
            break
    
    for y in range(1000):
        if(imagen[puntoCentralX][puntoCentralY + y] == 255):
            y1 = y
            break
        
    for y in range(1000):
        if(imagen[puntoCentralX][puntoCentralY - y] == 255):
            y2 = y
            break 
        
    if(x1>x2):
        m = x1
        n = x2
    else:
        m = x2
        n = x1
        
    if(y1>y2):
        q = y1
        p = y2
    else: 
        q = y2
        p = y1
     
    return (m,n,q,p)



def calculoVolumenes(ejes1, ejes2):
    A = int(ejes1[0])
    B = int(ejes1[1])
    C = int(ejes2[0])
    calculo = 4*math.pi*A*B*C
    return calculo

def calculaElipse(contorno,imagen):
    cnt = contorno[0]
    ellipse = cv2.fitEllipse(cnt)
    return ellipse

def excentricidad(ellipse):
    ejeMayor = ellipse[1][0]
    ejeMenor = ellipse[1][1]
    resultado = 0
    if(ejeMenor < ejeMayor):
        resultado = math.sqrt(math.pow(ejeMayor, 2) - math.pow(ejeMenor, 2)) / ejeMayor
    else:
        resultado = math.sqrt(math.pow(ejeMenor, 2) - math.pow(ejeMayor, 2)) / ejeMenor
    return resultado

def tipoDeFruta(redondez, excentricidad):
    media = redondez*excentricidad
    tipo = 0
    if(media > 0.51):
        tipo = "Mango"
    elif(media > 0.31 and media < 0.5):
        tipo = "Naranja"
    else:
        tipo = "Manzana"
    return tipo


def redondez(contorno):
    cnt= contorno[0]
    area = cv2.contourArea(cnt)
    perimetro = cv2.arcLength(cnt, True)
    resultado = 4* math.pi *(area / math.pow(perimetro,2))
    return resultado

def densidadFruta(fruta):
    densidad = 0
    if(fruta == "Naranja"):
        densidad = 2.35*(math.pow(10, -6))
    elif(fruta == "Mango"):
        densidad = 2.32*math.pow(10, -6)
    else:
        densidad = 2.17*math.pow(10, -6)
    return densidad

def menu():
    """Funcion que Muestra el Menu"""
    print("""************

************
Selecciona la fruta para calcular su masa
1)  mango
2)  mango2
3)  mango3
4)  manzana
5)  manzana2
6)  manzana3
7)  naranja
8)  naranja2
9)  naranja3

""")
    
#base de datos fija
imgMangoFrente1 = cv2.imread("img/mango-frente.jpg", 1)
imgMangoArriba1 = cv2.imread("img/mango-arriba.jpg",1)
imgMangoFrente1 = cv2.resize(imgMangoFrente1, (800, 600))
imgMangoArriba1 = cv2.resize(imgMangoArriba1, (800, 600))
imgMangoFrente2 = cv2.imread("img/mango2-frente.jpg", 1)
imgMangoArriba2 = cv2.imread("img/mango2-arriba.jpg",1)
imgMangoFrente2 = cv2.resize(imgMangoFrente2, (800, 600))
imgMangoArriba2 = cv2.resize(imgMangoArriba2, (800, 600))
imgMangoFrente3 = cv2.imread("img/mango3-frente.jpg", 1)
imgMangoArriba3 = cv2.imread("img/mango3-arriba.jpg",1)  
imgMangoFrente3 = cv2.resize(imgMangoFrente3, (800, 600))
imgMangoArriba3 = cv2.resize(imgMangoArriba3, (800, 600))
imgManzanaFrente1 = cv2.imread("img/manzana1-frente.jpg", 1)
imgManzanaArriba1 = cv2.imread("img/manzana1-arriba.jpg",1)
imgManzanaFrente1 = cv2.resize(imgManzanaFrente1, (800, 600))
imgManzanaArriba1 = cv2.resize(imgManzanaArriba1, (800, 600))
imgManzanaFrente2 = cv2.imread("img/manzana2-frente.jpg", 1)
imgManzanaArriba2 = cv2.imread("img/manzana2-arriba.jpg",1)
imgManzanaFrente2 = cv2.resize(imgManzanaFrente2, (800, 600))
imgManzanaArriba2 = cv2.resize(imgManzanaArriba2, (800, 600))
imgManzanaFrente3 = cv2.imread("img/manzana3-frente.jpg", 1)
imgManzanaArriba3 = cv2.imread("img/manzana3-arriba.jpg",1)
imgManzanaFrente3 = cv2.resize(imgManzanaFrente3, (800, 600))
imgManzanaArriba3 = cv2.resize(imgManzanaArriba3, (800, 600))
imgNaranjaFrente1 = cv2.imread("img/naranja1-frente.jpg", 1)
imgNaranjaArriba1 = cv2.imread("img/naranja1-arriba.jpg",1)
imgNaranjaFrente1 = cv2.resize(imgNaranjaFrente1, (800, 600))
imgNaranjaArriba1 = cv2.resize(imgNaranjaArriba1, (800, 600))
imgNaranjaFrente2 = cv2.imread("img/naranja2-frente.jpg", 1)
imgNaranjaArriba2 = cv2.imread("img/naranja2-arriba.jpg",1)
imgNaranjaFrente2 = cv2.resize(imgNaranjaFrente2, (800, 600))
imgNaranjaArriba2 = cv2.resize(imgNaranjaArriba2, (800, 600))
imgNaranjaFrente3 = cv2.imread("img/naranja3-frente.jpg", 1)
imgNaranjaArriba3 = cv2.imread("img/naranja3-arriba.jpg",1)
imgNaranjaFrente3 = cv2.resize(imgNaranjaFrente3, (800, 600))
imgNaranjaArriba3 = cv2.resize(imgNaranjaArriba3, (800, 600))


def programaCompleto(img,img2,pesoReal):
    
            
    #muestra imagen de frente y arriba
    cv2.imshow("img de frente", img)
    cv2.imshow("img de arriba", img2)
    cv2.waitKey(0)
            
    #convierte escala de grises
    gris =  convierteEscalaGrises(img)
    gris2 = convierteEscalaGrises(img2)
            
    #binariza la imagen con umbral minimo y maximo
    ret,thresh = binarizaImagen(gris, 244, 255, 0)
    ret2,thresh2 = binarizaImagen(gris2, 244, 255, 0)       
            
    #muestra mangoElipse1s binarizadas
    cv2.imshow("thresh", thresh) 
    cv2.imshow("thresh2", thresh2)
            
    cv2.waitKey(0)
            
    #aplicamos filtros gaussianos para eliminar el posible ruido
    gauss = filtroGaussiano(thresh, (5,5), 0)
    gauss2 = filtroGaussiano(thresh2, (5,5), 0)  
            
    #muestra mangoElipse1s con el filtro de gauss aplicados
    cv2.imshow("suavizado", gauss)
    cv2.imshow("suavizado2", gauss2)
            
    cv2.waitKey(0)
            
    #Aplicamos Canny para la deteccion de los bordes 
    canny = detectaBordes(gauss, 0, 255)
    canny2 = detectaBordes(gauss2, 0, 255)
            
    #mostramos las mangoElipse1s aplicadas con Canny
    cv2.imshow("canny", canny)
    cv2.imshow("canny2", canny2) 
            
    cv2.waitKey(0)
    #Buscamos los posibles contornos , ya que , que sea un borde no quiere
    #decir que sea un contorno
    (contornos,_) = buscaContornos(canny)
    (contornos2,_) = buscaContornos(canny2)
            
    #Dibujamos contornos 
    dibujaContornos(img, contornos, -1, (0,0,255), 2)
    dibujaContornos(img2, contornos2, -1, (0,0,255), 2)
            
    #mostramos los contornos de cada imagen
    cv2.imshow("contornos", img)
    cv2.imshow("contornos2", img2)
    cv2.waitKey(0)
            
    mangoElipse1=cv2.ellipse(img,calculaElipse(contornos, img),(0,255,0),2)
    cv2.imshow("Imagen con elipse",mangoElipse1)
    mangoElipse2=cv2.ellipse(img2,calculaElipse(contornos2, img2),(0,255,0),2)
    cv2.imshow("Imagen desde arriba con elipse",mangoElipse2)
            
    cv2.waitKey(0)
    #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
    print() 
    print("Eje mayor y eje menor",calculaElipse(contornos, img)[1])
    print("(x,y)",calculaElipse(contornos, img)[0])  
    print()
    print("Eje mayor y eje menor desde arriba",calculaElipse(contornos2, img2)[1])
    print("(x,y)",calculaElipse(contornos2, img2)[0])
    print()
            
    #calculamos la redondez y excentricidad para luego hacer una media y detectar el tipo de fruta
    redondez1 = redondez(contornos)
    excentricidad1 = excentricidad(calculaElipse(contornos, img))
            
    #miramos que tipo de fruta es
    fruta = tipoDeFruta(redondez1, excentricidad1)
            
    #el calculo de la densidad es la media de las densidades de cada tipo de fruta correspondiente
    #la densidad es el numero de gramos que tiene un pixel cubico de media
    densidad = densidadFruta(fruta)
            
    #volumen en pixeles cubicos ( contar los pixeles que ocupa cada fruta )
    volumen = calculoVolumenes(calculaElipse(contornos, img)[1],calculaElipse(contornos2, img2)[1])
    masa = volumen * densidad
    media = redondez1 * excentricidad1
    print()
    print("La fruta proporcionada es:", fruta)
    print("El volumen es:", volumen, "pixeles cubicos")
    print("La densidad es:", densidad, "gramos/pixeles cubicos")
    print("La masa de es:", masa,"gramos")
            
    #calculo del error cometido
    print("La masa real es:",pesoReal,"gramos")
    print("Error sobre el peso real y el calculado->",abs(pesoReal-masa),"gramos")         


def programa():
    aux = 0
    menu()
    aux = int(input("Selecione Opcion\n"))
    while(aux>0 and aux<=9):
        if aux==1:
            print()
            programaCompleto(imgMangoFrente1, imgMangoArriba1, 583)
            aux = int(input("Selecione Opcion\n"))           
        
        elif(aux==2):
            print()
            programaCompleto(imgMangoFrente2, imgMangoArriba2, 525)
            aux = int(input("Selecione Opcion\n"))    
        
        elif(aux==3):         
            print()
            programaCompleto(imgMangoFrente3, imgMangoArriba3, 443)
            aux = int(input("Selecione Opcion\n"))

        elif aux==4:
            print()
            programaCompleto(imgManzanaFrente1, imgManzanaArriba1, 214)
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==5:
            print()
            programaCompleto(imgManzanaFrente2, imgManzanaArriba2, 219)
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==6:    
            print()
            programaCompleto(imgManzanaFrente3, imgManzanaArriba3, 245)
            aux = int(input("Selecione Opcion\n"))
        
        elif aux==7:
            print()
            programaCompleto(imgNaranjaFrente1, imgNaranjaArriba1, 317)
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==8:
            print()
            programaCompleto(imgNaranjaFrente2, imgNaranjaArriba2, 360)
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==9:
            print()
            programaCompleto(imgNaranjaFrente3, imgNaranjaArriba3, 318)
            aux = int(input("Selecione Opcion\n"))
    
    
programa()

msvcrt.getch()