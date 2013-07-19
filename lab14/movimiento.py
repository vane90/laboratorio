import pygame, sys, time
from pygame.locals import *
import Image
import numpy as np
import math
from sys import argv
from math import *
import random


img='nuevo.png'
ancho=300
alto=300
ventana=None

def open_p():
    imagen=Image.open('nuevo.png')
    pixels=imagen.load()
    return pixels
    
def detect_motion(pix1,pix2):
    global img,ancho,alto
    pix=[pix1,pix2]
    for p in pix:
       
        formas(p)
    return            

def formas(pix):
    image = filtro(pix)
   
    image_c,minimo,maximo,gx,gy,conv = mascara(image)
    pix_n=normalizar(image_c,minimo,maximo,conv)
    pix_b= binarizar(pix_n)
    deteccion(pix_b,pix_b)

def deteccion(img,im):
    imagen,masa,centros=c_colorear(img,im)
    return masa,imagen,centros

def c_colorear(im,imag):
    pixels=im.load()
    global ancho,alto
    porcentajes=[]
    fondos=[]
    centro_masa=[]
    masa=[]
    ancho,alto=im.size
    t_pixels=ancho*alto
    c=0
    pintar=[]
    f=0
    m=[]
    for i in range(ancho):
        for j in range(alto):
            pix = pixels[i,j]
            r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)
            fondo=(r,g,b)
            if (pix==(0,0,0)):
                
                c +=1
                origen=(i,j)
                num_pixels,abscisa,ordenada,puntos=bfs(pix,origen,imag,fondo)
                p=(num_pixels/float(t_pixels))*100
                if p>.3:
                    centro=(sum(abscisa)/float(num_pixels),sum(ordenada)/float(num_pixels))
                       
                    masa.append(num_pixels)
                    
                    porcentajes.append(p)
                    
                    fondos.append(fondo)
                    centro_masa.append(centro)
    print centro
    
    im.save('formas.png')
    return im,m,centro_masa

def bfs(pix,origen,im,fondo):
    pixels=im.load()
    cola=list()
    lista=[-1,0,1]
    abscisa=[]
    ordenada=[]
    puntos=[]
    cola.append(origen)
    original = pixels[origen]
    num=1
    while len(cola) > 0:
        (i,j)=cola.pop(0)
        actual = pixels[i,j]
        if actual == original or actual==fondo:
            for x in lista:
                for y in lista:
                    a= i+x
                    b = j+y 
                    try:
                        if pixels[a,b]:
                            contenido = pixels[a,b]
                            if contenido == original:
                                pixels[a,b] = fondo
                                abscisa.append(a)
                                ordenada.append(b)
                                num +=1
                                cola.append((a,b))
                                puntos.append((a,b))
                    except IndexError:
                        pass
    return num,abscisa,ordenada,puntos

def normalizar(image,minimo,maximo,conv):
    pixels=image.load()
    global anocho,alto
    r = maximo-minimo
    prop = 255.0/r
    for i in range(ancho):
        for j in range(alto):
            p =int(floor((conv[i,j]-minimo)*prop))
            pixels[i,j]=(p,p,p);
    image.save('normalizar.png')
    return image

def binarizar(img):
    global anocho,alto
    pixels=img.load()
    img.save('para.png')
    minimo = int(argv[1])
    for i in range(ancho):
        for j in range(alto):
           
            if pixels[i,j][0] < minimo:
                p=0
               
            else:
                p= 255
            pixels[i,j]=(p,p,p)
    img.save('binarizar.png')
    return img

def mascara(image):
#Mascara Sobel
    sobelx = ([-1,0,1],[-2,0,2],[-1,0,1]) #gradiente horizontal
    sobely = ([1,2,1],[0,0,0],[-1,-2,-1]) # gradiente vertical    
    pixels,minimo,maximo,gx,gy,conv=convolucion(sobelx,sobely,image)
    return pixels,minimo,maximo,gx,gy,conv

    
def convolucion(h1,h2,image):
    global ancho,alto
    pixels=image.load()
    a=len(h1[0])
    conv = np.empty((ancho, alto))
    gx=np.empty((ancho, alto))
    gy=np.empty((ancho, alto))
    minimo = 255
    maximo = 0
    for x in range(ancho):
        for y in range(alto):
            sumax = 0.0
            sumay = 0.0
            for i in range(a): 
                for j in range(a): 
                    try:
                        sumax +=(pixels[x+i,y+j][0]*h1[i][j])
                        sumay +=(pixels[x+i,y+j][0]*h2[i][j])
                        
                    except:
                        pass
            gradiente = math.sqrt(pow(sumax,2)+pow(sumay,2))
            conv[x,y]=gradiente
            gx[x,y]=sumax
            gy[x,y]=sumay
            gradiente = int(gradiente)
            pixels[x,y] = (gradiente,gradiente,gradiente)
            p = gradiente
            if p <minimo:
                minimo = p
            if  p >maximo:
                maximo = p
    image.save('convolucion.png')
    return image,minimo,maximo,gx,gy,conv

