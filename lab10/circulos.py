import pygame                
from pygame.locals import *  
import Image                 
from math import *           
import sys                   
import numpy                 
import time
import math
from math import *
import random
from PIL import Image, ImageDraw,ImageFont


Inombre = raw_input("Nombre de la imagen con extencion: ")
nnormal = 'nimagen.png'
ngrises = 'filtro.png'
nfiltro = 'difusion.png'
nconvolucion = 'convolu.png'
numbra = 'umbral.png'
nnorma = 'normalizacion.png'


min = 110.0 ##parametro definido
max = 190.0 ##parametro definido

matriz = ([0,0,0],[-1,0,0],[0,0,0])

def cargar(imagen):
  im = Image.open(imagen)
	ancho, altura = im.size
	pixels = im.load()
	return ancho,altura,pixels,im

def sies(visitados,ancho,altura):
	for i in range(ancho):
        	for j in range(altura):
                	if visitados[j][i] == 0:
                                return j,i
	return 0,0
def bordes(imagen):
	#colores = ([130,130,130],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255],[250,0,0]) ##colores
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
				
                                cola.append((a,b+1))
                except:
			pass
		try:
                        if pixels[b,a-1][0] == pixels[b,a][0] and visitados[a][b-1] == 0:
                                cola.append((a,b-1))
		except:
                        pass
                try:
                        if pixels[b+1,a][0] == pixels[b,a][0] and visitados[a+1][b] == 0:
                                cola.append((a+1,b))

                except:
                        pass
                try:
                        if pixels[b-1,a][0] == pixels[b,a][0] and visitados[a-1][b] == 0:
				cola.append((a-1,b))
                except:
			pass
		r =colores[contcolor][0]
		g =colores[contcolor][1]
		h =colores[contcolor][2]
		pixels[b,a] = (r,g,h)
		if len(cola) == 0:
			j,i = sies(visitados,ancho,altura)
                        if i==0 and j ==0:
                                break
                        else:
                                cola.append((j,i))
                                contcolor = contcolor + 1
                                if contcolor == 7:
                                        contcolor = 1
	
	im.save(pin)
	return pin
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

	return nfiltro

def gvotos(frecs, ancho,altura):
	frec = list()
	for valor in histo:
		if valor is None:
			continue
		frecuencia = frecs[valor]
		acepta = False
		if len(frec) <= cantidad:
			acepta = True
		if not acepta:
			for (v, f) in frec:
				if frecuencia > f:
					acepta = True
					break
		if acepta:
			frec.append((valor, frecuencia))
			frec = sorted(frec, key = lambda tupla: tupla[1])
			if len(frec) > cantidad:
				frec.pop(0)
	incluidos = list()
	for (valor, frecuencia) in frec:
		incluidos.append(valor)
	return incluidos

def aplica_circulos(mayor,rmin):
	cola = []
        ancho,altura,pixels,im = cargar(nconvolucion)
	cont = 0
	aceptado = 0
	mod = []
        for k in range(len(mayor)):
		x = mayor[k][1]
		y = mayor[k][0]
		aceptado = 0
		for c in range(-rmin,rmin):
			if not y == rmin:
				if x+c >0 and x+c < ancho-1 and y+c >0 and y+c< altura-1:
					if pixels[x+c,y][1] == 255 or pixels[x,y+c][1]==255:
						cont = cont + 1
					if cont > 5:
						aceptado = 1
						print "valor de x aceptado: ",x
						print "valor de y acpetado: ",y
						mod.append((y,x))
	return aceptado,mod
		
	

def sinradio(rmin,rmax,gx,gy,mxy):
	print "Buscando radios"
	r = []
	maxa = 0
	rmaxa = 0
	ancho,altura,pixels,im = cargar(nconvolucion)
	ancho1,altura1,pixels1,im1 = cargar(ngrises)
	while rmin <= rmax:
		frecuencias,cord,mayor = circulos(gx,gy,rmin)
		if mayor > maxa:
			maxa = mayor
			print "mayor",rmin
			if len(cord) > 0:
				print "pasado"
				aceptado,mod = aplica_circulos(cord,rmin)
				if aceptado == 1:
					#print "radio aceptado: ",rmin
					for xx in range(len(mod)-1):
						 for angulo in range(360):
							 x = mod[xx][1] + rmin*cos(angulo)
							 y = mod[xx][0] + rmin*sin(angulo)
							 if x > 0 and y > 0 and  y < altura -1 and  x < ancho -1:
								 pixels1[x,y] = (0,0,255)    
		rmin = rmin + 1
	im1.save(ngrises)	
	
 	return ngrises
