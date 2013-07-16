import sys, pygame
import Image
from sys import argv
from math import sqrt, sin, cos, fabs
import numpy
from time import*
import math
import ImageDraw
import random

def main():
    imagen1 = circulos()
    #img = pygame.image.load(imagen2)




def circulos():    
    ima1 = Image.open("circulos.png")
    imagen = ima1.load()

    r = int(argv[1])                                              
    ancho,alto = ima1.size
    #frec = list()
    frec = numpy.empty((ancho, alto)) #frecuecia en centros 
    #frec = []
    
    mat_x = ([-1,0,1],[-2,0,2],[-1,0,1])
    mat_y = ([1,2,1],[0,0,0],[-1,-2,-1])
                                                              
    for i in range(ancho):
        for j in range(alto):
            sumx=0.0
            sumy = 0.0
            for m in range(len(mat_x[0])):
                for h in range(len(mat_y[0])):
                    try:
                        mul_x= mat_x[m][h] * imagen[i+m, j+h][0]
                        mul_y= mat_y[m][h] * imagen[i+m, j+h][0]
                    except:
                        mul_x=0
                        mul_y=0
                    sumx=mul_x+sumx
                    sumy=mul_y+sumy
            gx = pow(sumx,2)
            gy = pow(sumy,2)
            grad = int(math.sqrt(gx + gy))
            #obtener votos y centros
            if fabs(grad) > 0:
                costheta = (float(sumx / grad))
                sintheta = (float(sumy / grad))
                xc = int(round(i - r * costheta))
                yc = int(round(j - r * sintheta))
                xcm = (xc + alto)/2
                ycm = (ancho/2) - yc
                #centro = (xc)
                if ycm >= 0 and xcm < alto and xcm >= 0 and ycm < ancho:
                    frec[xcm][ycm] += 1
 #   agregar los votados
    for rango in range(1, int(round(alto*0.1))):
         agregado = True
         while agregado:
             agregado = False
             for y in range(ancho):
                 for x in range(alto):
                     v = frec[y][x]
                     if v > 0:
                          for dx in range(-rango, rango):
                               for dy in range(-rango, rango):
                                    if not (dx == 0 and dy == 0):
                                        if y + dy < ancho and y + dy >= 0 and x + dx >=0 and x + dx < ancho:
                                             w = frec[y+dy][x+dx]
                                             if w >0:
                                                 if v -rango >=w:
                                                     frec[y][x] = v + w
                                                     frec[y+dy][x+dx] = 0
                                                     agregado = True
    #return frec
#votos codigo Dra                     
    maximo = 0
    suma = 0.0
    print "sumando"
    for i in range(alto):
        for j in range(ancho):
            v = frec[j][i]
            suma += v
            if v > maximo:
                maximo = v
    promedio = suma / (ancho * alto)
    umbral = (maximo-promedio)/2.0

    centro = []
    for i in range(alto):
            for j in range(ancho):
                v = frec[j][i]
                if v > umbral:
                    print 'Posible centro en (%d, %d). ' % (j, i)
                    centro.append((j,i))    
#def dibujac(ima1, radio, centro)
    #Dibuja circulo
    draw = ImageDraw.Draw(ima1)
    ancho,alto = ima1.size
    for c in range(len(centro)):
        a = centro[c][0]
        b = centro[c][1]
        color = (255,random.randint(200,255), random.randint(0,200))
#toma el valor de  para dibujar los circulos
        draw.ellipse((a-r, b-r,a+r,b+r),  fill=None, outline=color)
        r+=1
        draw.ellipse((a-r, b-r, a+r,b+r), fill=None, outline=color)
        r+=2
        #draw.ellipse((a-radio))
#Etiquetas y Id
        draw.ellipse((a-2,b-2,a+2,b+2),fill="green")
        draw.text(((a+2,b+2)), str(c),fill="red")
        print "ID %s"%c
    print frec
    nueva = 'circulo.png'
    otra = ima1.save(nueva)
    return nueva

if __name__ == "__main__":
    main()
