from PIL import Image
from sys import argv
from math import floor
import numpy as np

def filtro(imagen_original):
#    se encarga de tomar de cada pixel los pixeles 
#    de izq, derecha, arriba, abajo y el mismo y los promedia, y ese
#    promedio es el valor de los nuevos pixeles
    
    x, y = imagen_original.size
    imagen_difusa = Image.new("RGB", (x, y))
    pixeles = []
    #temp sirve para obtener el promedio de los
    #pixeles contiguos 
    temp = []
    for a in range(y):
        for b in range(x):
            actual = imagen_original.getpixel((b, a))[0]
            if b>0 and b<(x-1) and a>0 and a<(y-1):
                    #en esta condicion entran todos los pixeles que no estan
                    #en el margen de la imagen, es decir casi todos
                pix_izq = imagen_original.getpixel((b-1, a))[0]
                pix_der = imagen_original.getpixel((b+1, a))[0]
                pix_arriba = imagen_original.getpixel((b, a+1))[0]
                pix_abajo = imagen_original.getpixel((b, a-1))[0]
                temp.append(pix_izq)
                temp.append(pix_der)
                temp.append(pix_arriba)
                temp.append(pix_abajo)
            else:
                #aqui entran todos los pixeles de la orilla
                try:
                    pix_abajo = imagen_original.getpixel((b, a-1))[0]
                    temp.append(pix_abajo)
                except:
                    pass
                try:
                    pix_der = imagen_original.getpixel((b+1, a))[0]
                    temp.append(pix_der)
                except:
                    pass
                try:                
                    pix_izq = imagen_original.getpixel((b-1, a))[0]
                    temp.append(pix_izq)
                except:
                    pass
                try:
                    pix_arriba = imagen_original.getpixel((b, a+1))[0]
                    temp.append(pix_arriba)
                except:
                    pass
            temp.append(actual)
                #se obtiene el promedio para cambiar el pixel
            prom = sum(temp)/len(temp)
            temp = []
            pixeles.append((prom, prom, prom))
    imagen_difusa.putdata(pixeles)
    imagen_difusa.save("imagen_difusa.png")
    return imagen_difusa

def aumenta_dism(antes, ((ancho, alto))):
  prom_ancho = (x * 1.0)/ancho
	prom_alto = (y * 1.0)/alto
	
	for a in range(alto):
		for b in range(ancho):
			mueve_x = floor(a * prom_alto)
			mueve_y = floor(b * prom_ancho)
			imagen[a,b] = antes[int(mueve_x),int(mueve_y)] 
	return imagen



def main():

	#im = Image.open("dory.jpg").convert('RGB')
	#(x,y) = im.size
	#print 'Image size:', x,y
	#imagen = np.array(im)
	try:
	    	imagen_inicial = "dory.jpg"
	    	print imagen_inicial
	    	imagen_original = Image.open(imagen_inicial)
	    	imagen_original = imagen_original.convert('RGB')
	except:
        	print "selecciona la imagen"
    		return	
if __name__ == "__main__":
    main()
