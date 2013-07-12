import Image                 ##para cargar imagenes, matriz de los pixeles
from math import *           ##operaciones
import sys                   ##cosas de sistema como para terminar el programa
import numpy                 ##arreglos
import time
import math
from math import *
import random
from PIL import Image, ImageDraw,ImageFont
Inombre = raw_input("Dame el nombre de la imagen con extencion: ")
nnormal = 'nimagen.png'
ngrises = 'filtro.png'
nfiltro = 'difusion.png'
nconvolucion = 'convolu.png'
numbra = 'umbral.png'
nnorma = 'normalizacion.png'

convx = "convox.png"
convy = "convoy.png"


matriz = ([-1,0,1],[-2,0,2],[-1,0,1])
matriz2=([1,2,1],[0,0,0],[-1,-2,-1])

def cargar(imagen):
  im = Image.open(imagen)
	ancho, altura = im.size
	pixels = im.load()
	return ancho,altura,pixels,im


def bordes(imagen):
	colores = ([130,130,130],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255],[250,0,0]) ##colores
	cola = []
	ancho,altura,pixels,im = cargar(imagen)
	visitados = []
	contcolor = 0
	for y in range(altura):
		visitados.append([])
		for x in range(ancho):
			if pixels[x,y][1] == 0:
				visitados[y].append(1)
				
			else:
				if len(cola) == 0:
                                        cola.append((y,x))
				visitados[y].append(0)			
	while len(cola) > 0:
		tam = len(cola)         ##extraemos datos de la colas
                a = int(cola[tam-1][0]) ##obtenemos direccion a y
		b = int(cola[tam-1][1]) ##b = x
                visitados[a][b] = 1 ##marcamos como visitados
                cola.pop(tam-1) ##borramos de la cola
                try:
                        if pixels[b,a+1][0] == pixels[b,a][0] and visitados[a][b+1] == 0:
				#print "llego a pasar por aqui chngado"
                                cola.append((a,b+1))
                except:
			pass
		try:
                        if pixels[b,a-1][0] == pixels[b,a][0] and visitados[a][b-1] == 0:
				#print "llego a pasar por aqui chngado"
                                cola.append((a,b-1))
		except:
                        pass
                try:
                        if pixels[b+1,a][0] == pixels[b,a][0] and visitados[a+1][b] == 0:
				                        #print "llego a pasar por aqui chngado"
                                cola.append((a+1,b))

                except:
                        pass
                try:
                        if pixels[b-1,a][0] == pixels[b,a][0] and visitados[a-1][b] == 0:
                               # print "llego a pasar por aqui chngado"         
				cola.append((a-1,b))
                except:
			pass
		r =colores[contcolor][0]
		g =colores[contcolor][1]
		h =colores[contcolor][2]
		pixels[b,a] = (r,g,h)
		
		if len(cola) == 0:
						
			j,i = sii(visitados,ancho,altura)
                        if i==0 and j ==0:
                                break
                        else:
                                cola.append((j,i))
                                contcolor = contcolor + 1
                                if contcolor == 7:
                                        contcolor = 1
	
	im.save(pin)
	print "finaliso"
	return 

###funcion de filtro
def filtro(imagen):
	prom = 0
	ancho,altura,pixels,im = cargar(imagen)
	for x in range(altura): ###
		for i in range(ancho):
			suma = 0
			cont = 0
			for j in range(-1,2): ##altura
				for k in range(-1,2): ##ancho
					if i+k >= 0 and i+k < ancho and x+j >= 0 and x+j < altura:
						suma += pixels[i+k,x+j][1]
						cont += 1
			prom = int(suma/cont)		
			pixels[i,x] = (prom,prom,prom)
	im.save(nfiltro)
	return 


def proceso(mx,mex,my,mey,cord):
	puntos = []
	for x in range(len(cord)):
		cx,cy = cord[x][0],cord[x][1]
		if cx == mx:
			puntos.append((cx,cy))
		if cx == mex:
			puntos.append((cx,cy))
		if cy == my:
			puntos.append((cx,cy))
		if cy == mey:
			puntos.append((cx,cy))	
	
	return puntos

