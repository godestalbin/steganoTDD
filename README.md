# Stegano TDD - Exercice for practising test driven development

## What is steganography
Steganography consist in hidding information inside a media.
In this example we aim at hidding a small text inside an image.
We can then retrive the hidden text by comparing the original image wih the one containing the text.

Note that to encode the text in the image we have to use a lossless compressed format such as PNG. This is not the case for JPG.

In our case we use a basic/trivial solution:
* Converrt the text to a binary string
* Add each bit to each RBG color byte of each pixel. Thus one pixel allow to encode 3 bit and we need 2,66 pixels (2 pixels + 2 colors of the 3rd one) to encode one single character.

What are the limitations:
* The hidden text can contain only text from the ASCII table because we assume character are on 8 bits.
* If the image contains colors with value 255, the bits of the text could not be stored correctly: the decoded string will contain errors.

## What is our algorithm ?
### Hide text inside image
* Convert text message to binary string (a string composed of '010101100...')
`convertToBit(msg)` returns the binary string
* Get the list of pixel colors
`getImage(image, bitStringLength)` returns a list of by value (the image pixel colors) (a list composed of byte size digits [45, 23, 78, 34, ...]).
The image is read by line first and then by colomn.
The return list has a length greater or equal to the length of the binary strin.
The return list has a length multiple of 3 (when processing one pixel, we always take the 3 colors).
* Add each value of the binary string to respectively each value of the pixel color list
`addList(colorList, binaryString)` returns the pixel color list update by adding the binary string value.
This is the list of pixel color which includes the hidden message.
With the examples above the result will be [45+0, 23+1, 78+0, 34+1, ...]
* Write a copy of the original image as stegano image with list of new colors provided
`writeImage(originalImage, steganoImage, rgbString)` does not return any value.
* Execute all the steps above
`steganoTo(message, originalImage, steganoImage)` prints a confirmation that message has been hidden in stegano image

### Retrieve text from image
* Get message binary string by comparing stegano image with original image.
`getStegano(originalImage, steganoImage)` return a binary string
* Decode the binary string as text
`decodeBitString(bitString)` return a string with the message

## How to run
* Add required modules: `pip install -r requirements.txt`
* To execute code: `py stegano/stegano.py`
* To execute tests: `py -m pytest -v tests`