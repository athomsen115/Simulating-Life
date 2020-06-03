import sys, os, random, imghdr
from PIL import Image
import numpy as np

def getAverageRGB(image):
    img = np.asarray(image)
    w, h, d = img.shape
    rgb = tuple(np.average(img.reshape(w*h, d), axis=0))
    
    return rgb

def splitImage(image, size):
    WIDTH, HEIGHT = image.size[0], image.size[1]
    row, col = size
    width, height = int(WIDTH/col), int(HEIGHT/row)
    
    images = []
    for i in range(row):
        for j in range(col):
            images.append(image.crop((j*width, i*height, (j+1)*width, (i+1)*height)))
    
    return images

def getImages(imageDir):
    files = os.listdir(imageDir)
    images = []
    for file in files:
        filePath = os.path.abspath(os.path.join(imageDir, file))
        try:
            f = open(filePath, "rb")
            image = Image.open(f)
            images.append(image)
            image.load()
            f.close()
        except:
            print("Invalid Image: {}".format(filePath))
    
    return images

def getImageFilenames(imageDir):
    files = os.listdir(imageDir)
    filenames = []
    for file in files:
        filePath = os.path.abspath(os.path.join(imageDir, file))
        try:
            imgType = imghdr.what(filePath)
            if imgType:
                filenames.append(filePath)
        except:
            print("Invalid Image: {}".format(filePath))
    
    return filenames

def getBestMatchIndex(inputAvg, avgs):
    #currently runs a nearest neighbor search, update to use a kdTree in scipy
    avg = inputAvg
    index = 0
    minIndex = 0
    minDist = float("inf")
    for val in avgs:
        dist = ((val[0] - avg[0])*(val[0] - avg[0]) + (val[1] - avg[1])*(val[1] - avg[1]) + (val[2] - avg[2])*(val[2] - avg[2]))
        if dist < minDist:
            minDist = dist
            minIndex = index
        index += 1
        
    return minIndex

def createImageGrid(images, dims):
    m, n = dims
    #add gaps between photos (adjust the gaps wwhen finding the size)
    assert m*n == len(images)
    width = max([image.size[0] for image in images])
    height = max([image.size[1] for image in images])
    
    gridImage = Image.new('RGB', (n*width, m*height))
    
    for index in range(len(images)):
        row = int(index/n)
        col = index - n*row
        gridImage.paste(images[index], (col*width, row*height))
    
    return gridImage

def createPhotomosaic(targetImage, inputImages, gridSize, reuseImages=True):
    print("Input image splitting into tiles...")
    targetImages = splitImage(targetImage, gridSize)
    
    print("Looking for potential matches...")
    outputImages = []
    count = 0
    batchSize = int(len(targetImages)/10)
    
    avgs = []
    for image in inputImages:
        avgs.append(getAverageRGB(image))
        
    for image in targetImages:
        avg = getAverageRGB(image)
        matchIndex = getBestMatchIndex(avg, avgs)
        outputImages.append(inputImages[matchIndex])
        if count > 0  and batchSize > 10 and count % batchSize is 0:
            print("Processed {} of {}".format(count, len(targetImages)))
        count += 1
        if not reuseImages:
            inputImages.remove(matchIndex)
    
    print("Building the mosaic...")
    mosaicImage = createImageGrid(outputImages, gridSize)
    
    return mosaicImage
    
def main():
    image = input("Please enter the image that will be used to base the photomosaic off of: ")
    inputFolder = input("Please enter the folder name of the source images: ")
    gridSize = input("Please enter the grid size as 2 integers (ex. 128 128): ")
    
    targetImage = Image.open(image)
    print("Processing the image folder...")
    inputImages = getImages(inputFolder)
    
    if inputImages == []:
        print("No input images found in {}. Exiting...".format(inputFolder), file=sys.stderr)
        sys.exit(1)
    
    random.shuffle(inputImages)
    g1, g2 = gridSize.split()
    gridSize = (int(g1), int(g2))
    outFile = 'mosaic.png'
    
    reuseImages = True
    resizeInput = True
    
    print("Starting photomosaic creation...")
    if not reuseImages:
        if gridSize[0]*gridSize[1] > len(inputImages):
            print("Grid size less than the number of images. Exiting...", file=sys.stderr)
            sys.exit(2)
            
    if resizeInput:
        print("Resizing images...")
        dimensions = (int(targetImage.size[0]/gridSize[1]), int(targetImage.size[1]/gridSize[0]))
        print("Max Tile Dimensions: {}".format(dimensions))
        for image in inputImages:
            image.thumbnail(dimensions)
            
    mosaicImage = createPhotomosaic(targetImage, inputImages, gridSize, reuseImages)
    
    mosaicImage.save(outFile, 'PNG')
    
    print("Saved output to {}".format(outFile))
    print("Photomosaic Complete!")

if __name__ == '__main__':
    main()