def gvotos(votos,ancho,altura):
	dim = int(ancho*altura)
	for rango in range (1,2):
		agregado = True
		while agregado:
			agregado = False
			for y in range(altura):
				for x in range(ancho):
					v = votos[y][x]
					if v > 0:
						for dy in xrange(-rango, rango):
							for dx in xrange(-rango, rango):
								if not (dx == 0 and dy == 0):
									if y + dy > 0 and y + dy < altura and x + dx > 0 and x + dx < ancho:
										w = votos[y + dy][x + dx]
										if w > 0:
											if v - rango >= w:
												votos[y][x] = v + w 
												votos[y + dy][x + dx] = 0
												agregado = True
		
	return votos

def circulos(gx,gy,radio):
	tiempo = time.time()
	CERO = 0.0001 ##para comparaciones de los angulos
        magnitud = [] ##guardamos el gradiente              
        angulos = [] ##guaramos angulos              
        rhos = [] ##guardamos rho                           
        ancho,altura,pixels,im = cargar(ngrises)                             
               
        angulo = 0.0 ##iniciamos rho como cero inicia  
        
        ancho2,altura2,pixels2,im2 = cargar(nconvolucion) ##ca
	
	cose = 0
	sen = 0
	votos = list()
	
	for x in range(altura):
		votos.append([])
		for y in range(ancho):
			votos[x].append(int(0))			
			
        for y in range(altura):
                rhos.append([])                                  
                angulos.append([])##                                
                magnitud.append([])##agre
		votos.append([])
		
                for x in range(ancho):
		#	ym = y - ancho/2
			if x > 0 and y > 0 and  y < altura -1 and  x < ancho -1:
				if pixels2[x,y][1] == 255:
					hor = gx[y][x] ##dat                       
					ver = gy[y][x] ##dato de             
					
					g = math.sqrt(hor ** 2 + ver ** 2)
					if fabs(g) > 0.0:
						
						#angulo = atan(ver/hor)
						cose = hor / g
						sen = ver / g
						xc = int(round(x -radio*cose))
						yc = int(round(y -radio*sen))
					
						
						xcm = xc + ancho/2
						ycm = altura/2 - yc
						
					
						if xcm > 0 and xcm < ancho -1 and ycm > 0 and ycm < altura:
							votos[ycm][xcm] += 1
							pixels[xcm,ycm] = (0,255,0) 
						
	votos = gvotos(votos,ancho,altura)						
	maximo = 0
	suma = 0.0
	#print "sumando"
	for x in range(altura):
		for y in range(ancho):
			v = votos[x][y]
			suma += v
			if v > maximo:
				maximo = v
                 
	promedio = suma / (ancho * altura)
	umbral = (promedio+maximo)/2.0
	#umbral = maximo-promedio
	
	puntosx = []
	puntosy = []
	mayor = 0
	cord = []
	mayorx = 0
	mayory = 0
	
	for x in range(altura):
		for y in range(ancho):
			v = votos[x][y]
			if v > umbral:
		
				if v > mayor:
					mayory = y 
					mayorx = x
					mayor = v
					cord.append((mayorx,mayory))
					
	return	votos,cord,mayor		
	       		

### bfs metodo
def busca(visitados,ancho,altura):
	for y in range(altura):
		for x in range(ancho):
			if visitados[y][x] == 0:
				return y,x
	return 0,0		


def bfs(j,i):
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
					#if pixels[x+j,y+i] == (0,0,0):
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
	
## convolucion
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
	
	return nconvolucion

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
	
	return numbra
##funcio para la diferenciacion entre la original y la imagen filtrada

def normalizacion(imagen,d):
	print "inicia normalizacion"
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
	print "terminino normalizacion"	
	print "Binarizacion"
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
	
	return nimagen


def buscar(lista, elemento):
	for i in range(len(lista)):
		if lista[i] == elemento:
			return 1,i
	return 0,0	


def comprobacion(imagen,gx,gy):
	ancho,altura,pixels,im = cargar(imagen)
	pro = []
	pro.append((0,0))
	visitados = []
	pintar = []
	#visitados = []
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
			y,x =buscar(visitados,ancho,altura)
			
			cont = 0
			cord = []
			if x == 0 and y == 0:
				cosa = 1
			else:
				pro.append((x,y))
				a,b,c = random.randint(1, 255),random.randint(1, 255),random.randint(1, 255)
		

				
	#im.save("bfs.png")
	#return pygame.image.load(imagen)
	return imagen



##funcion principla del programa
def main(nombreI):
	
	ancho,altura,pixels,im = cargar(nombreI)
	
	imagen = escala(nombreI) ##hace llamar a la funcion de escala y garda el resultado
	imagen = filtro(ngrises)
	imagen,gx,gy,mxy = convolucion(nfiltro)
	imagen = normalizacion(nconvolucion,mxy)
	imagen = comprobacion(nconvolucion,gx,gy)
	imagen = circulos(gx,gy,45)
	
	imagen = mumbra(nombreI) ##llama al metodo umbral
		 
main(Inombre) 
