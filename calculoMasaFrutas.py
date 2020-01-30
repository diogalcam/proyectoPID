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
print("""**************Instrucciones de uso*******************
Inicialmente se puede escoger entre una imagen precargada manualmente o una de nuestra base de datos:
    - Si escoge la opcion de utilizar una imagen precargada debera seleccionar la opcion 0 en el teclado y proporcionar el nombre de la imagen de frente y de arriba, en ese orden
    - Si escoge una opcion de nuestra base de datos simplemtente debera teclear el numero que desee

Funcionamiento del mismo:
    1. En consola ira apareciendo una explicacion paso a paso que esta realizando el algoritmo
    2. Se abriran 2 ventanas con las imagenes de frente y desde arriba mostrando esos resultados
    3. Para que el algoritmo avance de paso a paso debera cerrar las ventanas de las imagenes que se han abierto\n\n""")



def menu():
    
    print("************************\n",
"Selecciona la fruta para calcular su masa\n",
"0) Otra opcion\n",
"1) Mango1\n",
"2) Mango2\n",
"3) Mango3\n",
"4) Manzana1\n",
"5) Manzana2\n",
"6) Manzana3\n",
"7) Naranja1\n",
"8) Naranja2\n",
"9) Naranja3\n"

)



def programa():
    aux = 1000
    menu()
    aux = int(input("Selecione Opcion\n"))
    while(aux>=0 and aux<=9):
        imagenFrente = 0
        imagenArriba = 0
        if aux==0:
            print("Las imagenes deben estar contenidas en la carpeta llamada 'img' y estar en formato jpg")
            nombreImgFrente = input("Introduzca el nombre de la imagen de frente\n")
            nombreImgArriba = input("Introduzca el nombre de la imagen de arriba\n")
            n0 = "img/{}.jpg".format(nombreImgFrente)
            n1 = "img/{}.jpg".format(nombreImgArriba)
            imagenFrente = cv2.imread(n0,1)
            imagenArriba = cv2.imread(n1,1)
            
        elif aux==1:
            imagenFrente = cv2.imread("img/mango-frente.jpg", 1)
            imagenArriba = cv2.imread("img/mango-arriba.jpg",1)
            
        elif aux==2:
            imagenFrente = cv2.imread("img/mango2-frente.jpg", 1)
            imagenArriba = cv2.imread("img/mango2-arriba.jpg",1)
            
        elif aux==3:
            imagenFrente = cv2.imread("img/mango3-frente.jpg", 1)
            imagenArriba = cv2.imread("img/mango3-arriba.jpg",1)
        
        elif aux==4:
            imagenFrente = cv2.imread("img/manzana1-frente.jpg", 1)
            imagenArriba = cv2.imread("img/manzana1-arriba.jpg",1)
            
        elif aux==5:
            imagenFrente = cv2.imread("img/manzana2-frente.jpg", 1)
            imagenArriba = cv2.imread("img/manzana2-arriba.jpg",1)
        
        elif aux==6:
            imagenFrente = cv2.imread("img/manzana3-frente.jpg", 1)
            imagenArriba = cv2.imread("img/manzana3-arriba.jpg",1)
        
        elif aux==7:
            imagenFrente = cv2.imread("img/naranja1-frente.jpg", 1)
            imagenArriba = cv2.imread("img/naranja1-arriba.jpg",1)
            
        elif aux==8:
            imagenFrente = cv2.imread("img/naranja2-frente.jpg", 1)
            imagenArriba = cv2.imread("img/naranja2-arriba.jpg",1)
            
        elif aux==9:
            imagenFrente = cv2.imread("img/naranja3-frente.jpg", 1)
            imagenArriba = cv2.imread("img/naranja3-arriba.jpg",1)   
            
            
        imagenFrente = cv2.resize(imagenFrente, (800, 600))
        imagenArriba = cv2.resize(imagenArriba, (800, 600))
        
        print("=====================================================================")
        #muestra imagen de frente y arriba
        print("Paso 1) Se muestran las imagenes seleccionadas")
        cv2.imshow("Imagen de frente", imagenFrente)
        cv2.imshow("Imagen de arriba", imagenArriba)
        
        cv2.waitKey(0)
                
        #convierte escala de grises
        print("Paso 2) Se realiza la conversion de las imagenes originales a escala de grises")
        gris =  convierteEscalaGrises(imagenFrente)
        gris2 = convierteEscalaGrises(imagenArriba)
        
        cv2.imshow("Imagen de frente en escala de grises", gris) 
        cv2.imshow("Imagen de arriba en escala de grises", gris2)
        
        cv2.waitKey(0)
        
        #binariza la imagen con umbral minimo y maximo
        print("""Paso 3) Se binariza la imagen en escala de grises utilizando umbrales: todos los pixeles que esten por encima del valor 
        240 se convierten en blanco y el resto en negro""")
        ret,thresh = binarizaImagen(gris, 244, 255, 0)
        ret2,thresh2 = binarizaImagen(gris2, 244, 255, 0)
        
        #muestra mangoElipse1s binarizadas
        cv2.imshow("Imagen de frente binarizada", thresh) 
        cv2.imshow("Imagen de arriba binarizada", thresh2)
        
        cv2.waitKey(0)

        
        #Aplicamos Canny para la deteccion de los bordes 
        print("""Paso 4) Se le aplica el metodo de Canny para obtener los contornos. Este metodo inicialmente aplica un filtro 
        gaussiano para suavizar la imagen y se obtiene la imagen gradiente, a partir de esta se evalua que pixeles son bordes y cuales no""")
        canny = detectaBordes(thresh, 0, 255)
        canny2 = detectaBordes(thresh2, 0, 255)
        
        #mostramos las mangoElipse1s aplicadas con Canny
        cv2.imshow("Bordes de la imagen de frente", canny)
        cv2.imshow("Bordes de la imagen cenital", canny2) 
        
        cv2.waitKey(0)
        #Buscamos los posibles contornos , ya que , que sea un borde no quiere
        #decir que sea un contorno
        print("""Paso 5) Se buscan los posibles contornos y se dibujan. Este paso es necesario ya que un borde no es igual que un contorno. 
        Un contorno es un conjunto de pixeles que comienzan y acaban en el mismo punto""")
        (contornos,_) = buscaContornos(canny)
        (contornos2,_) = buscaContornos(canny2)
        
        #Dibujamos contornos 
        dibujaContornos(imagenFrente, contornos, -1, (0,0,255), 2)
        dibujaContornos(imagenArriba, contornos2, -1, (0,0,255), 2)
        
        #mostramos los contornos de cada imagen
        cv2.imshow("Contornos dibujados de la imagen de frente", imagenFrente)
        cv2.imshow("Contornos dibujados de la imagen cenital", imagenArriba)
        
        cv2.waitKey(0)
        
        #se calcula la elipse y se dibuja
        print("""Paso 6) Se calcula la elipse a partir de los momentos del contorno y se dibujan""")
        elipse1=cv2.ellipse(imagenFrente,calculaElipse(contornos, imagenFrente),(0,255,0),2)
        cv2.imshow("Imagen frontal con la elipse dibujada",elipse1)
        elipse2=cv2.ellipse(imagenArriba,calculaElipse(contornos2, imagenArriba),(0,255,0),2)
        cv2.imshow("Imagen cenital con la elipse dibujado",elipse2)
        
        cv2.waitKey(0)
        #CalculaElipse devuelve eje mayor y menor , y tambien (x,y)
        print() 
        print("Eje mayor y eje menor de la imagen frontal",calculaElipse(contornos, imagenFrente)[1])
        print("Eje mayor y eje menor de la imagen de arriba",calculaElipse(contornos2, imagenArriba)[1])
        print()
        
        #calculamos la redondez y excentricidad para luego hacer una media y detectar el tipo de fruta
        redondez1 = redondez(contornos)
        excentricidad1 = excentricidad(calculaElipse(contornos, imagenFrente))
        
        #miramos que tipo de fruta es
        fruta = tipoDeFruta(redondez1, excentricidad1)
        
        #el calculo de la densidad es la media de las densidades de cada tipo de fruta correspondiente
        #la densidad es el numero de gramos que tiene un pixel cubico de media
        densidad = densidadFruta(fruta)
        
        #volumen en pixeles cubicos ( contar los pixeles que ocupa cada fruta )
        volumen = calculoVolumenes(calculaElipse(contornos, imagenFrente)[1],calculaElipse(contornos2, imagenArriba)[1])
        masa = volumen * densidad
        media = redondez1 * excentricidad1
        print("""Paso 7) Se calculan la redondez y la excentricidad para poder obtener el tipo de fruta que es""")
        print("Redondez:",redondez1+"; Excentricidad:", excentricidad1)

        print("""Paso 8) Se calcula el volumen a partir de la siguiente formula:
         Volumen = 4*pi*Eje Mayor Imagen Frontal*Eje Menor Imagen Frontal*Eje Mayor Imagen Cenital""")
        
        print("""Paso 9) A partir de la fruta reconocida se escoge la densidad de la misma""")
       
        print("""Paso 10) Como paso final se calcula la masa a partir de los datos obtenidos en el volumen y la densidad con la siguiente formula:
        Masa = Volumen*Densidad\n""")
        print("****************Datos obtenidos*****************")
        print("La fruta proporcionada es:", fruta)
        print("La densidad es:", densidad, "gramos/pixeles cubicos")
        print("El volumen es:", volumen, "pixeles cubicos")
        print("La masa estimada es de:", int(masa),"gramos")
        print("************************************************\n\n")
        print()
        
        
        aux = int(input("Selecione Opcion\n"))  
    
r = 1000
while(r>0):
    programa()

msvcrt.getch()