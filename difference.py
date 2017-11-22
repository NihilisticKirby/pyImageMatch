## Python 3.6
## Program to search for an image inside a database
## Authors: Ian Raúl Huerta Gutiérrez & Daniela Abigail Parrales Mejía

from tkinter import *
from skimage.measure import compare_ssim as ssim
from PIL import Image
import numpy as np
import cv2
from timeit import default_timer as timer
import glob
import os
import math

######################################################################################

## Returns the SSIM (Structural Similarity) between two images. Author: Adrian Rosebrock
def compare_images(imageA, imageB):
	# The SSIM computation was developed by Zhou Wang, Member of IEEE
	s = ssim(imageA, imageB)
	return s

## Does the hippy thing
def heapify(keys, data, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2
    # See if left child of root exists and is greater than root
    if l < n and keys[i] < keys[l]:
        largest = l
    # See if right child of root exists and is greater than root
    if r < n and keys[largest] < keys[r]:
        largest = r
    # Change root, if needed
    if largest != i:
        keys[i], keys[largest] = keys[largest], keys[i]  # swap
        data[i], data[largest] = data[largest], data[i]  # swap
        # Heapify the root.
        heapify(keys, data, n, largest)

## Sorts the heap in nondecreasing order
def heapSort(keys, data):
    n = len(keys)
    # Build a maxheap.
    for i in range(n, -1, -1):
        heapify(keys, data, n, i)
    # One by one extract elements
    for i in range(n - 1, 0, -1):
        keys[i], keys[0] = keys[0], keys[i]  # swap
        data[i], data[0] = data[0], data[i]  # swap
        heapify(keys, data, i, 0)

## Returns the original image processed as we found it was best
def getSample(originalName):
	a = originalName
	b = a.split(".")
	name = b[0]
	formatI = b[1]
	if formatI == "gif": # Checks if it is GIF
		files = glob.glob(originalName) 
		for imageFile in files:
			filepath,filename = os.path.split(imageFile)
			filterame,exts = os.path.splitext(filename)
			print("Processing: " + imageFile,filterame)
			im = Image.open(imageFile)
			im.save( name+'.png','PNG')
		original = cv2.imread(name+".png") # First, read the original image
		original = cv2.resize(original, (50, 50)) # Then, resize the image, to save memory
		original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) #Finally, since the image is now small, change to grays
		return original
	original = cv2.imread(originalName) # First, read the original image
	original = cv2.resize(original, (50, 50)) # Then, resize the image, to save memory
	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) #Finally, since the image is now small, change to grays
	return original

## Returns a list with the names of the images in the given path
def readDirectory(pathName):                         
    data = os.listdir(pathName)
    return data

def processImages(data):
	keys = []
	for x in range(0,len(data)-1):
		print(data[x])
		a = data[x]
		b = a.split(".")
		name = b[0]
		formatI = b[1]
		if formatI == "gif": # Checks if it is a GIF
			files = glob.glob(data[x]) 
			for imageFile in files:
				filepath,filename = os.path.split(imageFile)
				filterame,exts = os.path.splitext(filename)
				print("Processing: " + imageFile,filterame)
				im = Image.open(imageFile)
				im.save( 'C:\\Users\\Ian\\Desktop\\pyshit\\testo2\\'+name+'.png','PNG')
				data.append(name + ".png")
				keys.append(0)
		else:
			ima = cv2.imread("C:\\Users\\Ian\\Desktop\\pyshit\\testo2\\"+data[x])
			ima = cv2.resize(ima, (50, 50))
			ima = cv2.cvtColor(ima, cv2.COLOR_BGR2GRAY)
			valor = compare_images(original, ima)
			if valor == 1.0: # If the image is the same, it will return it to save time
				print("\nLa imagen si esta, es: ",data[x])
				print("   con coincidencia del: 100%")
				result = [data[x], "100"]
				return result
			keys.append(valor)
	heapSort(keys, data)
	print("\nLa imagen no esta, pero la mas parecida con: ",math.floor(keys[len(keys)-1]*100),"%","de similitud")
	print("   es la imagen: ",data[len(keys)-1])
	result = [data[len(keys)-1], str(math.floor(keys[len(keys)-1]*100))]
	return result

######################################################################################

thisImage = "C:\\Users\\Ian\\Desktop\\pyshit\\boi.jpg"

################################ For the Console #####################################
start = timer() ## Starts the timer
original = getSample(thisImage) ## Loads the example in memory
data = readDirectory("C:\\Users\\Ian\\Desktop\\pyshit\\testo2") ## Reads a directory
result = processImages(data) ## Proceses the data
end = timer() ## Ends the timer
totalTime = end - start ## Time in seconds
print("Tiempo de ejecucion: ", totalTime,"segundos")


#################################### GUI #############################################
import PIL.Image

b = thisImage.split(".")
name = b[0]
formatI = b[1]
if formatI == "gif": ## Converts GIF images to PNG
	files = glob.glob(thisImage) 
	for imageFile in files:
		filepath,filename = os.path.split(imageFile)
		filterame,exts = os.path.splitext(filename)
		print("Processing: " + imageFile,filterame)
		im = Image.open(imageFile)
		im.save( name+'.png','PNG')
if formatI == "jpg": ## Converts JPG images to PNG
	im = PIL.Image.open(thisImage)
	im.save(name+'.png')

## ADD HERE CONVERTER FOR BMP FILES TO PNG

root = Tk()

leftFrame = Frame(root)
leftFrame.pack(side = LEFT)
rightFrame = Frame(root)
rightFrame.pack(side = RIGHT)
bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)

pic1 = PhotoImage(file = name + ".png")
label1 = Label(leftFrame, image = pic1)
label1.pack()

prueba = result[0]
c = prueba.split(".")
name1 = c[0]
formatI1 = c[1]
if formatI1 == "jpg": ## Converts JPG images to PNG
	im = PIL.Image.open("C:\\Users\\Ian\\Desktop\\pyshit\\testo2\\"+prueba)
	im.save("C:\\Users\\Ian\\Desktop\\pyshit\\testo2\\"+name1+'.png')

pic2 = PhotoImage(file = "C:\\Users\\Ian\\Desktop\\pyshit\\testo2\\"+name1+".png")
label2 = Label(rightFrame, image = pic2)
label2.pack()

rate = Label(bottomFrame, text = "Coincidencia de: "+result[1]+"%")
rate.pack()

root.mainloop()


"""
References:

Article about image comparison: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
Article about image manipulation: https://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/
Article about Structural Similarity: http://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf
Code to convert GIF images to PNG: https://stackoverflow.com/questions/6689380/how-to-change-gif-file-to-png-file-using-python-pil
"""