def bfsss(j,i):
	ancho,altura,pixels,im = cargar(nconvolucion)
	pro = []
	pro.append((j,i))
	visitados = []
	pintar = []
	visitados = []
	cont = 1
	total = 0
	cord = []
	#print "iniciando bfs"
	for q in range(altura):
		visitados.append([])
		for w in range(ancho):
			total += 1
			if pixels[w,q] == (0,0,0):
				visitados[q].append(0)
			else:
				visitados[q].append(1)
	a,b,c = random.randint(1, 255),random.randint(1, 255),random.randint(1, 255)   		
	while len(pro) > 0:
		x = pro[len(pro)-1][0]
		y = pro[len(pro)-1][1]
		pro.pop(len(pro)-1)
		for i in range(-1,2):
			for j in range(-1,2):
				if x+j >= 0 and y+i >=0 and x+j <ancho and y+i <altura:
					if visitados[y+i][x+j] == 0:
					
						if i == 0 and j == 0:
							cosa = 0
						else:	
							if pixels[x,y][1] == pixels[x+j,y+i][1]:
								pro.append((x+j,y+i))
								visitados[y+i][x+j] = 1
								
								
		cord.append((x,y))						
		pixels[x,y] = (a,b,c)
		visitados[y][x]	= 1
		cont += 1
	return cord		

def convolucion(imagen):
	
	print "Iniciando convolucion: "
	ancho,altura,pixels,im = cargar(imagen)
	matrix = ([-1,0,1],[-2,0,2],[-1,0,1])
        matriy = ([1,2,1],[0,0,0],[-1,-2,-1])
	nueva = Image.new("RGB", (ancho, altura))
	npixels = nueva.load()
	gx = [] ##gradientes de x
	gy = [] ##gradientes de y
	mxy = [] ##la convinacon de ambos
	for i in range(altura):
		gx.append([])
		gy.append([])
		mxy.append([])
		for j in range(ancho):
			sumax = 0
			sumay = 0
			for y in range(-1,2):
				for x in range(-1,2):
					if j+x >= 0 and j+x < ancho and i+y >=0 and i+y < altura: 
						sumax += matrix[y+1][x+1] * pixels[j+x,i+y][1]
						sumay += matriy[y+1][x+1] * pixels[j+x,i+y][1]			
			r = int(math.sqrt(sumax**2+sumay**2)) ##calculamos gradiente mayor 
			gx[i].append(sumax) ##guardamos los gradientes en x
			gy[i].append(sumay) ##guardamos los gradientes en y 
			mxy[i].append(r)    ##guardamos el resultado de los gradientes en x e y
			#r = sumay
			if r < 0:
				r = 0
			if r > 255:
				r = 255	
			
			npixels[j, i] = (r,r,r)
	nueva.save(nconvolucion)		
	
	return gx,gy,mxy


##funcion para la escala de grises
def escala(imagen):
	ancho,altura,pixels,im = cargar(imagen)
	for i in range(ancho):
        	for j in range(altura):
			##sacamos promedio de (r,g,b) de los pixeles
			(a,b,c) = pixels[i,j]	
			suma = a+b+c 
			prom = int(suma/3)
			a = prom ##igualamos
			b = prom ##igualamos
			c = prom ##igualamos 	 		
			pixels[i,j] = (a,b,c) ##igualamos
        im.save(ngrises) ##guardamos la imagen nueva
	return ##enviamos la imagen cargada

##funcion para el umbral
def mumbra(imagen):
	ancho,altura,pixels,im = cargar(imagen)
	for i in range(ancho):
		for j in range(altura):
			(a,b,c) = pixels[i,j] ##obtenemos valore
			prom = a+b+c/3        ##promedio
			if min >= prom:       #condiciones para poner blanco o negro
				prom = 0
			if max <= prom:
				prom = 255
			a = prom              ##asignamos el promedio a los pixeles
			b = prom
			c = prom
			pixels[i,j]=(a,b,c)  ##asiganmos
	im.save(numbra)                     ##guardamos 
	return     


def normalizacion(imagen,d):
	
	tiempoi = time.time()
	ancho,altura,pixels,im = cargar(imagen)
	prom = 0
	maxi = pixels[0,0][1]
	mini = pixels[0,0][1]
	for j in range(altura):
		for i in range(ancho):
			if maxi < pixels[i,j][1]:
				maxi = pixels[i,j][1]
			if mini > pixels[i,j][1]:
				mini = pixels[i,j][1]
	div = 256.0/(maxi-mini)			
	for j in range(altura):
		for i in range(ancho):
			prom = 0
			if i > 0 and j > 0 and i < ancho-1 and j < altura-1:
				prom = int(math.floor((pixels[i,j][1] - mini)*div))
				pixels[i,j] = (prom,prom,prom)
				if pixels[i,j][1] > 60:
					pixels[i,j] = (255,255,255)
				else:
					pixels[i,j] = (0,0,0)
			else:
				pixels[i,j] = (0,0,0)
	im.save(nconvolucion) ##guardamos imagenes
	return nconvolucion


