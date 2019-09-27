#Software adaptativo de identificacao de grandes areas por contraste
#Utilizando imagens de metalografia: ASTM 316L de 28/11/18
import cv2 as cv
import numpy as np
import statistics
import math
import glob
import pandas as pd

img_ = cv.imread("/Users/Gabiru/Documents/Digimetal/2018.07.03 - A4 - 12X - esc .tif")
img_ = cv.resize(img_, (0,0), fx=0.4, fy=0.4)
imagens = []
nomes = []
nome_do_arquivo = 'nenhum'
data = 0
colunas = ["Nome",
        "Area de Deposição", 
        "Area de Penetração",
        "Area da ZTA", 
        "Largura"]

font                   = cv.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,300)
fontScale              = 0.5
fontColor              = (255,255,255)
lineType               = 1

pixelparamicrometro = 6.94444444444444445 #pixelparamicrometro = referencia/wb
pixelmicroquadrado = pixelparamicrometro*pixelparamicrometro


def ToDataFrame(nome,Adep, Apen, Azta, largura):
    global data1, data
    #se não existe o dataframe, faz um novo
    if data == 0:
        data1 = pd.DataFrame([[nome,Adep, Apen,Azta, largura]],
        columns=colunas)
        data = 1
        data3 = data1
    #se existe dataframe, faz merge
    else:
        data2 = pd.DataFrame([[nome,Adep, Apen, Azta, largura]],
        columns=colunas)
        data3 = pd.merge(data1,
        data2,
        how='outer')
    return data3

def ExportImageData(dataframe,nome="SaídaDigimetal"):
    dataframe.to_excel(r"/Users/Gabiru/Documents/Digimetal/"+nome+".xlsx", 
                    na_rep='NaN', #Missing data representation.
                    float_format="%.5f", 
                    columns=colunas)
    print("Excel exportado como: "+nome+".xlsx")


def DiffString(a,b):
    if len(a)>len(b): 
        res=a.replace(b,'')             #get diff
    else: 
        res=b.replace(a,'')             #get diff
    return res

def EscolhaImagem(dir = "/Users/Gabiru/Documents/Digimetal/"):
    global imagens
    global nomes
    escolha  = cv.imread("/Users/Gabiru/Documents/Digimetal/escolha.jpg")
    escolha = cv.resize(escolha, (0,0), fx=0.4, fy=0.4)
    i = 1
    for file in glob.glob(dir+"*.tif"):
        imagens.append(file)
        cv.putText(escolha,str(i)+": "+file, (10,285+i*15), font, fontScale, fontColor, lineType)
        filename = DiffString(dir,file)
        nomes.append(filename)
        i = i + 1
    cv.imshow("Selecione a imagem: ", escolha)
    k = cv.waitKey()
    cv.destroyWindow("Selecione a imagem: ")
    return k


def MeuImgShow(imagem,nome="Print"): #Reduz tamanho, mostra imagem, espera tecla e fecha imagem
    #imagem = cv.resize(imagem, (0,0), fx=0.4, fy=0.4)
    cv.imshow(nome,imagem)
    k = cv.waitKey()
    cv.destroyWindow(nome)
    return k

#Mede cor do substrato e sobrestrato
def CorSobrestrato(imagem):    #Corta a escala da imagem e tira as suas medidas
    imagem = cv.resize(imagem, (0,0), fx=0.4, fy=0.4)
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        pass
    y=0; x=25; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana1 = np.median(crop)
    y=0; x=600; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana2 = np.median(crop)
    return max(intensidadeMediana1,intensidadeMediana2)

def CorSubstrato(imagem):    #Corta a escala da imagem e tira a mediana de cor
    #imagem = cv.resize(imagem, (0,0), fx=0.4, fy=0.4)
    try:
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    except:
        pass
    y=420; x=25; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana1 = np.median(crop)
    y=520; x=600; h=100; w=200
    crop = imagem[y:y+h, x:x+w]
    intensidadeMediana2 = np.median(crop)
    return max(intensidadeMediana1,intensidadeMediana2)

#Passa filtro de textura
def PreFiltragem(imagem):     #Median Blur (15), Pyramid Mean Shift (35,32)
    #Pre filtragem
    brilho=0
    filtrado = cv.medianBlur(imagem,11)
    #filtrado = cv.convertScaleAbs(filtrado, brilho,1.2,-10)
    try:
        filtrado = cv.pyrMeanShiftFiltering(filtrado, 35, 32)
        filtrado = cv.cvtColor(filtrado, cv.COLOR_BGR2GRAY)
    except:
        print("imagem ja esta em P&B, por isso nao pode passar por um filtro")
        #adicionar algum filtro de media aqui
    return filtrado

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
    if CorSubstrato(imagem) > 100:
        cv.convertScaleAbs(imagem,imagem, 1.7,0)
        print ("clara")
    elif CorSubstrato(imagem) > 80:
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



#Separa a linha divisoria
    #Descobre inclinacao da imagem
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

#Exclui o sobrestrato da imagem
#Separa Arev de Apen
def LinhaMedia(imagem):
    #Isola parte de interesse
    kernel = np.ones((3,3),np.uint8)
    ret,imagem = cv.threshold(imagem,30,255,cv.ADAPTIVE_THRESH_MEAN_C)
    divisaonomeio = cv.morphologyEx(imagem, cv.MORPH_OPEN, kernel)
    #Pega medidas da imagem para construcao da linha: w, y1 e y2
    a,x,y,w,h = CalculoImagemSemDesenho(divisaonomeio)
    y1,y2,m = MediaDeLados(divisaonomeio)
    return w, y1, y2

