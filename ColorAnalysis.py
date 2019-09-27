#Tem por objetivo medir as cores (intensidade de cinza) de 5 imagens 
#(A10,23,28,30 e 45) para medir em relacao a imagem teste (A4)
import cv2 as cv
import numpy as np
img_ = cv.imread("teste.jpg")
def CorteSobrestrato(imagem):    #Corta a escala da imagem e tira as suas medidas
    y=0; x=25; h=100; w=200
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        print("Escala nao foi filtrada!!!")
    crop = imagem[y:y+h, x:x+w]
    cv.imshow("Sobre",crop)
    #cv.waitKey()
    cv.destroyWindow("Sobre")
    intensidadeMedia = np.mean(crop)
    intensidadeMediana = np.median(crop)
    return intensidadeMediana

def CorteSubstrato(imagem):    #Corta a escala da imagem e tira as suas medidas
    y=420; x=25; h=100; w=200
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        print("Escala nao foi filtrada")
    crop = imagem[y:y+h, x:x+w]
    cv.imshow("Sub",crop)
    #cv.waitKey()
    cv.destroyWindow("Sub")
    intensidadeMedia = np.mean(crop)
    intensidadeMediana = np.median(crop)
    return intensidadeMediana

#*************************************Prefiltros*************************************
def Filtro1(imagem): #Median Blur (15), Pyramid Mean Shift (35,32)-> para Arev e Sobrestrato
    #Pre filtragem
    cv.convertScaleAbs(imagem,imagem, 2,0)
    imagem = cv.medianBlur(imagem,7)
    try:
        imagem = cv.pyrMeanShiftFiltering(imagem, 25, 30)
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        print("imagem ja esta em P&B, por isso nao pode passar por um filtro")
        #adicionar algum filtro de media aqui
    return imagem

def Filtro2(imagem): #Median Blur (15), Pyramid Mean Shift (35,32)-> para AZT
    #Pre filtragem
    if CorteSubstrato(imagem) > 100:
        cv.convertScaleAbs(imagem,imagem, 1.7,0)
        print ("clara")
    elif CorteSubstrato(imagem) > 80:
        cv.convertScaleAbs(imagem,imagem, 1.5,0)
        print("media")
    else:
        cv.convertScaleAbs(imagem,imagem, 1.5,30)
        print("escura")
    #filtrado = cv.medianBlur(imagem,7)
    try:
        imagem = cv.pyrMeanShiftFiltering(imagem, 20, 20)
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        print("imagem ja esta em P&B, por isso nao pode passar por um filtro")
        #adicionar algum filtro de media aqui
    return imagem

#*************************************THRESHOLD*************************************
#maximos
max_intensidade = 255; max_tipo = 5
#variaveis para Filtro sao duas: tipo e intensidade
tipo_ = 0; intensidade_ = 50

def ThreshIntensidade(intensidade):
    #atualiza variavel global
    global intensidade_
    intensidade_ = intensidade
    window_name ="Threshold"
    #condicional para tipo de filtro, aplicando nova intensidade
    if tipo_ == 0:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.THRESH_BINARY)
        print ("tipo: Binário")
    elif tipo_ == 1:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.ADAPTIVE_THRESH_MEAN_C)
        print ("tipo: Adaptativo Média")
    elif tipo_ == 2:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C)
        print ("tipo: Adaptativo Gaussiano")
    elif tipo_ == 3:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.THRESH_TRUNC)
        print ("tipo: Trunc")
    elif tipo_ == 4:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.THRESH_TOZERO)
        print ("tipo: To Zero")
    elif tipo_ == 5:
        ret,filtered = cv.threshold(img_,0,255,cv.THRESH_OTSU)
        print ("tipo: Otsu")
    #abre a janela e printa os valores
    cv.imshow(window_name, filtered)
    print ("intensidade: "+str(intensidade_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = filtered

def ThreshTipo (tipo):
    #atualiza variavel tipo
    global tipo_
    global filtered_
    tipo_ = tipo
    window_name ="Threshold"
    #aplica novo tipo de filtro com a mesma intensidade
    if tipo == 0:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.THRESH_BINARY)
        print ("tipo: Binário")
    elif tipo == 1:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.ADAPTIVE_THRESH_MEAN_C)
        print ("tipo: Adaptativo Média")
    elif tipo == 2:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C)
        print ("tipo: Adaptativo Gaussiano ")
    elif tipo == 3:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.THRESH_TRUNC)
        print ("tipo: Trunc")
    elif tipo_ == 4:
        ret,filtered = cv.threshold(img_,intensidade_,255,cv.THRESH_TOZERO)
        print ("tipo: To Zero")
    elif tipo_ == 5:
        ret,filtered = cv.threshold(img_,0,255,cv.THRESH_OTSU)
        print ("tipo: Otsu")
    cv.imshow(window_name, filtered)
    print ("intensidade: "+str(intensidade_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = filtered

def Thresh ():
    global img_
    window_name ="Threshold"
    cv.namedWindow(window_name)
    cv.createTrackbar("Tipo", window_name , 0, 5, ThreshTipo)
    cv.createTrackbar("Intensidade", window_name , 0, max_intensidade, ThreshIntensidade)
    #abre a janela e printa os valores
    print ("--Limiar--")
    #atualiza imagem global e fecha janela
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        cv.destroyWindow(window_name)
        Interface()


def Main():
    cv.imshow("original",img_)
    sobre = CorteSobrestrato(img_)
    print("Cores Sobrestrato: ",sobre)
    sub = CorteSubstrato(img_)
    print("Cores Substrato: ", sub)
    cv.destroyWindow("original")
#*************************************INTERFACE*************************************
def  Interface():       #
    global img_; global img
    winname = "Menu"
    cv.imshow(winname, img_)
    k = cv.waitKey()
    if k == 49:        #Se apertar 1: 
        img = cv.imread('2018.07.03 - A4 - 12X - esc .tif')
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("#######Imagem numero 4")
        Main()
        cv.destroyWindow("Menu")
    elif k == 50:      #Se apertar 2: 
        img = cv.imread('2018.07.03 - A10- 12X - esc .tif')
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("#######Imagem numero 10")
        Main()
    elif k == 51:      #Se apertar 3: 
        img = cv.imread("2018.07.03 - A23- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("#######Imagem numero 23")
        Main()
    elif k == 52:      #Se apertar 4: 
        img = cv.imread("2018.07.03 - A28- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("#######Imagem numero 28")
        Main()
    elif k == 53:      #Se apertar 5: 
        img = cv.imread("2018.07.03 - A30- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("#######Imagem numero 30")
        Main()
    elif k == 54:      #Se apertar 6: 
        img = cv.imread("2018.07.03 - A45- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("#######Imagem numero 45")
        Main()
    elif k == 116:  #Se apertar t: Thresh
        img_ = Filtro1 (img_)
        Thresh()
    else:              #Se apertar qualquer tecla: imprime a tecla 
        print("Selecione um comando válido! Você digitou: "+str(k))
        cv.destroyWindow("Menu")
    Interface()
#*************************************Main*************************************
Interface()