def diferencia(imagen1,imagen2,min,max):
	ancho,altura,pixels,im = cargar(imagen1)
        ancho,altura,pixels,im = cargar(imagen2)
	for i in range (ancho -2):
		for j in range (altura -2):
			(a,b,c) = pixels[i,j] ##guardamos pixeles de ambas 
			(a1,b1,c1) = pixels1[i,j] ##imagenes
			prom = a+b+c/3            ##sacamos propedio de ambas
			prom1 = a1+b1+c1/3
			prom2 = prom - prom1      ##restamos
			v = prom2*255/500
			print v
			if v > 25:            ##aqui asemos binarisasion
				prom2 = 255
			else:
				prom2 = 0
			a = prom2                 ##reasignamos la diferencia
			b = prom2
			c = prom2
			pixels[i,j] = (a,b,c)    ##cambiamos pixeles
	im.save(nimagen)                         ##guardamos imagenes
	return nimagen	##enviamos imagenes cargadas


def comprobacion(imagen,gx,gy):
	ancho,altura,pixels,im = cargar(imagen)
	pro = []
	pro.append((0,0))
	visitados = []
	pintar = []
	cont = 1
	total = 0
	cord = []
	cond = 0
	print "iniciando bfs"
	a,b,c = random.randint(1, 255),random.randint(1, 255),random.randint(1, 255)
	for q in range(altura):
		visitados.append([])
		for w in range(ancho):
			total += 1
			if pixels[w,q] == (255,255,255):
				visitados[q].append(0)
				if cond == 0:
                                        cond = 1
                                        pro.append((w,q))

			else:
				visitados[q].append(1)
	while len(pro) > 0:
		x = pro[len(pro)-1][0]
		y = pro[len(pro)-1][1]
		pro.pop(len(pro)-1)
		for i in range(-1,2):
			for j in range(-1,2):
				if x+j >= 0 and y+i >=0 and x+j <ancho and y+i <altura:
					if visitados[y+i][x+j] == 0:
						if i == 0 and j == 0:
							cosa = 0
						else:
							if pixels[x,y][1] == pixels[x+j,y+i][1]:
								pro.append((x+j,y+i))
						visitados[y+i][x+j] = 1
						
						
		pixels[x,y] = (a,b,c)
		visitados[y][x]= 1
		cont += 1
		cord.append((x,y))
		if len(pro) == 0:
			
			formas(imagen,gx,gy,cord)
			y,x = posible(visitados,ancho,altura)
			
			cord = []
			if x == 0 and y == 0:
				cosa = 1
			else:
				pro.append((x,y))
				a,b,c = random.randint(1, 255),random.randint(1, 255),random.randint(1, 255)
		
			
	return imagen


def posible(visitados,ancho,altura):
	for y in range(altura):
		for x in range(ancho):
			if visitados[y][x] == 0:
				return y,x
	return 0,0	