def IsolarBlob(imagem):     #Isola a mancha central, Area de revestimento + penetracao
    #Isola parte de interesse
    ret,areaDeRevestimento = cv.threshold(imagem,17,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    return areaDeRevestimento

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

#Exclui o subtrato da imagem
#separa ZTA
def IsolarAreaZTA(imagem):      #Isola mancha inferior, zona termicamente afetada
    #Isola parte de interesse
    ret,areaZonaTermicamenteAfetada = cv.threshold(imagem,70,255,cv.ADAPTIVE_THRESH_MEAN_C)
    return areaZonaTermicamenteAfetada

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
    try:
        if color == "green":
            cv.drawContours(img_, cnt, 1, (100,255,0), )
        elif color == "red":
            cv.drawContours(img_,cnt,1,(0,100,255))
        elif color == "blue":
            cv.drawContours(img_,cnt,1,(255,0,100))
        x,y,w,h = cv.boundingRect(cnt[1])
        a = cv.contourArea(cnt[1])
        return a,x,y,w,h
    except:
        print("não há Apen")
        return 0,0,0,0,0   

#Detecta contornos e 
# classifica por posicao Y (quanto maior mais baixo) -> A IMPLEMENTAR
def AreasELarguras(Azta, Arev, Apen):
            #Opening aplica uma erosao seguida de dilatacao, remove ruidos
    kernel = np.ones((3,3),np.uint8)
    Azta = cv.morphologyEx(Azta, cv.MORPH_OPEN, kernel)
    Arev = cv.morphologyEx(Arev, cv.MORPH_OPEN, kernel)
    Apen = cv.morphologyEx(Apen, cv.MORPH_OPEN, kernel)
    #Rotula, classifica e desenha as areas na imagem
    #Arev(1), Apen(2), Azta(3)
    a1,x1,y1,w1,h1 = CalculoImagem(Arev,"blue")
    a2,x2,y2,w2,h2 = CalculoImagemPeq(Apen,"green")
    a3,x3,y3,w3,h3 = CalculoImagem(Azta,"red")
    #Corte da imagem de referência
    xb,yb,wb,hb = CorteEscala(img_)
    return a1, a2,a3, w1,wb 
    #Rotaciona a imagem para tirar a inclinacao


#Mede, calcula e desenha

def Main():
    global data1
    MeuImgShow(img_)
    imagem = PreFiltragem(img_)
    Arev,Apen = SeparaAreasDeClad(imagem)
    Azta = IsolarAreaZTA(imagem)
    Arev, Apen, Azta, w, wb = AreasELarguras(Azta, Arev, Apen)
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
    PrintsBonitos(wb, Arev, Apen, w, Azta)
    Arev = Arev*pixelmicroquadrado/1000000
    Apen = Apen*pixelmicroquadrado/1000000
    Azta = Azta*pixelmicroquadrado/1000000
    w = w*pixelparamicrometro/1000
    data1 = ToDataFrame(winname,Arev,Apen,Azta,w)
    MeuImgShow(imagem,winname)
    Interface()

def PrintsBonitos(wb, a1, a2, w1, a3):
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
    #prints bonitos
    print("Largura da barra: "+str(wb)+" pixels")
    print("Um pixel mede: "+str(pixelparamicrometro)+" micrometros")
    print("Area de Revestimento: "+str(a1*pixelmicroquadrado/1000000)+" milimetros quadrados")
    print("Area de Penetracao: "+str(a2*pixelmicroquadrado/1000000)+" milimetros quadrados")
    print("Largura: "+str(w1*pixelparamicrometro/1000)+" mm")
    print("Area da Zona Termicamente Afetada: "+str(a3*pixelmicroquadrado/1000000)+" milimetros quadrados")

def Interface():
    global img_
    global winname
    winname = "Menu"
    k = EscolhaImagem()
    if k == 49: #Se apertar 1: imagem A4
        img_ = cv.imread(imagens[0])
        img_ = cv.resize(img_, (0,0), fx=0.4, fy=0.4)
        winname = nomes[0]
        Main()
    elif k == 50:      #Se apertar 2: 
        img_ = cv.imread(imagens[1])
        img_ = cv.resize(img_, (0,0), fx=0.4, fy=0.4)
        winname = nomes[1]
        Main()
    elif k == 51:      #Se apertar 3: 
        img_ = cv.imread(imagens[2])
        img_ = cv.resize(img_, (0,0), fx=0.4, fy=0.4)
        winname =nomes[2]
        Main()
    elif k == 52:      #Se apertar 4: 
        img_ = cv.imread(imagens[3])
        img_ = cv.resize(img_, (0,0), fx=0.4, fy=0.4)
        winname = nomes[3]
        Main()
    elif k == 53:      #Se apertar 5: 
        img_ = cv.imread(imagens[4])
        img_ = cv.resize(img_, (0,0), fx=0.4, fy=0.4)
        winname = nomes[4]
        Main()
    elif k == 54:      #Se apertar 6: 
        img_ = cv.imread(imagens[5])
        img_ = cv.resize(img_, (0,0), fx=0.4, fy=0.4)
        winname = nomes[5]
        Main()
    elif k == 103: #Se apertar G: Grayscale
        try:
            img_ = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
        except :
            print ("Já está em Grayscale.")
        Main()
    elif k == 27: #Se apertar ESC: fechar
        print("Fechando programa...")
        ExportImageData(data1)
    else:              #Se apertar qualquer tecla: imprime a tecla 
        print("Selecione um comando válido! Você digitou: "+str(k))
        Main()


Interface()