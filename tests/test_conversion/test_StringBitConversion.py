from stegano.stegano import convertToBit, addList, getImage, addList, writeImage, steganoTo, getStegano, decodeBitString
from functools import reduce
from PIL import Image
import re

def test_convertion():
    assert convertToBit('ab') == '0110000101100010'

def test_getImage():
    assert len(getImage('image/Mona_Lisa.jpg', 4)) >= 4 and len(getImage('image/Mona_Lisa.jpg', 4)) <= 6

# Validate there is not RGB value at 255
def test_getImage2():
    assert reduce(lambda x, y: x and y < 255, getImage('image/Mona_Lisa.jpg', True))

# All list should be equal
def test_addList():
    assert len(addList([1], [2])) == len([1]) == len([2])

# Element of the lists (at the same index) should be added together
def test_addList2():
    assert addList([1], [2])[0] == [1][0] + [2][0]

def test_writeImage():
    writeImage('image/Mona_Lisa.jpg', 'image/Mona_Lisa_test.png', [0,1,2,253,254,255])
    img = Image.open('image/Mona_Lisa_test.png')
    assert img.getpixel((0,0)) == (0,1,2)
    assert img.getpixel((1,0)) == (253,254,255)

# The result should be a string made of zeroes and ones
def test_getStegano():
    steganoTo('A', 'image/Mona_Lisa.jpg', 'image/Mona_Lisa_stegano.png')
    pattern = re.compile(r'[^0-1]')
    assert re.findall(pattern, getStegano('image/Mona_Lisa.jpg', 'image/Mona_Lisa_stegano.png')) == []

def test_decode():
    # A binary string multiple of 8 is entirely decoded
    assert decodeBitString('0110000101100010') == 'ab'

def test_decode2():
    # A binary string not multiple of 8 is decoded until the last full byte, last incomplete byte is not decoded
    assert decodeBitString('011000010110001') == 'a'
