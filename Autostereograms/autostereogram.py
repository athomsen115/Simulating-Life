import sys, random
from PIL import Image, ImageDraw

def createTiledImage(tile, dims):
    image = Image.new('RGB', dims)
    WIDTH, HEIGHT = dims
    width, height = tile.size
    cols = int(WIDTH/width) + 1
    rows = int(HEIGHT/height) + 1
    for i in range(rows):
        for j in range(cols):
            image.paste(tile, (j*width, i*height))
    
    return image

def createRandomTile(dims):
    image = Image.new('RGB', dims)
    draw = ImageDraw.Draw(image)
    radius = int(min(*dims)/100)
    numCircles = 1000
    for i in range(numCircles):
        x, y = random.randint(0, dims[0]-radius), random.randint(0, dims[1]-radius)
        fill = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill)
    
    return image

def createAutostereogram(depthMap, tile):
    if depthMap.mode is not 'L':
        depthMap = depthMap.convert('L')
        
    if not tile:
        tile = createRandomTile((100, 100))
        
    image = createTiledImage(tile, depthMap.size)
    shiftedImage = createDepthShiftedImage(depthMap, image)
    
    return shiftedImage

def createSpacingDepthExample():
    tiles = [Image.open('test/a.png'), Image.open('test/b.png'), Image.open('test/c.png')]
    image = Image.new('RGB', (600,400), (0,0,0))
    spacing = [10,20,40]
    for j, tile in enumerate(tiles):
        for i in range(8):
            image.paste(tile, (10 + i*(100 + j*10), 10 + j*100))
    image.save('spacedepth.png')
    
def createDepthMap(dims):
    depthMap = Image.new('L', dims)
    depthMap.paste(10, (200, 25, 300, 125))
    depthMap.paste(30, (200, 150, 300, 250))
    depthMap.paste(20, (200, 275, 300, 375))
    
    return depthMap

def createDepthShiftedImage(depthMap, image, scale=10):
    assert depthMap.size == image.size
    
    shiftedImage = image.copy()
    pixelD = depthMap.load()
    pixelS = shiftedImage.load()
    
    cols, rows = shiftedImage.size
    for i in range(rows):
        for j in range(cols):
            xShift = pixelD[j, i]/scale
            xPos = j - image.size[0] + xShift
            if xPos > 0  and xPos < cols:
                pixelS[j, i] = pixelS[xPos, i]
    
    return shiftedImage
    

def main():
    print("Welcome to the autostereogram generator...")
    print("For the options below, enter your own response, or hit 'enter' to choose the [default]")
    out = input("Enter the name of the output file: [autostereogram.png]")
    if out != '':
        outFile = out
    else:
        outFile = 'autostereogram.png'
        
    tile = input("Provide the name of the tileFile: [None]")
    if tile != '':
        tileFile = Image.open(tile)
    else:
        tileFile = False
    dep = input("Enter the depth image file: [depth/shark-depth.png]")    
    if dep != '':
        depth = dep
    else:
        depth = 'depth/shark-depth.png'
        
    depthImage = Image.open(depth)
    
    scale = input("Adjust the scale that the depth map is adjusted by: [10]")
    if scale != '':
        asImage = createAutostereogram(depthMap, tileFile, scale)
    else:
        asImage = createAutostereogram(depthImage, tileFile)
    asImage.save(outFile)
    
    print("Autosterogram saved at autosterogram.png")
    print("Image complete!")

main()
        