def formas(imagen,gx,gy,cord):
	ancho,altura,pixels,im = cargar(imagen)
	pro = []
	visitados = []
	pintar = []
	visitados = []
	cont = 1
	total = 0
	cordenadas = []
	a,b,c = random.randint(1, 255),random.randint(1, 255),random.randint(1, 255)		
	cond = 0
	print "iniciando verificacion:"	
	yep = 0
	draw = ImageDraw.Draw(im)
	for q in range(altura):
		visitados.append([])
		for w in range(ancho):						
			total += 1
			yep = 0						
			try:
				l = cord.index((w,q))
				visitados[q].append(0)
				if cond == 0:
                                        cond = 1
                                        pro.append((w,q))
			except:
				visitados[q].append(1)

			
	
	tras = []
	kk = 0
	print "todo bien"
	while len(pro) > 0:
		x = pro[len(pro)-1][0]
		y = pro[len(pro)-1][1]
		pro.pop(len(pro)-1)
		tras.append([])

		
		###nueva pendiente
		if gx[y][x] != 0:
			m = gy[y][x]/gx[y][x]
		else:
			m = gy[y][x]/1
		##nueva pendiente	
		for i in range(-1,2):
			for j in range(-1,2):
				if x+j >= 0 and y+i >=0 and x+j <ancho and y+i <altura:
					if visitados[y+i][x+j] == 0:
											
						if i == 0 and j == 0: ##para no tomar el mismo valor
							cosa = 0
						else:
							if gx[y+i][x+j] != 0:
								m2 = gy[y+i][x+j]/gx[y+i][x+j]
							else:
								m2 = gy[y+i][x+j]/1
							if pixels[x,y][1] == pixels[x+j,y+i][1]: ##siga siendo borde
								if m-3 <= m2 <= m+3:
								#if m == m2:
									pro.append((x+j,y+i))
						visitados[y+i][x+j] = 1
		visitados[y][x]= 1
		cont += 1
		cordenadas.append((x,y))
		tras[kk].append((x,y))
		#yep += 1
		#kk += 1		
		if len(pro) == 0:
			kk = kk + 1
			cont = 0
			cond = 0
			k = 0				
			y,x = posible(visitados,ancho,altura)
			if x == 0 and y == 0:
				cosa = 1
				cordenadas = []
			else:
				cordenadas = []
				pro.append((x,y))
				a,b,c = random.randint(1, 255),random.randint(1, 255),random.randint(1, 255)

	
	cosa = []
	medio = []

	for i in range (len(tras)-1):
		#print len(tras[i])
		if len(tras[i]) > 100:
			#print len(tras[i])
			puntosmedios = []
			
			menorx,menory = tras[i][0]
			mayorx,mayory = tras[i][len(tras[i])-1]
			lines = []
			
			for j in range (len(tras[i])):
				yep += 1 ## eso es para le porcentaje 
				x,y = tras[i][j]
				cosa.append((x,y))
				if menorx > x:
					menorx,menory = tras[i][j]
				if mayorx < x:
					mayorx,mayory = tras[i][j]
					
			mediox,medioy = ((mayorx+menorx)/2,(mayory+menory)/2) ##calculamos medio

			puntosmedios.append((mediox,medioy)) ##los agregamos a una lista para uso posterior

			lines.append((menorx,menory)) ##estos es para juntar y dibujar
			lines.append((mayorx,mayory)) ##esto es para juntar y dibujar
			
			medio.append((mayorx,mayory,menorx,menory)) ##esto es para calcular el centro

			draw = ImageDraw.Draw(im)
			draw.line(lines, fill=500) ##dibujamos lineas
			##aqui dibujamos laas lienas
			##dibujamos puntos medios
			for j in range (-10,11):
				for k in range (-10,11):
					pixels[mediox+k,medioy+j] = (255,255,0)

	##aqui calculamos centro de enmedio		
	menorx,menory = cosa[0]
	mayorx,mayory = cosa[len(cosa)-1]	
	for i in range(len(cosa)):
		x,y = cosa[i]
		if x > mayorx:
			mayorx = x
		if x < menorx:
			menorx = x

		if y > mayory:
			mayory = y
		if y < menory:
			menory = y

			
	centrox,centroy = ((mayorx+menorx)/2,(mayory+menory)/2)		
	for i in range (-10,10):
		for j in range (-10,10):
			pixels[centrox+i,centroy+j] = (255,0,255)
			
	hor = 0
	ver = 0
	print "total de segmentos: ",len(medio)
	for i in range (len(medio)):
		mx,my,mex,mey = medio[i]
		mediox,medioy = ((mx+mex)/2,(my+mey)/2)
		hor = 0
		ver = 0
		lines = []
		
		pixels[mediox,medioy] = (0,255,0)
		diferenciax = centrox - mediox
		diferenciay = centroy - medioy
		mx = mx + diferenciax
		my = my + diferenciay
		mex = mex + diferenciax
		mey = mey + diferenciay
			
		lines.append((mex,mey))
		lines.append((mx,my))		
		draw.line(lines, fill=100)
	
	porcentaje = int(float(yep*100)/float(len(cord)))
	print "porcentaje hacer figura: ",porcentaje
	fuente = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-C.ttf',20)
	draw.text((mediox,medioy), 'L', fill =(0,255,0), font=fuente)
	
	im.save(imagen)
	
	print "termino"
	return 
	
##funcion principla del programa
def main(nombreI):
	ancho,altura,pixels,im = cargar(nombreI)
	imagen = escala(nombreI) 
	imagen = filtro(ngrises)
	gx,gy,mxy = convolucion(nfiltro)
	imagen = normalizacion(nconvolucion,mxy)
	imagen = comprobacion(nconvolucion,gx,gy)
	imagen = filtro(ngrises) ##lo mismo que arriba pero para filtro						
	imagen = formas(nconvolucion,gx,gy,mxy)
	imagen = mumbra(nombreI) ##llama al metodo umbral


main(Inombre)


