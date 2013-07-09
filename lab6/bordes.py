import Image
import random
import numpy as np
import math
from math import *
from sys import argv
import numpy 

#mascaras
mascarax = ([-1,0,1],[-2,0,2],[-1,0,1]) 
mascaray = ([1,2,1],[0,0,0],[-1,-2,-1])      

def mascara(image): 
    img,g_x,g_y,minimo,maximo,borde=aplica_m(mascarax,mascaray,image)
    return img,g_x,g_y,minimo,maximo,borde

def aplica_m(mascarax,mascaray,image):
    imagen_o = image.load()
    x, y = image.size 
    matriz=len(mascarax[0])
    borde = np.empty((x, y))
    g_x = numpy.empty((x, y))
    g_y = numpy.empty((x, y))
    minimo = 255
    maximo = 0
    for l in range(x):
        for k in range(y):
            sumax = 0.0
            sumay = 0.0
            for i in range(matriz): 
                for j in range(matriz): 
                    try:
                        sumax +=(imagen_o[l+i,k+j][0]*mascarax[i][j])
                        sumay +=(imagen_o[l+i,k+j][0]*mascaray[i][j])

                    except:
                        pass
            grad = math.sqrt(pow(sumax,2)+pow(sumay,2))
            borde[l,k]=grad
            g_x[l,k]=sumax
            g_y[l,k]=sumay
            grad = int(grad)
            imagen_o[l,k] = (grad,grad,grad)
            c = grad
            if c < minimo:
                minimo = c
            if  c > maximo:
                maximo = c
    return image,g_x,g_y,minimo,maximo,borde

def imagen(img):
  image = hacer_difusa(img)
	image,g_x,g_y,minimo,maximo,borde = mascara(image)
	img=im_normal(image,minimo,maximo,borde)
	img.save('normalizada.png')
	im_bin,tomap = b_n(img)
	img.save('binariza.png')
	return im_bin,g_x,g_y,minimo,maximo,borde,tomap


def im_normal(image,minimo,maximo,borde):
    imagen_n = image.load()
    dif = maximo-minimo
    todos = 255.0/dif
    x,y = image.size
    for i in range(x):
        for j in range(y):
            pixel =int(floor((borde[i,j]-minimo)*todos))
            imagen_n[i,j]=(pixel,pixel,pixel);
	return image

def b_n(img):
    imagen_bin = img.load()
    x,y = img.size
    tomap = numpy.empty((x, y))
    #minimo = 60
    minimo = int(argv[2])
    for i in range(x):
        for j in range(y):
            if imagen_bin[i,j][1] < minimo:
                p=0
            else:
                p= 255
            imagen_bin[i,j]=(p,p,p)
            tomap[i,j]= p
    return img,tomap


def escala(image):
    image = Image.open(image)
    imagen_e = image.load()
    x,y = image.size
    tomap = numpy.empty((x, y))
    for i in range(x):
        for j in range(y):
            (r,g,b) = image.getpixel((i,j))
            esc = (r+g+b)/3
            imagen_e[i,j] = (esc,esc,esc)
            tomap[i,j] = int(esc)
    a = image.save('escala.png')
    return image,tomap


def hacer_difusa(image):
    image,tomap = escala(image)
    imagen_fil = image.load()
    x, y =image.size
    l_pix = [-1,0,1]
    for i in range(x):
        for j in range(y):
            prom_v = pix_v(i,j,l_pix,tomap)
            imagen_fil[i,j] = (prom_v,prom_v,prom_v)
    return image



def pix_v(i,j,l_pix,tomap):
    promedio = 0
    m  = 0
    for l in l_pix:
        for k in l_pix:
            a = i+l
            b = j+k
            try:
                if tomap[a,b] and (l!=a and k!=b):
                    promedio += tomap[a,b] 
                    m +=1            
            except IndexError:
                pass
            try:
                promedio=int(promedio/m)
                return promedio
            except ZeroDivisionError:
                return 0  

def es_pixel(i,j,pix,tomap,x,y):
    selec_pix=[]
    for l in pix:
        for k in pix:
            a = i+l
            b = j+k
            try:
                if a >= 0 and a < x and b >= 0 and b < y:
                  selec_pix.append(tomap[a,b])
            except IndexError:
                pass
         
    return selec_pix

def borde_del(image,tomap): #morfologias erosion
	imagen_d = image.load()
	x, y =image.size
	tomap_2 = numpy.empty((x, y))
	pix = [-1,0,1]
	for i in range(x):
		for j in range(y):
			borde_min = es_pixel(i,j,pix,tomap,x,y)
			borde_min = int(min(borde_min))
			tomap_2[i,j] = borde_min
			imagen_d[i,j] = (borde_min,borde_min,borde_min)
	image.save('delgado.png')
	return image,tomap_2

def borde_gr(image,tomap): #morfologias dilatacion
	imagen_g = image.load()
	x, y =image.size
	pix = [-1,0,1]
	for i in range(x):
		for j in range(y):
			borde_max = es_pixel(i,j,pix,tomap,x,y)
			borde_max = int(max(borde_max))
			imagen_g[i,j] = (borde_max,borde_max,borde_max)
	image.save('grueso.png')
	return image


def main():
	#mascarax = ([-1,0,1],[-2,0,2],[-1,0,1]) 
    	#mascaray = ([1,2,1],[0,0,0],[-1,-2,-1])     
    		
	
	imagen_f,g_x,g_y,minimo,maximo,borde,tomap=imagen(argv[1])
	erosion,tomap=borde_del(imagen_f,tomap)
	image=borde_gr(erosion,tomap)
    		

if __name__ == "__main__":
     main()
