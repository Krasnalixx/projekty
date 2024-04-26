import cv2
import numpy as np
import matplotlib.pyplot as plt
sciezka1 = 'dublin.jpg'
sciezka2 = 'dublin_edited.jpg'
obraz1 = cv2.imread(sciezka1)
obraz2 = cv2.imread(sciezka2)
wysokosc = obraz1.shape[0]
szerokosc = obraz1.shape[1]


def wyswietl(red2,green2,blue2):
    plt.subplot(121), plt.imshow(cv2.cvtColor(obraz2, cv2.COLOR_BGR2RGB)), plt.title('Oryginalny Obraz')
    plt.subplot(122), plt.imshow(cv2.merge([red2.astype(np.uint8), green2.astype(np.uint8), blue2.astype(np.uint8)])), plt.title('Zmieniony Obraz')
    plt.show()


def rozdziel_kolory():
    red = np.zeros((wysokosc, szerokosc))
    green = np.zeros((wysokosc, szerokosc))
    blue = np.zeros((wysokosc, szerokosc))
    red2 = np.zeros((wysokosc, szerokosc))
    green2 = np.zeros((wysokosc, szerokosc))
    blue2 = np.zeros((wysokosc, szerokosc))

    for i in range(wysokosc):
        for j in range(szerokosc):
            red[i, j] = obraz1[i, j, 0]
            green[i, j] = obraz1[i, j, 1]
            blue[i, j] = obraz1[i, j, 2]
            red2[i, j] = obraz2[i, j, 0]
            green2[i, j] = obraz2[i, j, 1]
            blue2[i, j] = obraz2[i, j, 2]
    return red,green,blue,red2,green2,blue2


def poprawa(wysokosc2,szerokosc2):
    for i in range(1, wysokosc2-1):
        for j in range(1, szerokosc2 - 1):
            if alpha[i][j - 1] - alpha[i][j + 1] == 0:
                alpha[i][j] = alpha[i][j - 1]
            if alpha[i - 1][j] - alpha[i + 1][j] == 0:
                alpha[i][j] = alpha[i - 1][j]
    for i in range(2, wysokosc2 - 2):
        for j in range(2, szerokosc2 - 2):
            if alpha[i - 2][j] - alpha[i + 2][j] == 0:
                alpha[i][j] = alpha[i - 2][j]
            if alpha[i][j - 2] - alpha[i][j + 2] == 0:
                alpha[i][j] = alpha[i][j - 2]

red,green,blue,red2,green2,blue2=rozdziel_kolory()
zmienione_r = red2
zmienione_g = green2
zmienione_b = blue2
sprawdzone = np.zeros((wysokosc,szerokosc), dtype=np.uint8)
wykrytych =0
wykryte=[]
prog=40

for i in range(wysokosc):
    for j in range(szerokosc):
        if (abs(red[i,j] - red2[i,j]) > prog or abs(green[i,j] - green2[i,j]) > prog or abs(blue[i,j] - blue2[i,j]) > prog) and sprawdzone[i, j] ==0:  #
            max1=i+100
            if max1>szerokosc:
                max1=szerokosc
            max2=j+50
            if max2>wysokosc:
                max2=wysokosc
            min2 = j - 50
            if min2 < 0:
                min2 = 0
            min_x = szerokosc
            max_x = 0
            min_y = None
            max_y = None
            for m in range(i, i + 100):
                for n in range(j - 50, j + 50):
                    if (abs(red[m,n] - red2[m,n]) > prog or abs(green[m,n] - green2[m,n]) > prog or abs(blue[m,n] - blue2[m,n]) > prog) and sprawdzone[m,n]==0:
                        max_y=m
                        if min_y==None:
                            min_y=m
                        if n<min_x:
                            min_x=n
                        if n>max_x:
                            max_x=n
                        sprawdzone[m,n]=1
            wykryte.append([min_x, max_x, min_y, max_y])

for obramowanie in wykryte:
    poszerzenie = 2
    lewa = obramowanie[0] - poszerzenie
    prawa = obramowanie[1] +poszerzenie
    gora = obramowanie[2] -poszerzenie
    dol = obramowanie[3] +poszerzenie
    for i in range(gora,dol+1):
        for j in range(lewa,prawa+1):
            if (i==gora or i==dol or j==lewa or j==prawa) and sprawdzone[i,j]==0:
                zmienione_r[i, j] = 255
                zmienione_g[i, j] = 255
                zmienione_b[i, j] = 255

lewa = wykryte[0][0]
prawa = wykryte[0][1]
gora = wykryte[0][2]
dol = wykryte[0][3]
wysokosc2 = dol - gora
szerokosc2 =prawa - lewa
alpha = np.ones((wysokosc2, szerokosc2)) * 255
red_kevin = np.zeros((wysokosc2, szerokosc2))
green_kevin = np.zeros((wysokosc2, szerokosc2))
blue_kevin = np.zeros((wysokosc2, szerokosc2))
prog=5

for i in range(gora,dol):
    for j in range(lewa,prawa):
        if abs(red[i, j] - red2[i, j]) < prog or abs(green[i, j] - green2[i, j]) < prog or abs(blue[i, j] - blue2[i, j]) < prog:  #
            alpha[i-gora,j-lewa] = 0
        red_kevin[i - gora, j - lewa] = red2[i, j]
        green_kevin[i - gora, j - lewa] = green2[i, j]
        blue_kevin[i - gora, j - lewa] = blue2[i, j]
poprawa(wysokosc2,szerokosc2)
poprawa(wysokosc2,szerokosc2)
poprawa(wysokosc2,szerokosc2)
red_kevin2 = np.zeros((wysokosc2-1, szerokosc2-2))
green_kevin2 = np.zeros((wysokosc2-1, szerokosc2-2))
blue_kevin2 = np.zeros((wysokosc2-1, szerokosc2-2))
alpha2 = np.ones((wysokosc2-1, szerokosc2-2)) * 255

for i in range(wysokosc2-1):
    for j in range(szerokosc2-2):
        red_kevin2[i,j]=red_kevin[i,j+1]
        blue_kevin2[i,j]=blue_kevin[i,j+1]
        green_kevin2[i,j]=green_kevin[i,j+1]
        alpha2[i,j]=alpha[i,j+1]

kolory = np.dstack((red_kevin2, green_kevin2, blue_kevin2, alpha2))
cv2.imwrite('kevin.png', kolory)