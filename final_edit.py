import numpy as np
import cv2
import math
img = cv2.imread('messi.jpg')

height,width,channels = img.shape
print height,width

number_of_slices = 3
width_of_slice = math.floor(width/number_of_slices)

#code to fragment images
for x in range(1,number_of_slices):
    cropped = img[0:height,((x-1)*width_of_slice + 1):x*width_of_slice]
    image_name = 'd'+ str(x) +'.jpg'
    cv2.imwrite(image_name, cropped)

#add the last slice    
cropped = img[0:height,(number_of_slices-1)*width_of_slice:width]
image_name = 'd' + str(number_of_slices) + '.jpg'
cv2.imwrite(image_name, cropped)





#code to encrypt
import os, random, struct
from Crypto.Cipher import AES

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

for x in range(1,number_of_slices+1):
    encrypt_file('1234567890123456', 'd'+str(x)+'.jpg')

#sending encrypted files to servers
import os;
os.rename("d1.jpg.enc","server1/d1.jpg.enc")
os.rename("d2.jpg.enc","server2/d2.jpg.enc")
os.rename("d3.jpg.enc","server3/d3.jpg.enc")
#code to decrypt
import os, random, struct
from Crypto.Cipher import AES

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
for  x in range(1,number_of_slices+1):
    decrypt_file('1234567890123456', 'server'+str(x)+'/d'+str(x)+'.jpg.enc', 'd'+str(x)+'_decrypted.jpg')

#concatenating all the images
output_image = cv2.imread('d1.jpg')
for x in range(2,number_of_slices + 1):
    image_name = 'd'+ str(x) +'_decrypted.jpg';
    img = cv2.imread(image_name)
    output_image = np.concatenate((output_image, img), axis=1)
	
cv2.imwrite('concatenated_output_final.jpg', output_image)

input = ("processes complete,press any key to exit")

