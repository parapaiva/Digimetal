#FILtra, MEDe e desENHA
import cv2 as cv
import numpy as np
import statistics
import math

#Le a imagem, reduz e faz copia grayscale
img = cv.imread('teste.tif')
img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
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

#*************************************MeanShift*************************************
#maximos
max_color = 50; max_spatial = 50; 
#variaveis para Filtro
color_ = 21; spatial_ = 21; 

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

#*************************************Prefiltragem*************************************
def PreFiltragem():
    global s1
    global img_
    global img_1
    #Pre filtragem
    filtrado = cv.medianBlur(img_,15)
    try:
        filtrado = cv.pyrMeanShiftFiltering(filtrado, 35, 32)
        filtrado = cv.cvtColor(filtrado, cv.COLOR_BGR2GRAY)
    except:
        pass
    return filtrado

#*************************************Isolate Deposition Area*************************************
def IsolateDepArea(imagem): #esta pegando a de diluicao e a de deposicao juntas
    #Isola parte de interesse
    ret,areadecima = cv.threshold(imagem,17,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    #Remove fundo
    ret,areadecima = cv.threshold(areadecima,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    return areadecima

#*************************************Isolate Thermal Affected Area*************************************
def IsolateThermalArea(imagem):
    #Isola parte de interesse
    ret,areadebaixo = cv.threshold(imagem,70,255,cv.ADAPTIVE_THRESH_MEAN_C)
    #Remove fundo
    ret,areadebaixo = cv.threshold(areadebaixo,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    return areadebaixo

#*************************************Isolate Dilution Area*************************************
#def IsolateDilArea(imagem): # Nao esta funcionando ainda

#*************************************Isolate White Areas*************************************
def IsolateWhiteAreas():
    global s1
    global img_
    global img_1
    #Pre filtragem
    filtrado = PreFiltragem()
    #Isolar area debaixo
    areadebaixo = IsolateThermalArea(filtrado)
    #Isolar area de cima
    areadecima = IsolateDepArea(filtrado)
    #somar com imagem original
    try:
        s1 = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
    except:
        pass
    soma1 = cv.add(areadebaixo,s1)
    #Soma Final
    img_ = cv.add(soma1,areadecima)
    #Remove fundo
    ret,img_ = cv.threshold(img_,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    cv.imshow("Soma final",img_)
    cv.waitKey()
    cv.destroyWindow("Soma final")


#*************************************Find Contours*************************************
def Corte(imagem):
    global img_
    y=520
    x=25
    h=100
    w=200
    try:
        imagem = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
        ret,imagem = cv.threshold(imagem,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    except:
        pass
    crop = imagem[y:y+h, x:x+w]
    crop, contour, hierarchy= cv.findContours(crop,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    barra = sorted(contour,key=cv.contourArea, reverse=False)
    xb,yb,wb,hb = cv.boundingRect(barra[0])
    return xb,yb,wb,hb

def CalculoImagemSemDesenho(imagem):
    global img_
    img, contorno_baixo, hierarchy= cv.findContours(imagem,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Organiza imagem por area, da maior para menor
    cnt = sorted(contorno_baixo,key=cv.contourArea, reverse=True)
    #Desenha Contornos
    #Extrai as medidas extremas das Areas
        #(x,y)are the top-left coordinate of the rectangle 
        #and (w,h) are its width and height.
    x,y,w,h = cv.boundingRect(cnt[0])
    a = cv.contourArea(cnt[0])
    return a,x,y,w,h

def CalculoImagem(imagem):
    global img_
    img, contorno_baixo, hierarchy= cv.findContours(imagem,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Organiza imagem por area, da maior para menor
    cnt = sorted(contorno_baixo,key=cv.contourArea, reverse=True)
    #Desenha Contornos
    cv.drawContours(img_, cnt, 0, (100,255,0), )
    #Extrai as medidas extremas das Areas
        #(x,y)are the top-left coordinate of the rectangle 
        #and (w,h) are its width and height.
    x,y,w,h = cv.boundingRect(cnt[0])
    a = cv.contourArea(cnt[0])
    return a,x,y,w,h

def CalculoImagemPeq(imagem):
    global img_
    img, contorno_baixo, hierarchy= cv.findContours(imagem,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Organiza imagem por area, da maior para menor
    cnt = sorted(contorno_baixo,key=cv.contourArea, reverse=True)
    #Desenha Contornos
    cv.drawContours(img_, cnt, 1, (100,255,0), )
    #Extrai as medidas extremas das Areas
        #(x,y)are the top-left coordinate of the rectangle 
        #and (w,h) are its width and height.
    x,y,w,h = cv.boundingRect(cnt[1])
    a = cv.contourArea(cnt[1])
    return a,x,y,w,h

def YdaImagem(imagem):
    global img_
    src, contorno_baixo, hierarchy= cv.findContours(imagem,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Organiza imagem por area, da maior para menor
    cnt = sorted(contorno_baixo,key=cv.contourArea, reverse=True)
    #Extrai as medidas extremas das Areas
        #(x,y)are the top-left coordinate of the rectangle 
        #and (w,h) are its width and height.
    x,y,w,h = cv.boundingRect(cnt[0])
    return y

def MediaDeLados(divisaonomeio):
    esque=[]
    direi=[]
    y_esque=[]
    y_direi=[]
    y_vazio=[]
    lenght = img_.shape[1] #por enquanto 819
    #"a" e "b" sao os pontos limites da Adep
    a = int(lenght/4)
    #Mostra a area lida para fazer a regressao linear
    img_direi = divisaonomeio[:,0:a]
    img_esque = divisaonomeio[:,-a:-1]
    cv.imshow("Faixa lida na esquerda",img_direi)
    cv.imshow("Faixa lida na direita",img_esque)
    cv.waitKey()
    cv.destroyWindow("Faixa lida na esquerda")
    cv.destroyWindow("Faixa lida na direita")
    for i in range(0,a,2):#step=2
        #Adiciona a posicao y listas para fazer a regressao linear
        y_esque.append(YdaImagem(divisaonomeio[:,i:i+2]))
        y_esque.append(YdaImagem(divisaonomeio[:,i:i+2]))
        y_direi.append(YdaImagem(divisaonomeio[:,-i-3:-i-1]))
        y_direi.append(YdaImagem(divisaonomeio[:,-i-3:-i-1]))
    #Preenche os meios com o maximo das faixas medidas
    max_esq = a*[np.max(y_esque)]
    max_dir = a*[np.max(y_direi)]
    y = y_esque+max_esq+max_esq+y_direi
    #Faz regressao linear
    series=np.polyfit(range(0,4*a),y,1)
    #series = m*x + b, x_zero=0 e x_final=816
    y_zero= int(0*series[0] + series[1])
    y_final= int(4*a*series[0] + series[1])
    area,x,y,w,h = CalculoImagemSemDesenho(divisaonomeio)
    #Calcular angulacao da reta media
    #Rotacionar imagem para m = 0
    return y_zero,y_final,series[0]

def IsolateDivisionLine(imagem):
    #Prefiltragem
    kernel = np.ones((3,3),np.uint8)
    try:
        divisaonomeio = cv.medianBlur(imagem,3)
        divisaonomeio = cv.pyrMeanShiftFiltering(divisaonomeio,33,40)
        divisaonomeio = cv.cvtColor(divisaonomeio, cv.COLOR_BGR2GRAY)
    except:
        print ("Faiou")
    #Isola parte de interesse
    ret,divisaonomeio = cv.threshold(divisaonomeio,33,255,cv.ADAPTIVE_THRESH_MEAN_C)
    divisaonomeio = cv.morphologyEx(divisaonomeio, cv.MORPH_OPEN, kernel)
    #Pega medidas da imagem para construcao da linha: w, y1 e y2
    a,x,y,w,h = CalculoImagemSemDesenho(divisaonomeio)
    y1,y2,m = MediaDeLados(divisaonomeio)
    Adep = IsolateDepArea(imagem)
    Adil = IsolateDepArea(imagem)
    cv.line(Adep,(0,y1+4),(w,y2+4),(0,0,0),2)
    cv.line(Adil,(0,y1-1),(w,y2-1),(0,0,0),2)
    cv.imshow("Adep",Adep)
    cv.imshow("Adil",Adil)
    cv.waitKey()
    #PROBLEMA DA ROTACAO
        #cv.imshow("teste sem rotacao",divisaonomeio)
        #print("inicial: ",y1,y2,m)
        #m eh a angulacao da reta y=m*x + b
        #Calcular angulacao a partir de m = tg(alpha)
        #alpha = np.arctan(m)
        #Rotacionar imagem por alpha
        #Novo calculo para linha
        #cv.line(divisaonomeio,(0,y1),(w,y2),(100,100,100),1)
        #cv.imshow("teste rotacao",imagem_rot)
        #cv.waitKey()
    return Adep,Adil

def FindContours():
    global img_
    #essa referencia podera ser lida da imagem
    referencia = 500
    kernel = np.ones((3,3),np.uint8)
    #Primeiro usamos um Filtros para remover os ruidos
    filtrado = PreFiltragem()
    cv.imshow("Imagem com pre-filtro",filtrado)
    cv.waitKey()
    #achar linha do material base
    areadecima,areadomeio = IsolateDivisionLine(filtrado)
    cv.imshow("Linha de divisao",areadecima)
    cv.waitKey()
    #Isolamos a area debaixo Azta
    areadebaixo = IsolateThermalArea(filtrado)
    #Transformacoes morfologicas para obter um formato genérico
        #Opening aplica uma erosao seguida de dilatacao, remove ruidos
    areadebaixo = cv.morphologyEx(areadebaixo, cv.MORPH_OPEN, kernel)
    areadecima = cv.morphologyEx(areadecima, cv.MORPH_OPEN, kernel)
    areadomeio = cv.morphologyEx(areadomeio, cv.MORPH_OPEN, kernel)
    #Rotular e classificar as areas na imagem
    #Adep(1), Adil(2), Azta(3)
    a1,x1,y1,w1,h1 = CalculoImagem(areadecima)
    a2,x2,y2,w2,h2 = CalculoImagemPeq(areadomeio)
    a3,x3,y3,w3,h3 = CalculoImagem(areadebaixo)
    #Corte da imagem de referência
    xb,yb,wb,hb = Corte(img_)
    #Calcula valores para conversao pixel-mm
        #Estereoscópio<br>
            #295 pixels - 1000um<br>
        #10x
            #1776 pixels - 5000 um<br>
        #12x
            #1799 pixels - 3000 um<br>
        #20x
            #399 pixels - 1000 um<br>
        #16x
            #177pixels - 0.5mm
    pixelparamicrometro = referencia/wb
    pixelmicroquadrado = pixelparamicrometro*pixelparamicrometro
    #prints bonitos
    print("Largura da barra: "+str(wb)+" pixels")
    print("Um pixel mede: "+str(pixelparamicrometro)+" micrometros")
    print("Area de Revestimento: "+str(a1*pixelmicroquadrado/1000000)+" milimetros quadrados")
    print("Area de Penetracao: "+str(a2*pixelmicroquadrado/1000000)+" milimetros quadrados")
    print("Largura: "+str(w1*pixelparamicrometro/1000)+" mm")
    print("Area da Zona Termicamente Afetada: "+str(a3*pixelmicroquadrado/1000000)+" milimetros quadrados")
    cv.waitKey()

#*************************************INTERFACE*************************************
def  Interface():
    global img_
    global s1
    global img_1
    winname = "Menu"
    cv.imshow(winname, img_)
    k = cv.waitKey()
    if k == 49:        #Se apertar 1: 
        FindContours()
        cv.destroyWindow("Menu")
    # elif k == 50:      #Se apertar 2: 
    # elif k == 51:      #Se apertar 3: 
    # elif k == 52:      #Se apertar 4: 
    # elif k == 53:      #Se apertar 5: 
    # elif k == 54:      #Se apertar 6: 
    # elif k == 55:      #Se apertar 7: 
    # elif k == 56:      #Se apertar 8: 
    # elif k == 27:      #Se apertar ESC
    # elif k == 105:     #Se apertar I: 
    # elif k == 122:     #Se apertar Z: 
    # elif k == 97:      #Se apertar A: 
    # elif k == 114:     #Se apertar R: 
    # elif k == 102:      #Se apertar F: Find Contour
    #     FindContours()
    # elif k == 109:     #Se apertar M: 
    # elif k == 103:     #Se apertar G: 
    else:              #Se apertar qualquer tecla: imprime a tecla 
        print("Selecione um comando válido! Você digitou: "+str(k))
        cv.destroyWindow("Menu")
    Interface()

#*************************************Main*************************************
Interface()