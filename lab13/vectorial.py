import Image
import sys
import numpy
from sys import argv
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata
import numpy as np

NUMBER = 0

def readGif(filename):
    # This metod was taken of...
    # https://code.google.com/p/python-learning-tools/source/browse/trunk/images2gif.py
  
    #Read images from an animated GIF file.  Returns a list of numpy 
    #arrays, or, if asNumpy is false, a list if PIL images.
    
    
    # Load file using PIL
    pilIm = Image.open(filename)   
    pilIm.seek(0)
    
    # Read all images inside
    images = []
    try:
        while True:
            # Get image as numpy array
            tmp = pilIm.convert() # Make without palette
            a = numpy.asarray(tmp)
            if len(a.shape)==0:
                raise MemoryError("Too little memory to convert PIL image to array")
            # Store, and next
            images.append(tmp)
            pilIm.seek(pilIm.tell()+1)
    except EOFError:
        pass
    
    # Done
    return images


def diferencia(ima, ima2):

    umbral = int(argv[2]) 
    
    global NUMBER

    w = ima.size[0] 
    h = ima.size[1]

    pix = ima.load() 
    pix2 = ima2.load() 

    # create a new image that will be the difference of both pixeles. tomado del ejemplo
    
    newImage = Image.new('RGB', (w,h))
    newPix = newImage.load()
    
    for y in range(h):
        for x in range(w):
            if(pix2[x,y][0] - pix[x,y][0]) > umbral:
                newPix[x,y] = (255,0,0) # 
            else:
                newPix[x,y] = pix[x,y] # 

    newImage.save(str(NUMBER+1)+'.png') # 
    NUMBER += 1
    return newImage


def detectMotion(images):
    print 'Diferencia de pixeles'
 
    motionPixels = list()
    #print motionPixels
    for i in range(len(images)-1):
        
  newImage = diferencia(images[i], images[i+1])
        motionPixels.append(newImage)
    
    return motionPixels

def main():
    #(folder1)= Directory.createDirectory()
    nombreGif = sys.argv[1]
    images = readGif(nombreGif)
    
    # play with scanned images
    motionPixels = detectMotion(images)

if __name__ == "__main__":
    main()

