from Tkinter import *
from PIL import Image, ImageTk
import math
import sys


def convolucion(imagen_original,mascara):
    
    x, y = imagen_original.size
    pos = imagen_original.load()
    nueva_imagen = Image.new("RGB", (x,y))
    pos_nueva = nueva_imagen.load() 
    for i in range(x):
        for j in range(y):
            total = 0
            for n in range(i-1, i+2):
                for m in range(j-1, j+2):
                    if n >= 0 and m >= 0 and n < x and m < y:
                        total += mascara[n - (i - 1)][ m - (j - 1)] * pos[n, m][1]
            pos_nueva[i, j] = (total, total, total)
    nueva_imagen.save("convolucion.png")
    return nueva_imagen
        

#def mascaras():
 #   matri_x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  #  matri_x = numpy.array(matri_x, dtype = numpy.int8)
   # h= [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
   # h = numpy.array(h, dtype = numpy.int8)
   # matrix_out = numpy.zeros((3, 3,), dtype = numpy.int8)

def otro_gris(imagen_original):
    #escala de grises
    #toma el valor maximo del rgb de cada pixel
    
    x, y = imagen_original.size
    imagen_gris = Image.new("RGB", (x,y))
    pixeles = []

    for a in range(y):
        for b in range(x):
            r, g, b = imagen_original.getpixel((b, a))
            rgb = (r, g, b)
                #se elige el valor mas grande
            maximo = max(rgb)
            data = (maximo, maximo, maximo)
            pixeles.append(data)
    imagen_gris.putdata(pixeles)
    imagen_gris.save("imagen_gris.png")
    return imagen_gris

def normalizar(imagen_original):
    x, y = imagen_original.size
    imagen_normalizada = Image.new("RGB", (x, y))
    pixeles = []
    for a in range(y):
        for b in range(x):
            pix = imagen_original.getpixel((b, a))[0]
            pixeles.append(pix)
    maximo = max(pixeles) 
    minimo = min(pixeles)
    print maximo
    print minimo
    l = 256.0/(maximo - minimo)
    pixeles = []
    for a in range(y):
        for b in range(x):
            pix = imagen_original.getpixel((b, a))[0]
            nuevo_pix = int(math.floor((pix-minimo)*l))
            pixeles.append((nuevo_pix, nuevo_pix, nuevo_pix))
    imagen_normalizada.putdata(pixeles)
    imagen_normalizada.save("imagen_normalizada.png")
    return imagen_normalizada  	


def main():
    """funcion principal
    """
    try:
    	imagen_inicial = sys.argv[1]
    	print imagen_inicial
    	imagen_original = Image.open(imagen_inicial)
    	imagen_original = imagen_original.convert('RGB')
    except:
        print "selecciona la imagen"
    	return
    imagen_b = otro_gris(imagen_original)
    nueva = normalizar(imagen_b)
    mascara1 = [[-1,0,1],[-2,0,2],[-1,0,1]]#mascara sobel horizontal
    mascara2 = [[1,1,1],[0,0,0],[-1,-1,-1]]#mascara sobel vertical
    mascara3 = [[1,1,1],[-1,-2,1],[-1,-1,1]]#mascara prewitt h
    mascara4 = [[-1,1,1],[-1,-2,1],[-1,1,1]]#mascara prewitt v
    #mascara5 = [[0, 1], [-1, 0]]#roberts hor
    #mascara6 = [[1, 0], [0, -1]]#roberts ver
    nueva = convolucion(nueva, mascara1)#aplica convolucion
    nueva.save("sobelh.png")
    nueva = convolucion(nueva, mascara2) #aplica convolucion
    nueva.save("sobelv.png")
    nueva = convolucion(nueva, mascara3) #aplica convolucion
    nueva.save("prewith.png")
    nueva = convolucion(nueva, mascara4) #aplica convolucion
    nueva.save("prewitv.png")
    #nueva = convolucion(nueva, mascara5) #aplica convolucion #no aplicado
    #nueva.save("roberth.png")
    #nueva = convolucion(nueva, mascara6) #aplica convolucion #no aplicado
    #nueva.save("robertv.png")
if __name__ == "__main__":
    main()
