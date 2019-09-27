#FILtra, MEDe e desENHA
import cv2 as cv
import numpy as np
import statistics
import math
#Le a imagem, reduz e faz copia grayscale
img = cv.imread('/Users/Gabiru/Documents/Digimetal/2018.07.03 - A28- 12X - esc .tif')
img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
#menu da interface, imagem nao esta funcionando por isso nao esta sendo chamada
menu = cv.imread("menu.jpg")
#*************************************SALVAR*************************************
def SaveImage(nomearquivo = "Salva"):       #Salva a imagem atual em JPG
    cv.imwrite(nomearquivo+".jpg",img_)
    print ("Imagem salva como: "+nomearquivo+".jpg")

#*************************************Prefiltragem*************************************
def PreFiltragem():     #Median Blur (15), Pyramid Mean Shift (35,32)
    global img_;
    #Pre filtragem
    filtrado = cv.medianBlur(img_,15)
    try:
        filtrado = cv.pyrMeanShiftFiltering(filtrado, 35, 32)
        filtrado = cv.cvtColor(filtrado, cv.COLOR_BGR2GRAY)
    except:
        print("imagem ja esta em P&B, por isso nao pode passar por um filtro")
        #adicionar algum filtro de media aqui
    return filtrado

#*************************************Isolate Blob Area*************************************
def IsolarBlob(imagem):     #Isola a mancha central, Area de revestimento + penetracao
    #Isola parte de interesse
    ret,areaDeRevestimento = cv.threshold(imagem,17,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    #Remove fundo
    ret,areaDeRevestimento = cv.threshold(areaDeRevestimento,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    return areaDeRevestimento

#*************************************Isolate Thermal Affected Area*************************************
def IsolarAreaZTA(imagem):      #Isola mancha inferior, zona termicamente afetada
    #Isola parte de interesse
    ret,areaZonaTermicamenteAfetada = cv.threshold(imagem,70,255,cv.ADAPTIVE_THRESH_MEAN_C)
    #Remove fundo
    ret,areaZonaTermicamenteAfetada = cv.threshold(areaZonaTermicamenteAfetada,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    return areaZonaTermicamenteAfetada

#*************************************Corte *************************************
def CorteEscala(imagem):    #Corta a escala da imagem e tira as suas medidas
    global img_
    y=520; x=25; h=100; w=200
    #Precisa de um filtro proprio pois no Prefiltro a escala fica apagada
    try:
        imagem = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
        ret,imagem = cv.threshold(imagem,170,255,cv.ADAPTIVE_THRESH_MEAN_C)
    except:
        print("Escala nao foi filtrada")
    crop = imagem[y:y+h, x:x+w]
    crop, contour, hierarchy= cv.findContours(crop,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    barra = sorted(contour,key=cv.contourArea, reverse=False)
    xb,yb,wb,hb = cv.boundingRect(barra[0])
    return xb,yb,wb,hb

#*************************************Calculos de tamanho*************************************
def CalculoImagemSemDesenho(imagem):    #Fornece medidas da maior area da imagem sem desenhar
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

def CalculoImagem(imagem,color="green"):      #Fornece medidas da maior area da imagem
    global img_
    img, contorno_baixo, hierarchy= cv.findContours(imagem,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Organiza imagem por area, da maior para menor
    cnt = sorted(contorno_baixo,key=cv.contourArea, reverse=True)
    #Desenha Contorno na imagem principal
    if color == "green":
        cv.drawContours(img_, cnt, 0, (100,255,0), )
    elif color == "red":
        cv.drawContours(img_,cnt,0,(0,100,255))
    elif color == "blue":
        cv.drawContours(img_,cnt,0,(255,0,100))
    x,y,w,h = cv.boundingRect(cnt[0])
    a = cv.contourArea(cnt[0])
    return a,x,y,w,h

def CalculoImagemPeq(imagem,color="green"):       #Fornece medidas da 2a maior area da imagem
    global img_
    img, contorno_baixo, hierarchy= cv.findContours(imagem,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Organiza imagem por area, da maior para menor
    cnt = sorted(contorno_baixo,key=cv.contourArea, reverse=True)
    #Desenha Contornos na imagem principal
    if color == "green":
        cv.drawContours(img_, cnt, 1, (100,255,0), )
    elif color == "red":
        cv.drawContours(img_,cnt,1,(0,100,255))
    elif color == "blue":
        cv.drawContours(img_,cnt,1,(255,0,100))
    x,y,w,h = cv.boundingRect(cnt[1])
    a = cv.contourArea(cnt[1])
    return a,x,y,w,h

#*************************************Operacoes com imagem*************************************
def YdaImagem(imagem): #Informa a altura da maior area da imagem
    global img_
    ret, contorno_baixo, hierarchy= cv.findContours(imagem,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Organiza imagem por area, da maior para menor
    cnt = sorted(contorno_baixo,key=cv.contourArea, reverse=True)
    #Extrai as medidas extremas das Areas
        #(x,y)are the top-left coordinate of the rectangle 
        #and (w,h) are its width and height.
    x,y,w,h = cv.boundingRect(cnt[0])
    return y

def MediaDeLados(imagem): #Informa qual o y inicial, y final e a angulacao do substrato
    y_esque=[]
    y_direi=[]
    lenght = img_.shape[1] #por enquanto 819
    #"a" eh o ponto onde pode comecar a blob
    a = int(lenght/4)
    #Areas lidas para fazer a regressao linear
    img_direi = imagem[:,0:a]
    img_esque = imagem[:,-a:-1]
    #Nao esta mostrando os lados da imagem que estao sendo usado para tracar a reta
    cv.imshow("Faixa lida na esquerda",img_direi)
    cv.waitKey()
    cv.destroyWindow("Faixa lida na esquerda")
    cv.imshow("Faixa lida na direita",img_esque)
    cv.waitKey()
    cv.destroyWindow("Faixa lida na direita")
    for i in range(0,a,2):#step=2 se faz necessario? um intervalo de 2 pixel tambem?
        #Adiciona a posicao y listas para fazer a regressao linear
        y_esque.append(YdaImagem(imagem[:,i:i+2]))
        y_esque.append(YdaImagem(imagem[:,i:i+2]))
        y_direi.append(YdaImagem(imagem[:,-i-3:-i-1]))
        y_direi.append(YdaImagem(imagem[:,-i-3:-i-1]))
    #Preenche os meios com o maximo das faixas medidas
    max_esq = a*[np.max(y_esque)]
    y = y_esque+max_esq+max_esq+y_direi
    #Faz regressao linear
    series=np.polyfit(range(0,4*a),y,1)
    #series = m*x + b, x_zero=0 e x_final=816 (a*4)
    y_zero= int(0*series[0] + series[1])
    y_final= int(4*a*series[0] + series[1])
    #Calcular angulacao da reta para rotacionar imagem ate que m = 0
    return y_zero,y_final,series[0]

def LinhaMedia(imagem):
    #Isola parte de interesse
    kernel = np.ones((3,3),np.uint8)
    ret,divisaonomeio = cv.threshold(imagem,33,255,cv.ADAPTIVE_THRESH_MEAN_C)
    divisaonomeio = cv.morphologyEx(divisaonomeio, cv.MORPH_OPEN, kernel)
    #Pega medidas da imagem para construcao da linha: w, y1 e y2
    a,x,y,w,h = CalculoImagemSemDesenho(divisaonomeio)
    y1,y2,m = MediaDeLados(divisaonomeio)
    return w, y1, y2

def SeparaAreasDeClad(imagem): #Retorna area acima e abaixo da linha do subtrato
    #Isola parte de interesse
    w, y1, y2 = LinhaMedia(imagem)
    #Ambas areas partem da Blob central
    Arev = IsolarBlob(imagem)
    Apen = IsolarBlob(imagem)
    #Desenhamos uma linha um pouco mais abaixo (somando pixels a sua posicao Y) para Arev
    cv.line(Arev,(0,y1+2),(w,y2+2),(0,0,0),2)
    #e uma linha um pouco mais acima (subtraindo pixels da sua posicao Y) para Apen
    cv.line(Apen,(0,y1),(w,y2),(0,0,0),2)
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
    return Arev,Apen


#*************************************Main*************************************
def Main(): #Pre-filtra, extrai partes de interesse, filtra, mede e desenha.
    global img_
    cv.imshow("Menu",img_)
    #essa referencia podera ser lida da imagem
    referencia = 500
    #Primeiro usamos alguns filtros para remover os ruidos
    filtrado = PreFiltragem()
    cv.imshow("Imagem com pre-filtro",filtrado)
    cv.waitKey()
    cv.destroyWindow("Imagem com pre-filtro")
    #Isola Area de Revestimento da Area de Penetração
    areaDeRevestimento,areaDePenetracao = SeparaAreasDeClad(filtrado)
    cv.imshow("Revestimento",areaDeRevestimento)
    cv.waitKey()
    cv.destroyWindow("Revestimento")
    cv.imshow("Penetracao",areaDePenetracao)
    cv.waitKey()
    cv.destroyWindow("Penetracao")
    #Isola Area da zona termicamente afetada
    areaZonaTermicamenteAfetada = IsolarAreaZTA(filtrado)
    cv.imshow("ZTA",areaZonaTermicamenteAfetada)
    cv.waitKey()
    cv.destroyWindow("ZTA")
    #Transformacoes morfologicas para obter um formato genérico
        #Opening aplica uma erosao seguida de dilatacao, remove ruidos
    kernel = np.ones((3,3),np.uint8)
    areaZonaTermicamenteAfetada = cv.morphologyEx(areaZonaTermicamenteAfetada, cv.MORPH_OPEN, kernel)
    areaDeRevestimento = cv.morphologyEx(areaDeRevestimento, cv.MORPH_OPEN, kernel)
    areaDePenetracao = cv.morphologyEx(areaDePenetracao, cv.MORPH_OPEN, kernel)
    #Rotular e classificar as areas na imagem
    #Arev(1), Apen(2), Azta(3)
    a1,x1,y1,w1,h1 = CalculoImagem(areaDeRevestimento,"blue")
    a2,x2,y2,w2,h2 = CalculoImagemPeq(areaDePenetracao,"green")
    a3,x3,y3,w3,h3 = CalculoImagem(areaZonaTermicamenteAfetada,"red")
    #Corte da imagem de referência
    xb,yb,wb,hb = CorteEscala(img_)
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
    #pixelparamicrometro = referencia/wb
    pixelparamicrometro = 6.94444444444444445
    pixelmicroquadrado = pixelparamicrometro*pixelparamicrometro
    #prints bonitos
    print("Largura da barra: "+str(wb)+" pixels")
    print("Um pixel mede: "+str(pixelparamicrometro)+" micrometros")
    print("Area de Revestimento: "+str(a1*pixelmicroquadrado/1000000)+" milimetros quadrados")
    print("Area de Penetracao: "+str(a2*pixelmicroquadrado/1000000)+" milimetros quadrados")
    print("Largura: "+str(w1*pixelparamicrometro/1000)+" mm")
    print("Area da Zona Termicamente Afetada: "+str(a3*pixelmicroquadrado/1000000)+" milimetros quadrados")

#*************************************INTERFACE*************************************
def  Interface():       #
    global img_; global img
    winname = "Menu"
    cv.imshow(winname, img_)
    k = cv.waitKey()
    if k == 49:        #Se apertar 1: 
        print("Imagem numero 4")
        Main()
        cv.destroyWindow("Menu")
    elif k == 50:      #Se apertar 2: 
        img = cv.imread('Digimetal/2018.07.03 - A10- 12X - esc .tif')
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("Imagem numero 10")
        Main()
    elif k == 51:      #Se apertar 3: 
        img = cv.imread("Digimetal/2018.07.03 - A23- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("Imagem numero 23")
        Main()
    elif k == 52:      #Se apertar 4: 
        img = cv.imread("Digimetal/2018.07.03 - A28- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("Imagem numero 28")
        Main()
    elif k == 53:      #Se apertar 5: 
        img = cv.imread("/Users/Gabiru/Documents/Digimetal/2018.07.03 - A28- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("Imagem numero 30")
        Main()
    elif k == 54:      #Se apertar 6: 
        img = cv.imread("Digimetal/2018.07.03 - A45- 12X - esc .tif")
        img_ = cv.resize(img, (0,0), fx=0.4, fy=0.4)
        print("Imagem numero 45")
        Main()
    else:              #Se apertar qualquer tecla: imprime a tecla 
        print("Selecione um comando válido! Você digitou: "+str(k))
        cv.destroyWindow("Menu")
    Interface()
#*************************************Main*************************************
Interface()