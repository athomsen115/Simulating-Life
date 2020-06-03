import sys, random, math
import numpy as np
from PIL import Image

grayScale70 = "$@B%8&WM#*oahkbdpqwmZO0OLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`''. "

grayScale10 = "@%#*+=-:. "

def getAverageLuminesence(image):
    img = np.asarray(image)
    w, h = img.shape
    avg = np.average(img.reshape(w*h))
    return avg

def convertImagetoAscii(fileName, cols, scale, moreLevels, invert):
    image = Image.open(fileName).convert("L")
    WIDTH, HEIGHT = image.size[0], image.size[1]
    width = WIDTH/cols
    height = width/scale 
    rows = int(HEIGHT/height)
    
    print("Columns: {}, Rows: {}".format(cols, rows))
    print("Tile Dimensions: {} x {}".format(width, height))
    
    if cols > WIDTH or rows > HEIGHT:
        print("[ERROR] Image too small for specified columns!")
        
    asciiImage = []
    for i in range(rows):
        y1 = int(i*height)
        y2 = int((i+1)*height)
        if i == rows - 1:
            y2 = HEIGHT
        asciiImage.append("")
        for j in range(cols):
            x1 = int(j*width)
            x2 = int((j+1)*width)
            if j == cols - 1: 
                x2 = WIDTH
            img = image.crop((x1, y1, x2, y2))
            if invert:
                avg = int(255 - getAverageLuminesence(img))
            avg = int(getAverageLuminesence(img))
            
            if moreLevels:
                gsval = grayScale70[int((avg*69)/255)]
            else:
                gsval = grayScale10[int((avg*9)/255)]
            asciiImage[i] += gsval
    
    return asciiImage

def main():
    name = input("Enter the name of the image file to be converted: ")
    outFile = 'ascii.txt'
    scale = 0.5
    cols = 80
    moreLevels = True
    invert = False
    
    print("Generating ASCII Art...")
    asciiArt = convertImagetoAscii(name, cols, scale, moreLevels, invert)
    
    f = open(outFile, 'w')
    for row in asciiArt:
        f.write(row + '\n')
    f.close()
    print("ASCII Art written to {}".format(outFile))
    
if __name__ == '__main__':
    main()

    