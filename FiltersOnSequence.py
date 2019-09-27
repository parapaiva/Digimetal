# -*- coding: utf-8 -*-
#importacao do matplotlib nao funciona, pode ser util para fazer graficos diferentes
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

#Le a imagem, reduz e faz copia grayscale
img = cv.imread('/Users/Gabiru/Documents/Digimetal_2/2018.07.03 - A28- 12X - esc .tif')
img_ = cv.resize(img, (0,0), fx=.4, fy=.4)
#imagem que sera usada pelo proximo filtro: img_ e original: img
filtered_ = img_
#variavel para undo
img_1 = img_
#nome do Save
nomearquivo = "Salva"
#menu da interface
menu = cv.imread("menu.jpg")
#imagem memorizada para operacoes
s1 = img_

#*************************************BILATERAL*************************************
#valores maximos
max_lowThresholdDist = 15; max_lowThresholdEspa = 255; max_lowThresholdCor = 255
#variaveis para filtro Bilateral
dist_ = 9; cor_ = 75; espa_ = 75

#Filtro Bilateral possui tres variaveis para ajustar:
    #diametro da vizinhanca do pixel,dis
    #desvio padrao nas cores, cor
    #desvio padrao no espaco, espa
def BiFilterDist (dist):
    window_name ="Filtro Bilateral"
    #atualiza dist global
    global dist_
    global filtered_
    dist_ = dist
    #calcula filtro
    blur = cv.bilateralFilter(img_,dist_,cor_,espa_)
    #abre a janela e printa os valores
    cv.imshow(window_name, blur)
    #salva o filtro aplicado na variavel temporaria
    filtered_ = blur
    #print de controle
    print ("dist: "+str(dist))
    print ("cor: "+str(cor_))
    print ("espa: "+str(espa_))
    print ("--------------")

def BiFilterCor (cor):
    window_name ="Filtro Bilateral"
    #atualiza cor global
    global cor_
    global filtered_
    cor_  = cor
    #calcula filtro
    blur = cv.bilateralFilter(img_,dist_,cor_,espa_)
    #abre a janela e printa os valores
    cv.imshow(window_name, blur)
    #salva o filtro aplicado na variavel temporaria
    filtered_ = blur
    #print de controle
    print ("dist: "+str(dist_))
    print ("cor: "+str(cor))
    print ("espa: "+str(espa_))
    print ("--------------")

def BiFilterEspa (espa):
    window_name ="Filtro Bilateral"
    #atualiza espa global
    global espa_
    global filtered_
    espa_  = espa
    #calcula filtro
    blur = cv.bilateralFilter(img_,dist_,cor_,espa_)
    #abre a janela e printa os valores
    cv.imshow(window_name, blur)
    #salva o filtro aplicado na variavel temporaria
    filtered_ = blur    
    #print de controle
    print ("dist: "+str(dist_))
    print ("cor: "+str(cor_))
    print ("espa: "+str(espa))
    print ("--------------")

def BiFilter():
    global img_
    #cria janela e trackbar com nomes
    window_name ="Filtro Bilateral"
    cv.namedWindow(window_name)
    cv.createTrackbar("distancia", window_name , 0, max_lowThresholdDist, BiFilterDist)
    cv.createTrackbar("desvio cor", window_name , 0, max_lowThresholdCor, BiFilterCor)
    cv.createTrackbar("desvio espacial", window_name , 0, max_lowThresholdEspa, BiFilterEspa)
    #chama uma vez o filtro com valor padrao
    print ("--Filtro Bilateral--")
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()

#*************************************CANNY*************************************
#valores maximos
max_lowThreshold = 100; max_ratio = 2; max_kernelsize = 12
#variaveis
low_threshold_ = 0; ratio_ = 2; kernel_size_ = 3

#Filtro possui tres variaveis para ajustar
    #limiar minimo para ser considerado contorno, low_threshold_
        #
    #razao entre menor e maior limiar, ratio
        #1, 2 ou 3
    #tamanho do miolo para borrar
        #valores baixos aconselhado, deve ser impar
