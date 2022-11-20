from PIL import Image
import re

# execute tests: py -m pytest tests

"""
Algo to code
Read a msg
Convert to binary string
Read an image
Convert part of image to RBG value: we need only number of pixels = len(binary string)
Add binary string to RGB string
Write modified RGB value to image

Decode msg: Create binary string from originalImage and encodedImage
Convert binary string to msg
"""

def convertToBit(msg):
    return ''.join(map(lambda x: bin(ord(x))[2:].zfill(8), msg))

# Return list of numbers from image pixels RGB for the required length
def getImage(image, bitStringLength):
    img = Image.open(image)
    rgbList = []
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            rgbList += list(img.getpixel((x,y)))
            if len(rgbList) > bitStringLength: break
        if len(rgbList) > bitStringLength: break
    return rgbList  #[:bitStringLength]

# Add respectively elements of binaryString to colorList and return the result
# colorList=[int1, int2,...] 
# binaryString = '1010...'
# result=[int1+1, int2+0,...]
def addList(colorList, binaryString):
    addedList = []
    for i in range(len(colorList)):
        addedList += [colorList[i] + (int(binaryString[i]) if i < len(binaryString) else 0)]
    return addedList

# Get original image
# Apply stegano to image and write as steganoImage
def writeImage(originalImage, steganoImage, rgbString):
    img = Image.open(originalImage)
    i = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel = img.getpixel((x, y))
            img.putpixel((x,y), (rgbString[i], rgbString[i+1], rgbString[i+2]))
            i += 3
            if i+2 > len(rgbString): break     
        if i+2 >= len(rgbString): break
    img.save(steganoImage)

def getStegano(originalImage, steganoImage):
    oimg = Image.open(originalImage)
    simg = Image.open(steganoImage)

    binaryString = ''
    i = 0
    for y in range(oimg.size[1]):
        for x in range(oimg.size[0]):
            opixel, spixel = oimg.getpixel((x, y)), simg.getpixel((x, y))
            binaryString += str(spixel[0] - opixel[0]) + str(spixel[1] - opixel[1]) + str(spixel[2] - opixel[2])
            if binaryString[len(binaryString)-9:len(binaryString)] == '000000000': break
        if binaryString[len(binaryString)-9:len(binaryString)] == '000000000': break

    return binaryString
    #return binaryString resulting from differences identified between the 2 images

def decodeBitString(bitString):
    pattern = re.compile(r'[01]{8}')
    # print(reduce(lambda x, y: x + chr(int(y,2)), re.findall(pattern, bitString), ''))
    return ''.join(map( lambda x: chr(int(x,2)), re.findall(pattern, bitString)))

def steganoTo(message, originalImage, steganoImage):
    msg = message  # input('Enter message to stegano:')
    binaryString = convertToBit(msg)
    rgbString = getImage(originalImage, len(binaryString))
    rgbString = addList(rgbString, binaryString)
    writeImage(originalImage, steganoImage, rgbString)
    print(f'"{message}" encoded to inage {steganoImage}')

steganoTo('Message à encoder', 'image/Mona_Lisa.jpg', 'image/Mona_Lisa_stegano.png')
print(f"Retrieved encoded message: {decodeBitString(getStegano('image/Mona_Lisa.jpg', 'image/Mona_Lisa_stegano.png'))}")