def filtro(pix):
    global ancho,alto
    imagen = Image.new('RGB', (ancho, alto), (255, 255, 255))
    image=escala_grises(pix,imagen)
    pixels=image.load()
    lista = [-1,0,1]
    for i in range(ancho):
        for j in range(alto):
    
            promedio = vecindad(i,j,lista,image)
    
            pixels[i,j] = (promedio,promedio,promedio)
    image.save('filtro.png')
    return image

def vecindad(i,j,lista,image):
    
    pixels=image.load()
    promedio = 0
    indice  = 0
    for x in lista:
        for y in lista:
    
            a = i+x
            b = j+y
            try:
                if pixels[a,b] and (x!=a and y!=b):
                    promedio += pixels[a,b][0] 
                    indice +=1            
            except IndexError:
                pass
    try:
        promedio=int(promedio/indice)
        return promedio
    except ZeroDivisionError:
        return 0

def escala_grises(pix,image):
    p=image.load()
    global ancho,alto
    pixels = pix
    matriz = np.empty((ancho, alto))
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = pixels[i,j]
            escala = (r+g+b)/3
            pixels[i,j] = (escala,escala,escala)
            p[i,j]=(escala,escala,escala)
    image.save('escala.png')
    return image

NUMBER = 0
def main():

    anterior=None
    siguiente=None
    global img,ventana
    pygame.init()
    ancho = 400
    alto = 400
    ventana= pygame.display.set_mode((ancho, alto), 0, 32)
    pygame.display.set_caption('Deteccion de Movimiento')

    global NUMBER
    DOWNLEFT = 5
    LEFT = 7
    DOWNRIGHT = 5
    RIGHT = 9
    UPRIGHT = 3
    UPLEFT=3
    DOWNRIGHT = 5
    MOVESPEED = 20
    RED = (25, 120, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    

    b = {'rect':pygame.Rect(100, 50, 100, 50), 'color':BLUE, 'dir':LEFT}
    blocks = [b]
    b2 = {'rect':pygame.Rect(50, 50, 50, 50), 'color':GREEN, 'dir':RIGHT}
    blocks = [b2]
    while True:        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
        ventana.fill((0,0,0))
        
        for b in blocks:
            
            if b['dir'] == LEFT:
                b['rect'].left -= MOVESPEED
                b['rect'].top += MOVESPEED
  	print 'izquierda', MOVESPEED
            if b['dir'] == RIGHT:
                b['rect'].left += MOVESPEED
                b['rect'].top += MOVESPEED
		print 'derecha', MOVESPEED
            if b['dir'] == DOWNLEFT:
                b['rect'].left -= MOVESPEED
                b['rect'].top -= MOVESPEED
            if b['dir'] == DOWNRIGHT:
                b['rect'].left += MOVESPEED
                b['rect'].top -= MOVESPEED

        
            if b['rect'].top < 0:
                
                
                if b['dir'] == RIGHT:
                    b['dir'] = UPRIGHT
		if b['dir'] == LEFT:
                    b['dir'] = UPLEFT
            if b['rect'].left < 0:
                if b['dir'] == UPLEFT:
                    b['dir'] = UPRIGHT
                if b['dir'] == LEFT:
                    b['dir'] = RIGHT
            if b['rect'].right > alto:
                if b['dir'] == UPRIGHT:
                    b['dir'] = UPLEFT
                if b['dir'] == RIGHT:
                    b['dir'] = LEFT

        
        pygame.draw.rect(ventana, b['color'], b['rect'])

        if anterior==None:
            pix_a=open_p()
            anterior=pix_a
            print 'anterior',anterior
        else:
            pix_s=open_p()
            siguiente=pix_s
            print 'siguiente'
            detect_motion(pix_a,pix_s)
            anterior=siguiente            
            print 'detect'
	pygame.image.save(ventana,str(NUMBER+1)+'.png')
	NUMBER += 1
       
        pygame.display.update()
        time.sleep(0.01)
if __name__ == "__main__":
    main()        