def CannyLow (low_threshold):
    window_name ="Mapa de Contornos"
    #atualiza variavel global
    global low_threshold_
    global filtered_
    low_threshold_ = low_threshold
    #aplica filtro de blur
    img_blur = cv.blur(img_, (kernel_size_,kernel_size_))
    #aplica canny com imagem borrada
    detected_edges = cv.Canny(img_blur, low_threshold_, low_threshold_*ratio_, kernel_size_)
    #abre a janela e printa os valores
    cv.imshow(window_name, detected_edges)
    #print de controle
    print("Threshold minimo:"+str(low_threshold_))
    print("Ratio :"+str(ratio_))
    print("Kernel Size :"+str(kernel_size_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = detected_edges

def CannyRatio (ratio):
    window_name ="Mapa de Contornos"
    #atualiza variavel global
    global ratio_
    global filtered_
    #ajusta-se o ratio para ficar de 1 a 3
    ratio_ = ratio + 1
    #aplica filtro de blur
    img_blur = cv.blur(img_, (kernel_size_,kernel_size_))
    #aplica canny com imagem borrada
    detected_edges = cv.Canny(img_blur, low_threshold_, low_threshold_*ratio_, kernel_size_)
    #abre a janela e printa os valores
    cv.imshow(window_name, detected_edges)
    #print de controle
    print("Threshold minimo:"+str(low_threshold_))
    print("Ratio :"+str(ratio_))
    print("Kernel Size :"+str(kernel_size_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = detected_edges

def CannyKernel (kernel_size):
    window_name ="Mapa de Contornos"
    cv.namedWindow(window_name)
    #atualiza variavel global
    global kernel_size_
    global filtered_
    if kernel_size%2: #se for impar = 1, ou seja, True
        kernel_size_ = kernel_size
    else: #se for par, será = 0, ou seja, False
        kernel_size_ = kernel_size + 1
    #aplica filtro de blur
    #img_blur = cv.blur(img_, (kernel_size_,kernel_size_))
    img_blur = cv.GaussianBlur(img_,(kernel_size_,kernel_size_),0)
    #aplica canny com imagem borrada
    detected_edges = cv.Canny(img_blur, low_threshold_, low_threshold_*ratio_, kernel_size_)
    #abre a janela e printa os valores
    cv.imshow(window_name, detected_edges)
    #print de controle
    print("Threshold minimo:"+str(low_threshold_))
    print("Ratio :"+str(ratio_))
    print("Kernel Size :"+str(kernel_size_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = detected_edges

def Canny ():
    global img_
    window_name ="Mapa de Contornos"
    cv.namedWindow(window_name)
    cv.createTrackbar("Minimo Threshold", window_name , 0, max_lowThreshold, CannyLow)
    cv.createTrackbar("Ratio", window_name , 0,max_ratio, CannyRatio)
    cv.createTrackbar("Tamanho do Miolo", window_name , 0,max_kernelsize , CannyKernel)
    #fecha filtro
    print ("--Detector de Canny--")
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()


#*************************************SHARPEN*************************************
#maximo
max_lowThresholdKsize = 31
#variaveis para Filtro
ddepth_ = cv.CV_32F; ksize_ = 3 #deve ser impar
xorder_ = 1; yorder_ = 1; scale_ = 1; delta_ = 0

def GradientFilters(trackbar):
    window_name ="Gradient Filter"
    cv.namedWindow(window_name)
    cv.createTrackbar("1-Laplace 2-Sobel", window_name , 0, 1, GradientFilters)
    global img_
    global filtered_
    if trackbar == 0:
        filtered_ = cv.Laplacian(img_,ddepth_,ksize_ -1)
        print ("----Laplacian----")
        cv.imshow(window_name, filtered_)
    elif trackbar == 1:
        grad_x = cv.Sobel(img_,ddepth_,0,1,3)
        grad_y = cv.Sobel(img_,ddepth_,1,0,3)
        filtered_ = cv.addWeighted(grad_x, 0.5, grad_y, 0.5, 0)
        print ("----Sobel----")
        cv.imshow(window_name, filtered_)
    elif trackbar == -1:
        print ("--Filtros Gradientes--")
        filtered_ = img_
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()

#*************************************SHARPEN2*************************************
#maximo
max_ksizesharpen = 100
#variaveis para Filtro
ksizesharpen_ = 3 #deve ser impar

def SharpenKsize(ksizesharpen):
    #atualiza variavel global
    global ksizesharpen_
    global filtered_
    if ksizesharpen%2 == 0:
        ksizesharpen_ = ksizesharpen+1
    else:
        ksizesharpen_ = ksizesharpen
    window_name ="Sharpen"
    #aplica filtro Smooth
    lowpass = cv.blur(img_,ksizesharpen_)
    filtered = cv.subtract(img_,lowpass)
    #abre a janela e printa os valores
    cv.imshow(window_name, filtered)
    print ("ksize: "+str(ksizesharpen_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = filtered


def Sharpen():
    global img_
    window_name ="Sharpen"
    cv.namedWindow(window_name)
    cv.createTrackbar("ksize", window_name , 0, max_ksizesharpen, SharpenKsize)
    #cv.createTrackbar("Intensidade", window_name , 0, max_intensidade, ThreshIntensidade)
    #abre a janela e printa os valores
    print ("--Sharpen Filter--")
    #atualiza imagem global e fecha janela
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()

#*************************************MEDIAN BLUR*************************************
#maximo
max_ksizeblur = 100
#variaveis para Filtro
ksizeblur_ = 3 #deve ser impar

def MedianBlurKsize(ksizeblur):
    #atualiza variavel global
    global ksizeblur_
    global filtered_
    if ksizeblur%2 == 0:
        ksizeblur_ = ksizeblur+1
    else:
        ksizeblur_ = ksizeblur
    window_name ="Median Blur"
    #aplica filtro Smooth
    lowpass = cv.medianBlur(img_,ksizeblur_)
    #abre a janela e printa os valores
    cv.imshow(window_name, lowpass)
    print ("ksize: "+str(ksizeblur_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = lowpass


def MedianBlur():
    global img_
    window_name ="Median Blur"
    cv.namedWindow(window_name)
    cv.createTrackbar("ksize", window_name , 0, max_ksizeblur, MedianBlurKsize)
    #abre a janela e printa os valores
    print ("--Median Filter--")
    #atualiza imagem global e fecha janela
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()


#*************************************THRESHOLD*************************************
#maximos
max_intensidade = 255; max_tipo = 5
#variaveis para Filtro sao duas: tipo e intensidade
tipo_ = 0; intensidade_ = 50

def ThreshIntensidade(intensidade):
    #atualiza variavel global
    global intensidade_
    global filtered_
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
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()

#*************************************DENOISE*************************************
#maximos
max_template = 14; max_search = 42; max_strength = 100
#variaveis para Filtro
template_ = 7; search_ = 30; strength_ = 30

#Filtro possui tres variaveis para ajustar: template, search e strength
def DenoiseTemplate (template):
    window_name ="Filtro Ruidos"
    global template_
    global filtered_
    #deve ser um valor impar
    if template % 2 == 0:
        template_ = template +1
    else:
        template_ = template
    #aplica filtro com nova variavel
    filtered = cv.fastNlMeansDenoising(img_,None,strength_,template,search_)
    #atualiza imagem, abre a janela e printa os valores
    cv.imshow(window_name, filtered)
    print ("Template: "+str(template_))
    print ("Searh: "+str(search_))
    print ("Strength: "+str(strength_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = filtered

def DenoiseSearch (search):
    window_name ="Filtro Ruidos"
    global search_
    global filtered_
    #deve ser um valor impar
    if search % 2 == 0:
        search_ = search +1
    else:
        search_ = search 
    search_ = search
    #aplica filtro com nova variavel
    filtered = cv.fastNlMeansDenoising(img_,None,strength_,template_,search)
    #abre a janela e printa os valores
    cv.imshow(window_name, filtered)
    print ("Template: "+str(template_))
    print ("Searh: "+str(search_))
    print ("Strength: "+str(strength_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = filtered

def DenoiseStrength (strength):
    window_name ="Filtro Ruidos"
    global strength_
    global filtered_
    strength_ = strength
    #aplica filtro com nova variavel
    filtered = cv.fastNlMeansDenoising(img_,None,strength,template_,search_)
    #abre a janela e printa os valores
    cv.imshow(window_name, filtered)
    print ("Template: "+str(template_))
    print ("Searh: "+str(search_))
    print ("Strength: "+str(strength_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = filtered

def Denoise ():
    global img_
    window_name ="Filtro Ruidos"
    cv.namedWindow(window_name)
    cv.createTrackbar("Template Size", window_name , 0, max_template, DenoiseTemplate)
    cv.createTrackbar("Searh Size", window_name , 0, max_search, DenoiseSearch)
    cv.createTrackbar("Strength", window_name , 0, max_strength, DenoiseStrength)
    #abre a janela e printa os valores
    print ("--Filtro de Ruidos--")
    #atualiza imagem global e fecha janela
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()

#*************************************FIND CONTOURS*************************************


#*************************************Gaussian Blur*************************************

#*************************************Blur basicao*************************************


#*************************************MeanShift*************************************
#maximos
max_color = 50; max_spatial = 50
#variaveis para Filtro
color_ = 21; spatial_ = 21

def MeanShiftColor(color):
    window_name ="Mean Shift"
    global color_
    global filtered_
    color_ = color
    #aplica filtro com nova variavel
    shifted = cv.pyrMeanShiftFiltering(img_, spatial_, color_)
    #abre a janela e printa os valores
    cv.imshow(window_name, shifted)
    print ("color: "+str(color_))
    print ("spatial: "+str(spatial_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = shifted

def MeanShiftSpatial(spatial):
    window_name ="Mean Shift"
    global spatial_
    global filtered_
    spatial_ = spatial
    #aplica filtro com nova variavel
    shifted = cv.pyrMeanShiftFiltering(img_, spatial_, color_)
    #abre a janela e printa os valores
    cv.imshow(window_name, shifted)
    print ("color: "+str(color_))
    print ("spatial: "+str(spatial_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = shifted

def MeanShift():
    global img_
    window_name ="Mean Shift"
    cv.namedWindow(window_name)
    cv.createTrackbar("Color", window_name , 0, max_color, MeanShiftColor)
    cv.createTrackbar("Spatial", window_name , 0, max_spatial, MeanShiftSpatial)
    #abre a janela e printa os valores
    print ("--Filtro de Ruidos--")
    #atualiza imagem global e fecha janela
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()


#*************************************SALVAR*************************************

def SaveImage():
    cv.imwrite(nomearquivo+".jpg",img_)
    print ("Imagem salva como: "+nomearquivo+".jpg")

#*************************************Check Ilumination*************************************
#Mede cor do substrato e sobrestrato
def CorSobrestratoEsq(imagem):    #Corta a escala da imagem e tira as suas medidas
    imagem = cv.resize(imagem, (0,0), fx=0.4, fy=0.4)
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        pass
    y=0; x=25; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana1 = np.median(crop)
    return intensidadeMediana1

def CorSubstratoDir(imagem):    #Corta a escala da imagem e tira a mediana de cor
    #imagem = cv.resize(imagem, (0,0), fx=0.4, fy=0.4)
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        pass
    y=520; x=600; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana2 = np.median(crop)
    return intensidadeMediana2

def CorSobrestratoDir(imagem):    #Corta a escala da imagem e tira as suas medidas
    imagem = cv.resize(imagem, (0,0), fx=0.4, fy=0.4)
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        pass
    y=0; x=600; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana2 = np.median(crop)
    return intensidadeMediana2

def CorSubstratoEsq(imagem):    #Corta a escala da imagem e tira a mediana de cor
    #imagem = cv.resize(imagem, (0,0), fx=0.4, fy=0.4)
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        pass
    y=420; x=25; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana1 = np.median(crop)
    return intensidadeMediana1

def DivideImage(imagem):
    esq = imagem[:,:imagem.shape[1]]
    direi = imagem[:,imagem.shape[1]:]
    return esq,direi

def CheckIlumination(imagem):
    sobreDif=CorSobrestratoDir(imagem)-CorSobrestratoEsq(imagem)
    subDif=CorSubstratoEsq(imagem)-CorSubstratoEsq(imagem)
    if abs(sobreDif) > 10 or abs(subDif) >10:
        print("diferença Sobre: ",sobreDif)
        print("diferença Sub: ",subDif)
        return 1
    else:
        print("Nao ha diferenca de luz imagem:",sobreDif,subDif)
        return 0

#*************************************Equaliza Histograma*************************************
#Nao esta transformando em cinza
def EqualizaHistograma(imagem):
    try:
        equalizada = cv.cvtColor(imagem,cv.COLOR_BGR2GRAY)
    except:
        pass
    equalizada = cv.equalizeHist(imagem)
    return equalizada
    
#*************************************Contraste e Brilho*************************************
max_contraste = 50; max_brilho = 100
contraste_ = 1; brilho_ = 50;

def Contraste(contraste):
    window_name ="Contraste e Brilho"
    global filtered_
    global contraste_
    contraste_ = contraste/10.0
    #aplica filtro com nova variavel
    shifted = cv.convertScaleAbs(img_, contraste,contraste_,brilho_)
    #abre a janela e printa os valores
    cv.imshow(window_name, filtered_)
    print ("contraste: "+str(contraste_))
    print ("brilho: "+str(brilho_))
    print ("--------------")
    filtered_ = shifted

def Brilho(brilho):
    window_name ="Contraste e Brilho"
    global filtered_
    global brilho_
    brilho_ = brilho-50
    #aplica filtro com nova variavel
    shifted = cv.convertScaleAbs(img_, brilho,contraste_,brilho_)
    #abre a janela e printa os valores
    cv.imshow(window_name, shifted)
    print ("contraste: "+str(contraste_))
    print ("brilho: "+str(brilho_))
    print ("--------------")
    #salva o filtro aplicado na variavel temporaria
    filtered_ = shifted


def ConstrasteBrilho():
    global img_
    window_name ="Contraste e Brilho"
    cv.namedWindow(window_name)
    cv.createTrackbar("Constraste", window_name , 0, max_contraste, Contraste)
    cv.createTrackbar("Brilho", window_name , 0, max_brilho, Brilho)
    #abre a janela e printa os valores
    print ("--Contraste e Brilho--")
    #atualiza imagem global e fecha janela
    k = cv.waitKey()
    #se apertar esc nao salva, qualquer outro botao salva
    if k == 27:
        cv.destroyWindow(window_name)
        Interface()
    else:
        img_1 = img_
        img_ = filtered_
        cv.destroyWindow(window_name)
        Interface()

#*************************************Find Contours*************************************
def IsolateWhiteAreas():
    global s1
    global img_
    global img_1
    #Pre filtragem
    filtrado = cv.medianBlur(img_,21)
    try:
        filtrado = cv.pyrMeanShiftFiltering(filtrado, 23, 25)
        filtrado = cv.cvtColor(filtrado, cv.COLOR_BGR2GRAY)
    except:
        pass
    #Isolar area debaixo
    ret,areadebaixo = cv.threshold(filtrado,75,255,cv.ADAPTIVE_THRESH_MEAN_C)
    try:
        s1 = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
    except:
        s1 = img_
    #somar com imagem original
    soma1 = cv.add(areadebaixo,s1)
    ret,areadecima = cv.threshold(filtrado,12,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    #Soma Final
    img_ = cv.add(soma1,areadecima)
    ret,img_ = cv.threshold(img_,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    cv.imshow("Soma final",img_)
    cv.waitKey()
    cv.destroyWindow("Soma final")

def FindContours():
    global img_
    #essa referencia podera ser lida da imagem
    referencia = 500
    kernel = np.ones((4,4),np.uint8)
    #primeiro usamos pre-filtros para obter contornos em branco
    IsolateWhiteAreas()
    #Transformacoes morfologicas para obter um formato genérico
    #erosion remove os pixels da borda
    erosion = cv.erode(img_,kernel,iterations = 1)
    #Rotular e classificar as areas na imagem
    cv.findContours()
    img, contours, hierarchy= cv.findContours(erosion,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    cnt = sorted(contours,key=cv.contourArea, reverse=True)
    cv.drawContours(img_, cnt, 0, (100,255,0), 3)
    cv.drawContours(img_, cnt, 1, (100,255,0), 3)
    #(x,y)are the top-left coordinate of the rectangle 
    #and (w,h) are its width and height.
    x1,y1,w1,h1 = cv.boundingRect(cnt[0])
    x2,y2,w2,h2 = cv.boundingRect(cnt[1])

    #Corte da imagem de referência
    y=520
    x=25
    h=100
    w=200
    crop = img_[y:y+h, x:x+w]
    crop, contour, hierarchy= cv.findContours(crop,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    barra = sorted(contour,key=cv.contourArea, reverse=True)
    cv.drawContours(crop, barra, 7, (100,255,0), 3)
    xb,yb,wb,hb = cv.boundingRect(barra[7])
    pixelparamicrometro = referencia/wb
    pixelmicroquadrado = pixelparamicrometro*pixelparamicrometro
    print("Largura da barra: "+str(wb)+" pixels")
    print("um pixel mede: "+str(pixelparamicrometro)+" micrometros")
    print("Area 1: "+str(cv.contourArea(cnt[0])*pixelmicroquadrado)+" micrometros quadrados")
    print("Largura 1: "+str(w1*pixelparamicrometro)+" um    Altura 1: "+str(h1*pixelparamicrometro)+" um")
    print("Area 2: "+str(cv.contourArea(cnt[1])*pixelmicroquadrado)+" micrometros quadrados")
    print("Largura 2: "+str(w2*pixelparamicrometro)+" um    Altura 2: "+str(h2*pixelparamicrometro)+" um")
    cv.waitKey()

    #background e 0 e depois adicionamos 1 a todos da matriz para virar o 1

    #marcamos o que estiver preto com 0

    #aplica watershed

def Histograma(imagem):
    try:
        imagem = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
    except:
        pass
    hist = cv.calcHist(imagem,[1],None,[256],[0,256])
    plt.hist(imagem.ravel(),256,[0,256]); plt.show()
    cv.waitKey()


#*************************************INTERFACE*************************************
def  Interface():
    global img_
    global s1
    global img_1
    winname = "Menu"
    cv.imshow(winname, img_)
    k = cv.waitKey()
    if k == 27:      #Se apertar ESC: sai do programa
        SaveImage()
        cv.destroyWindow("Menu")
    elif k == 49:        #Se apertar 1: Ajuste de Contraste e Brilho
        ConstrasteBrilho()
        cv.destroyWindow("Menu")
    elif k == 50:      #Se apertar 2: Filtro de Ruidos
        Denoise()
        cv.destroyWindow("Menu")
    elif k == 51:      #Se apertar 3: Canny
        Canny()
        cv.destroyWindow("Menu")
    elif k == 52:      #Se apertar 4: Filtros Gradientes
        GradientFilters(-1)
        cv.destroyWindow("Menu")
    elif k == 53:      #Se apertar 5: Threshold
        Thresh()
        cv.destroyWindow("Menu")
    elif k == 54:      #Se apertar 6: Sharpen 2
        Sharpen()
        cv.destroyWindow("Menu")
    elif k == 55:      #Se apertar 7: Median Blur
        MedianBlur()
        cv.destroyWindow("Menu")
    elif k == 56:      #Se apertar 8: Mean Shift Blur
        MeanShift()
        cv.destroyWindow("Menu")
    elif k == 97:      #Se apertar A: And Logico
        try:
            img_ = cv.add(img_,s1)
        except:
            print("Não pode somar cinza com colorido")
        cv.destroyWindow("Menu")
    elif k == 101:      #Se apertar E: Equaliza Histograma
        img_1 = img_
        img_ = EqualizaHistograma(img_)
        cv.destroyWindow("Menu")
    elif k == 102:      #Se apertar F: Find Contour
        FindContours()
    elif k == 103:     #Se apertar G: Grayscale
        try:
            img_1 = img_
            img_ = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
        except :
            print ("Já está em Grayscale.")
        cv.destroyWindow("Menu")
    elif k == 104:      #Se apertar H: Mostra Histogramas
        Histograma(img_)
        cv.destroyWindow("Menu")
    elif k == 105:     #Se apertar I: Inverter
        img_ = cv.bitwise_not(img_)
        cv.destroyWindow("Menu")
    elif k == 109:     #Se apertar M: Memorizar
        s1 = img_
        print ("imagem salva em S1")
        cv.destroyWindow("Menu")
    elif k == 114:     #Se apertar R: Resetar
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        cv.destroyWindow("Menu")
    elif k == 122:     #Se apertar Z: Desfazer
        img_= img_1
        cv.destroyWindow("Menu")
    else:              #Se apertar qualquer tecla: imprime a tecla 
        print("Selecione um comando válido! Você digitou: "+str(k))
        cv.destroyWindow("Menu")
    Interface()
    
#*************************************Main*************************************

Interface()