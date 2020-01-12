import cv2
import math
import msvcrt
import time

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

def buscaContornos(imgMangoFrente1Borde):
    return cv2.findContours(imgMangoFrente1Borde.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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



def programa():
    aux = 0
    menu()
    aux = int(input("Selecione Opcion\n"))
    while(aux>0 and aux<=9):
        if aux==1:
            imgMangoFrente1 = cv2.imread("img/mango-frente.jpg", 1)
            imgMangoArriba1 = cv2.imread("img/mango-arriba.jpg",1)
            
            imgMangoFrente1 = cv2.resize(imgMangoFrente1, (800, 600))
            imgMangoArriba1 = cv2.resize(imgMangoArriba1, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgMangoFrente1", imgMangoFrente1)
            cv2.imshow("imgMangoArriba1", imgMangoArriba1)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris =  convierteEscalaGrises(imgMangoFrente1)
            gris2 = convierteEscalaGrises(imgMangoArriba1)
            
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
            dibujaContornos(imgMangoFrente1, contornos, -1, (0,0,255), 2)
            dibujaContornos(imgMangoArriba1, contornos2, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos", imgMangoFrente1)
            cv2.imshow("contornos2", imgMangoArriba1)
            
            
            mangoElipse1=cv2.ellipse(imgMangoFrente1,calculaElipse(contornos, imgMangoFrente1),(0,255,0),2)
            cv2.imshow("Imagen del mango1 con elipse",mangoElipse1)
            mangoElipse2=cv2.ellipse(imgMangoArriba1,calculaElipse(contornos2, imgMangoArriba1),(0,255,0),2)
            cv2.imshow("Imagen del mango1 desde arriba con elipse",mangoElipse2)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print() 
            print("Eje mayor y eje menor",calculaElipse(contornos, imgMangoFrente1)[1])
            print("(x,y)",calculaElipse(contornos, imgMangoFrente1)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos2, imgMangoArriba1)[1])
            print("(x,y)",calculaElipse(contornos2, imgMangoArriba1)[0])
            print()
            
            #calculamos la redondez y excentricidad para luego hacer una media y detectar el tipo de fruta
            redondez1 = redondez(contornos)
            excentricidad1 = excentricidad(calculaElipse(contornos, imgMangoFrente1))
            
            #miramos que tipo de fruta es
            fruta = tipoDeFruta(redondez1, excentricidad1)
            
            #el calculo de la densidad es la media de las densidades de cada tipo de fruta correspondiente
            #la densidad es el numero de gramos que tiene un pixel cubico de media
            densidad = densidadFruta(fruta)
            
            #volumen en pixeles cubicos ( contar los pixeles que ocupa cada fruta )
            volumen = calculoVolumenes(calculaElipse(contornos, imgMangoFrente1)[1],calculaElipse(contornos2, imgMangoArriba1)[1])
            masa = volumen * densidad
            media = redondez1 * excentricidad1
            print(redondez1, excentricidad1, media)
            print("La fruta proporcionada es:", fruta)
            print("El volumen es:", volumen, "pixeles cubicos")
            print("La densidad es:", densidad, "gramos/pixeles cubicos")
            print("La masa de es:", masa,"gramos")
            
            #calculo del error cometido
            print("La masa real es:",583,"gramos")
            print("Error sobre el peso real y el calculado->",abs(583-masa),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))           
        
        elif(aux==2):
            imgMangoFrente2 = cv2.imread("img/mango2-frente.jpg", 1)
            imgMangoArriba2 = cv2.imread("img/mango2-arriba.jpg",1)
            
            imgMangoFrente2 = cv2.resize(imgMangoFrente2, (800, 600))
            imgMangoArriba2 = cv2.resize(imgMangoArriba2, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgMangoFrente2", imgMangoFrente2)
            cv2.imshow("imgMangoArriba2", imgMangoArriba2)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris3 =  convierteEscalaGrises(imgMangoFrente2)
            gris4 = convierteEscalaGrises(imgMangoArriba2)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh3 = binarizaImagen(gris3, 244, 255, 0)
            ret2,thresh4 = binarizaImagen(gris4, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh3", thresh3) 
            cv2.imshow("thresh4", thresh4)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss3 = filtroGaussiano(thresh3, (5,5), 0)
            gauss4 = filtroGaussiano(thresh4, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado", gauss3)
            cv2.imshow("suavizado2", gauss4)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny3 = detectaBordes(gauss3, 0, 255)
            canny4 = detectaBordes(gauss4, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny3", canny3)
            cv2.imshow("canny4", canny4) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos3,_) = buscaContornos(canny3)
            (contornos4,_) = buscaContornos(canny4)
            
            #Dibujamos contornos 
            dibujaContornos(imgMangoFrente2, contornos3, -1, (0,0,255), 2)
            dibujaContornos(imgMangoArriba2, contornos4, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos3", imgMangoFrente2)
            cv2.imshow("contornos4", imgMangoArriba2)
            
            
            mangoElipse3=cv2.ellipse(imgMangoFrente2,calculaElipse(contornos3, imgMangoFrente2),(0,255,0),2)
            cv2.imshow("Imagen del mango2 con elipse",mangoElipse3)
            mangoElipse4=cv2.ellipse(imgMangoArriba2,calculaElipse(contornos4, imgMangoArriba2),(0,255,0),2)
            cv2.imshow("Imagen del mango2 desde arriba con elipse",mangoElipse4)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print() 
            print("Eje mayor y eje menor",calculaElipse(contornos3, imgMangoFrente2)[1])
            print("(x,y)",calculaElipse(contornos3, imgMangoFrente2)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos4, imgMangoArriba2)[1])
            print("(x,y)",calculaElipse(contornos3, imgMangoArriba2)[0])
            print()
            
            redondez2 = redondez(contornos3)
            excentricidad2 = excentricidad(calculaElipse(contornos3, imgMangoFrente2))
            
            fruta2 = tipoDeFruta(redondez2, excentricidad2)
            densidad2 = densidadFruta(fruta2)
            
            volumen2 = calculoVolumenes(calculaElipse(contornos3, imgMangoFrente2)[1],calculaElipse(contornos4, imgMangoArriba2)[1])
            masa2 = volumen2 * densidad2
            media2 = redondez2 * excentricidad2
            print()
            print("Redondez,excentricidad y media->",redondez2, excentricidad2, media2)
            print("La fruta proporcionada es:", fruta2)
            print("El volumen es:", volumen2, "pixeles cubicos")
            print("La densidad es:", densidad2, "gramos/pixeles cubicos")
            print("La masa de es:", masa2,"gramos")
            print("La masa real es:",525,"gramos")
            print("Error sobre el peso real y el calculado->",abs(525-masa2),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))    
        
        elif(aux==3):
            imgMangoFrente3 = cv2.imread("img/mango3-frente.jpg", 1)
            imgMangoArriba3 = cv2.imread("img/mango3-arriba.jpg",1)
            
            imgMangoFrente3 = cv2.resize(imgMangoFrente3, (800, 600))
            imgMangoArriba3 = cv2.resize(imgMangoArriba3, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgMangoFrente3", imgMangoFrente3)
            cv2.imshow("imgMangoArriba3", imgMangoArriba3)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris5 =  convierteEscalaGrises(imgMangoFrente3)
            gris6 = convierteEscalaGrises(imgMangoArriba3)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh5 = binarizaImagen(gris5, 244, 255, 0)
            ret2,thresh6 = binarizaImagen(gris6, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh5", thresh5) 
            cv2.imshow("thresh6", thresh6)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss5 = filtroGaussiano(thresh5, (5,5), 0)
            gauss6 = filtroGaussiano(thresh6, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado5", gauss5)
            cv2.imshow("suavizado6", gauss6)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny5 = detectaBordes(gauss5, 0, 255)
            canny6 = detectaBordes(gauss6, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny5", canny6)
            cv2.imshow("canny5", canny6) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos5,_) = buscaContornos(canny5)
            (contornos6,_) = buscaContornos(canny6)
            
            #Dibujamos contornos 
            dibujaContornos(imgMangoFrente3, contornos5, -1, (0,0,255), 2)
            dibujaContornos(imgMangoArriba3, contornos6, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos5", imgMangoFrente3)
            cv2.imshow("contornos6", imgMangoArriba3)
            
            
            mangoElipse5=cv2.ellipse(imgMangoFrente3,calculaElipse(contornos5, imgMangoFrente3),(0,255,0),2)
            cv2.imshow("Imagen del mango3 con elipse",mangoElipse5)
            mangoElipse6=cv2.ellipse(imgMangoArriba3,calculaElipse(contornos6, imgMangoArriba3),(0,255,0),2)
            cv2.imshow("Imagen del mango3 desde arriba con elipse",mangoElipse6)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print() 
            print("Eje mayor y eje menor",calculaElipse(contornos5, imgMangoFrente3)[1])
            print("(x,y)",calculaElipse(contornos5, imgMangoFrente3)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos6, imgMangoArriba3)[1])
            print("(x,y)",calculaElipse(contornos6, imgMangoArriba3)[0])
            print()
            
            redondez3 = redondez(contornos5)
            excentricidad3 = excentricidad(calculaElipse(contornos5, imgMangoFrente3))
            
            fruta3 = tipoDeFruta(redondez3, excentricidad3)
            densidad3 = densidadFruta(fruta3)
            
            volumen3 = calculoVolumenes(calculaElipse(contornos5, imgMangoFrente3)[1],calculaElipse(contornos6, imgMangoArriba3)[1])
            masa3 = volumen3 * densidad3
            media3 = redondez3 * excentricidad3
            
            print("Redondez,excentricidad y media->",redondez3, excentricidad3, media3)
            print("La fruta proporcionada es:", fruta3)
            print("El volumen es:", volumen3, "pixeles cubicos")
            print("La densidad es:", densidad3, "gramos/pixeles cubicos")
            print("La masa de es:", masa3,"gramos")
            print("La masa real es:",443,"gramos")
            print("Error sobre el peso real y el calculado->",abs(443-masa3),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))
        
       
        elif aux==4:
            imgManzanaFrente1 = cv2.imread("img/manzana1-frente.jpg", 1)
            imgManzanaArriba1 = cv2.imread("img/manzana1-arriba.jpg",1)
            
            imgManzanaFrente1 = cv2.resize(imgManzanaFrente1, (800, 600))
            imgManzanaArriba1 = cv2.resize(imgManzanaArriba1, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgManzanaFrente1", imgManzanaFrente1)
            cv2.imshow("imgManzanaArriba1", imgManzanaArriba1)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris7 =  convierteEscalaGrises(imgManzanaFrente1)
            gris8 = convierteEscalaGrises(imgManzanaArriba1)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh7 = binarizaImagen(gris7, 244, 255, 0)
            ret2,thresh8 = binarizaImagen(gris8, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh7", thresh7) 
            cv2.imshow("thresh8", thresh8)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss7 = filtroGaussiano(thresh7, (5,5), 0)
            gauss8 = filtroGaussiano(thresh8, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado7", gauss7)
            cv2.imshow("suavizado8", gauss8)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny7 = detectaBordes(gauss7, 0, 255)
            canny8 = detectaBordes(gauss8, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny7", canny7)
            cv2.imshow("canny8", canny8) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos7,_) = buscaContornos(canny7)
            (contornos8,_) = buscaContornos(canny8)
            
            #Dibujamos contornos 
            dibujaContornos(imgManzanaFrente1, contornos7, -1, (0,0,255), 2)
            dibujaContornos(imgManzanaArriba1, contornos8, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos7", imgManzanaFrente1)
            cv2.imshow("contornos8", imgManzanaArriba1)
            
            
            mangoElipse7=cv2.ellipse(imgManzanaFrente1,calculaElipse(contornos7, imgManzanaFrente1),(0,255,0),2)
            cv2.imshow("Imagen de la manzana con elipse",mangoElipse7)
            mangoElipse8=cv2.ellipse(imgManzanaArriba1,calculaElipse(contornos8, imgManzanaArriba1),(0,255,0),2)
            cv2.imshow("Imagen del manzana desde arriba con elipse",mangoElipse8)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print()
            print("Eje mayor y eje menor",calculaElipse(contornos7, imgManzanaFrente1)[1])
            print("(x,y)",calculaElipse(contornos7, imgManzanaFrente1)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos8, imgManzanaArriba1)[1])
            print("(x,y)",calculaElipse(contornos8, imgManzanaArriba1)[0])
            print()
            
            redondez4 = redondez(contornos7)
            excentricidad4 = excentricidad(calculaElipse(contornos7, imgManzanaFrente1))
            
            fruta4 = tipoDeFruta(redondez4, excentricidad4)
            densidad4 = densidadFruta(fruta4)
            
            volumen4 = calculoVolumenes(calculaElipse(contornos7, imgManzanaFrente1)[1],calculaElipse(contornos8, imgManzanaArriba1)[1])
            masa4 = volumen4 * densidad4
            media4 = redondez4 * excentricidad4
            
            print("Redondez,excentricidad y media->",redondez4, excentricidad4, media4)
            print("La fruta proporcionada es:", fruta4)
            print("El volumen es:", volumen4, "pixeles cubicos")
            print("La densidad es:", densidad4, "gramos/pixeles cubicos")
            print("La masa de es:", masa4,"gramos")
            print("La masa real es:",214,"gramos")
            print("Error sobre el peso real y el calculado->",abs(214-masa4),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==5:
            imgManzanaFrente2 = cv2.imread("img/manzana2-frente.jpg", 1)
            imgManzanaArriba2 = cv2.imread("img/manzana2-arriba.jpg",1)
            
            imgManzanaFrente2 = cv2.resize(imgManzanaFrente2, (800, 600))
            imgManzanaArriba2 = cv2.resize(imgManzanaArriba2, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgManzanaFrente2", imgManzanaFrente2)
            cv2.imshow("imgManzanaArriba2", imgManzanaArriba2)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris9 =  convierteEscalaGrises(imgManzanaFrente2)
            gris10 = convierteEscalaGrises(imgManzanaArriba2)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh9 = binarizaImagen(gris9, 244, 255, 0)
            ret2,thresh10 = binarizaImagen(gris10, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh9", thresh9) 
            cv2.imshow("thresh10", thresh10)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss9 = filtroGaussiano(thresh9, (5,5), 0)
            gauss10 = filtroGaussiano(thresh10, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado9", gauss9)
            cv2.imshow("suavizado10", gauss10)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny9 = detectaBordes(gauss9, 0, 255)
            canny10 = detectaBordes(gauss10, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny9", canny9)
            cv2.imshow("canny10", canny10) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos9,_) = buscaContornos(canny9)
            (contornos10,_) = buscaContornos(canny10)
            
            #Dibujamos contornos 
            dibujaContornos(imgManzanaFrente2, contornos9, -1, (0,0,255), 2)
            dibujaContornos(imgManzanaArriba2, contornos10, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos9", imgManzanaFrente2)
            cv2.imshow("contornos10", imgManzanaArriba2)
            
            
            manzanaElipse=cv2.ellipse(imgManzanaFrente2,calculaElipse(contornos9, imgManzanaFrente2),(0,255,0),2)
            cv2.imshow("Imagen de la manzana2 con elipse",manzanaElipse)
            manzanaElipse2=cv2.ellipse(imgManzanaArriba2,calculaElipse(contornos10, imgManzanaArriba2),(0,255,0),2)
            cv2.imshow("Imagen de la manzana2 desde arriba con elipse",manzanaElipse2)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print() 
            print("Eje mayor y eje menor",calculaElipse(contornos9, imgManzanaFrente2)[1])
            print("(x,y)",calculaElipse(contornos9, imgManzanaFrente2)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos10, imgManzanaArriba2)[1])
            print("(x,y)",calculaElipse(contornos10, imgManzanaArriba2)[0])
            print()
            
            redondez5 = redondez(contornos9)
            excentricidad5 = excentricidad(calculaElipse(contornos9, imgManzanaFrente2))
            
            fruta5 = tipoDeFruta(redondez5, excentricidad5)
            densidad5 = densidadFruta(fruta5)
            
            volumen5 = calculoVolumenes(calculaElipse(contornos9, imgManzanaFrente2)[1],calculaElipse(contornos10, imgManzanaArriba2)[1])
            masa5 = volumen5 * densidad5
            media5 = redondez5 * excentricidad5
            
            print("Redondez,excentricidad y media->",redondez5, excentricidad5, media5)
            print("La fruta proporcionada es:", fruta5)
            print("El volumen es:", volumen5, "pixeles cubicos")
            print("La densidad es:", densidad5, "gramos/pixeles cubicos")
            print("La masa de es:", masa5,"gramos")
            print("La masa real es:",219,"gramos")
            print("Error sobre el peso real y el calculado->",abs(219-masa5),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==6:
            imgManzanaFrente3 = cv2.imread("img/manzana3-frente.jpg", 1)
            imgManzanaArriba3 = cv2.imread("img/manzana3-arriba.jpg",1)
            
            imgManzanaFrente3 = cv2.resize(imgManzanaFrente3, (800, 600))
            imgManzanaArriba3 = cv2.resize(imgManzanaArriba3, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgManzanaFrente3", imgManzanaFrente3)
            cv2.imshow("imgManzanaArriba3", imgManzanaArriba3)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris11 =  convierteEscalaGrises(imgManzanaFrente3)
            gris12 = convierteEscalaGrises(imgManzanaArriba3)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh11 = binarizaImagen(gris11, 244, 255, 0)
            ret2,thresh12 = binarizaImagen(gris12, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh11", thresh11) 
            cv2.imshow("thresh12", thresh12)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss11 = filtroGaussiano(thresh11, (5,5), 0)
            gauss12 = filtroGaussiano(thresh12, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado11", gauss11)
            cv2.imshow("suavizado12", gauss12)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny11 = detectaBordes(gauss11, 0, 255)
            canny12 = detectaBordes(gauss12, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny11", canny11)
            cv2.imshow("canny12", canny12) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos11,_) = buscaContornos(canny11)
            (contornos12,_) = buscaContornos(canny12)
            
            #Dibujamos contornos 
            dibujaContornos(imgManzanaFrente3, contornos11, -1, (0,0,255), 2)
            dibujaContornos(imgManzanaArriba3, contornos12, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos11", imgManzanaFrente3)
            cv2.imshow("contornos12", imgManzanaArriba3)
            
            
            manzanaElipse=cv2.ellipse(imgManzanaFrente3,calculaElipse(contornos11, imgManzanaFrente3),(0,255,0),2)
            cv2.imshow("Imagen de la manzana2 con elipse",manzanaElipse)
            manzanaElipse2=cv2.ellipse(imgManzanaArriba3,calculaElipse(contornos12, imgManzanaArriba3),(0,255,0),2)
            cv2.imshow("Imagen de la manzana2 desde arriba con elipse",manzanaElipse2)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print() 
            print("Eje mayor y eje menor",calculaElipse(contornos11, imgManzanaFrente3)[1])
            print("(x,y)",calculaElipse(contornos11, imgManzanaFrente3)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos12, imgManzanaArriba3)[1])
            print("(x,y)",calculaElipse(contornos12, imgManzanaArriba3)[0])
            print()
            
            redondez6 = redondez(contornos11)
            excentricidad6 = excentricidad(calculaElipse(contornos11, imgManzanaFrente3))
            
            fruta6 = tipoDeFruta(redondez6, excentricidad6)
            densidad6 = densidadFruta(fruta6)
            
            volumen6 = calculoVolumenes(calculaElipse(contornos11, imgManzanaFrente3)[1],calculaElipse(contornos12, imgManzanaArriba3)[1])
            masa6 = volumen6 * densidad6
            media6 = redondez6 * excentricidad6
            
            print("Redondez,excentricidad y media->",redondez5, excentricidad5, media5)
            print("La fruta proporcionada es:", fruta5)
            print("El volumen es:", volumen5, "pixeles cubicos")
            print("La densidad es:", densidad5, "gramos/pixeles cubicos")
            print("La masa de es:", masa5,"gramos")
            print("La masa real es:",245,"gramos")
            print("Error sobre el peso real y el calculado->",abs(245-masa5),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))
        
        elif aux==7:
            imgNaranjaFrente1 = cv2.imread("img/naranja1-frente.jpg", 1)
            imgNaranjaArriba1 = cv2.imread("img/naranja1-arriba.jpg",1)
            
            imgNaranjaFrente1 = cv2.resize(imgNaranjaFrente1, (800, 600))
            imgNaranjaArriba1 = cv2.resize(imgNaranjaArriba1, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgNaranjaFrente", imgNaranjaFrente1)
            cv2.imshow("imgNaranjaArriba", imgNaranjaArriba1)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris9 =  convierteEscalaGrises(imgNaranjaFrente1)
            gris10 = convierteEscalaGrises(imgNaranjaArriba1)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh9 = binarizaImagen(gris9, 244, 255, 0)
            ret2,thresh10 = binarizaImagen(gris10, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh9", thresh9) 
            cv2.imshow("thresh10", thresh10)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss9 = filtroGaussiano(thresh9, (5,5), 0)
            gauss10 = filtroGaussiano(thresh10, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado9", gauss9)
            cv2.imshow("suavizado10", gauss10)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny9 = detectaBordes(gauss9, 0, 255)
            canny10 = detectaBordes(gauss10, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny9", canny9)
            cv2.imshow("canny10", canny10) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos9,_) = buscaContornos(canny9)
            (contornos10,_) = buscaContornos(canny10)
            
            #Dibujamos contornos 
            dibujaContornos(imgNaranjaFrente1, contornos9, -1, (0,0,255), 2)
            dibujaContornos(imgNaranjaArriba1, contornos10, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos9", imgNaranjaFrente1)
            cv2.imshow("contornos10", imgNaranjaArriba1)
            
            
            naranjaElipse=cv2.ellipse(imgNaranjaFrente1,calculaElipse(contornos9, imgNaranjaFrente1),(0,255,0),2)
            cv2.imshow("Imagen de la naranja con elipse",naranjaElipse)
            naranjaElipse2=cv2.ellipse(imgNaranjaArriba1,calculaElipse(contornos10, imgNaranjaArriba1),(0,255,0),2)
            cv2.imshow("Imagen de la naranja desde arriba con elipse",naranjaElipse2)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print()
            print("Eje mayor y eje menor",calculaElipse(contornos9, imgNaranjaFrente1)[1])
            print("(x,y)",calculaElipse(contornos9, imgNaranjaFrente1)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos10, imgNaranjaArriba1)[1])
            print("(x,y)",calculaElipse(contornos10, imgNaranjaArriba1)[0])
            print()
            
            redondez5 = redondez(contornos9)
            excentricidad5 = excentricidad(calculaElipse(contornos9, imgNaranjaFrente1))
            
            fruta5 = tipoDeFruta(redondez5, excentricidad5)
            densidad5 = densidadFruta(fruta5)
            
            volumen5 = calculoVolumenes(calculaElipse(contornos9, imgNaranjaFrente1)[1],calculaElipse(contornos10, imgNaranjaArriba1)[1])
            masa5 = volumen5 * densidad5
            media5 = redondez5 * excentricidad5
            
            print("Redondez,excentricidad y media->",redondez5, excentricidad5, media5)
            print("La fruta proporcionada es:", fruta5)
            print("El volumen es:", volumen5, "pixeles cubicos")
            print("La densidad es:", densidad5, "gramos/pixeles cubicos")
            print("La masa de es:", masa5,"gramos")
            print("La masa real es:",317,"gramos")
            print("Error sobre el peso real y el calculado->",abs(317-masa5),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==8:
            imgNaranjaFrente2 = cv2.imread("img/naranja2-frente.jpg", 1)
            imgNaranjaArriba2 = cv2.imread("img/naranja2-arriba.jpg",1)
            
            imgNaranjaFrente2 = cv2.resize(imgNaranjaFrente2, (800, 600))
            imgNaranjaArriba2 = cv2.resize(imgNaranjaArriba2, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgNaranjaFrente", imgNaranjaFrente2)
            cv2.imshow("imgNaranjaArriba", imgNaranjaArriba2)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris9 =  convierteEscalaGrises(imgNaranjaFrente2)
            gris10 = convierteEscalaGrises(imgNaranjaArriba2)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh9 = binarizaImagen(gris9, 244, 255, 0)
            ret2,thresh10 = binarizaImagen(gris10, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh9", thresh9) 
            cv2.imshow("thresh10", thresh10)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss9 = filtroGaussiano(thresh9, (5,5), 0)
            gauss10 = filtroGaussiano(thresh10, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado9", gauss9)
            cv2.imshow("suavizado10", gauss10)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny9 = detectaBordes(gauss9, 0, 255)
            canny10 = detectaBordes(gauss10, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny9", canny9)
            cv2.imshow("canny10", canny10) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos9,_) = buscaContornos(canny9)
            (contornos10,_) = buscaContornos(canny10)
            
            #Dibujamos contornos 
            dibujaContornos(imgNaranjaFrente2, contornos9, -1, (0,0,255), 2)
            dibujaContornos(imgNaranjaArriba2, contornos10, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos9", imgNaranjaFrente2)
            cv2.imshow("contornos10", imgNaranjaArriba2)
            
            
            naranjaElipse=cv2.ellipse(imgNaranjaFrente2,calculaElipse(contornos9, imgNaranjaFrente2),(0,255,0),2)
            cv2.imshow("Imagen de la naranja2 con elipse",naranjaElipse)
            naranjaElipse2=cv2.ellipse(imgNaranjaArriba2,calculaElipse(contornos10, imgNaranjaArriba2),(0,255,0),2)
            cv2.imshow("Imagen de la naranja2 desde arriba con elipse",naranjaElipse2)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            print() 
            print("Eje mayor y eje menor",calculaElipse(contornos9, imgNaranjaFrente2)[1])
            print("(x,y)",calculaElipse(contornos9, imgNaranjaFrente2)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos10, imgNaranjaArriba2)[1])
            print("(x,y)",calculaElipse(contornos10, imgNaranjaArriba2)[0])
            print()
            
            redondez5 = redondez(contornos9)
            excentricidad5 = excentricidad(calculaElipse(contornos9, imgNaranjaFrente2))
            
            fruta5 = tipoDeFruta(redondez5, excentricidad5)
            densidad5 = densidadFruta(fruta5)
            
            volumen5 = calculoVolumenes(calculaElipse(contornos9, imgNaranjaFrente2)[1],calculaElipse(contornos10, imgNaranjaArriba2)[1])
            masa5 = volumen5 * densidad5
            media5 = redondez5 * excentricidad5
            
            print("Redondez,excentricidad y media->",redondez5, excentricidad5, media5)
            print("La fruta proporcionada es:", fruta5)
            print("El volumen es:", volumen5, "pixeles cubicos")
            print("La densidad es:", densidad5, "gramos/pixeles cubicos")
            print("La masa de es:", masa5,"gramos")
            print("La masa real es:",360,"gramos")
            print("Error sobre el peso real y el calculado->",abs(360-masa5),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))
            
        elif aux==9:
            imgNaranjaFrente3 = cv2.imread("img/naranja3-frente.jpg", 1)
            imgNaranjaArriba3 = cv2.imread("img/naranja3-arriba.jpg",1)
            
            imgNaranjaFrente3 = cv2.resize(imgNaranjaFrente3, (800, 600))
            imgNaranjaArriba3 = cv2.resize(imgNaranjaArriba3, (800, 600))
            
            #muestra imagen de frente y arriba
            cv2.imshow("imgNaranjaFrente", imgNaranjaFrente3)
            cv2.imshow("imgNaranjaArriba", imgNaranjaArriba3)
            cv2.waitKey(0)
            
            #convierte escala de grises
            gris9 =  convierteEscalaGrises(imgNaranjaFrente3)
            gris10 = convierteEscalaGrises(imgNaranjaArriba3)
            
            #binariza la imagen con umbral minimo y maximo
            ret,thresh9 = binarizaImagen(gris9, 244, 255, 0)
            ret2,thresh10 = binarizaImagen(gris10, 244, 255, 0)
            
            #muestra mangoElipse1s binarizadas
            cv2.imshow("thresh9", thresh9) 
            cv2.imshow("thresh10", thresh10)
            
            cv2.waitKey(0)
            
            #aplicamos filtros gaussianos para eliminar el posible ruido
            gauss9 = filtroGaussiano(thresh9, (5,5), 0)
            gauss10 = filtroGaussiano(thresh10, (5,5), 0)  
            
            #muestra mangoElipse1s con el filtro de gauss aplicados
            cv2.imshow("suavizado9", gauss9)
            cv2.imshow("suavizado10", gauss10)
            
            cv2.waitKey(0)
            
            #Aplicamos Canny para la deteccion de los bordes 
            canny9 = detectaBordes(gauss9, 0, 255)
            canny10 = detectaBordes(gauss10, 0, 255)
            
            #mostramos las mangoElipse1s aplicadas con Canny
            cv2.imshow("canny9", canny9)
            cv2.imshow("canny10", canny10) 
            
            cv2.waitKey(0)
            #Buscamos los posibles contornos , ya que , que sea un borde no quiere
            #decir que sea un contorno
            (contornos9,_) = buscaContornos(canny9)
            (contornos10,_) = buscaContornos(canny10)
            
            #Dibujamos contornos 
            dibujaContornos(imgNaranjaFrente3, contornos9, -1, (0,0,255), 2)
            dibujaContornos(imgNaranjaArriba3, contornos10, -1, (0,0,255), 2)
            
            #mostramos los contornos de cada imagen
            cv2.imshow("contornos9", imgNaranjaFrente3)
            cv2.imshow("contornos10", imgNaranjaArriba3)
            
            
            naranjaElipse=cv2.ellipse(imgNaranjaFrente3,calculaElipse(contornos9, imgNaranjaFrente3),(0,255,0),2)
            cv2.imshow("Imagen de la naranja3 con elipse",naranjaElipse)
            naranjaElipse2=cv2.ellipse(imgNaranjaArriba3,calculaElipse(contornos10, imgNaranjaArriba3),(0,255,0),2)
            cv2.imshow("Imagen de la naranja3 desde arriba con elipse",naranjaElipse2)
            
            cv2.waitKey(0)
            #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
            
            print() 
            print("Eje mayor y eje menor",calculaElipse(contornos9, imgNaranjaFrente3)[1])
            print("(x,y)",calculaElipse(contornos9, imgNaranjaFrente3)[0])  
            print()
            print("Eje mayor y eje menor desde arriba",calculaElipse(contornos10, imgNaranjaArriba3)[1])
            print("(x,y)",calculaElipse(contornos10, imgNaranjaArriba3)[0])
            print()
            
            redondez5 = redondez(contornos9)
            excentricidad5 = excentricidad(calculaElipse(contornos9, imgNaranjaFrente3))
            
            fruta5 = tipoDeFruta(redondez5, excentricidad5)
            densidad5 = densidadFruta(fruta5)
            
            volumen5 = calculoVolumenes(calculaElipse(contornos9, imgNaranjaFrente3)[1],calculaElipse(contornos10, imgNaranjaArriba3)[1])
            masa5 = volumen5 * densidad5
            media5 = redondez5 * excentricidad5
            
            print("Redondez,excentricidad y media->",redondez5, excentricidad5, media5)
            print("La fruta proporcionada es:", fruta5)
            print("El volumen es:", volumen5, "pixeles cubicos")
            print("La densidad es:", densidad5, "gramos/pixeles cubicos")
            print("La masa es:", masa5,"gramos")
            print("La masa real es:",318)
            print("Error sobre el peso real y el calculado->",abs(318-masa5),"gramos")
            cv2.waitKey(0)
            print()
            aux = int(input("Selecione Opcion\n"))
    
    
programa()

msvcrt.getch()