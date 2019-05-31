#%%
from PIL import Image
import numpy as np

from os import listdir
from os.path import isfile, join
import argparse

#%%
def dhash(image, hash_size = 8):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )
    pixels = np.asarray(image)
    # Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)

#%%
def checkModification(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for idx in range(len(onlyfiles)):
        im = Image.open(join(path, onlyfiles[idx]))
        for idx1 in range(len(onlyfiles) - idx):
            if onlyfiles[idx] != onlyfiles[idx1 + idx]:
                im_modif = Image.open(join(path, onlyfiles[idx1 + idx]))
                #print(hamming_distance(dhash(im), dhash(im_modif)))
                if dhash(im) == dhash(im_modif) or hamming_distance(dhash(im), dhash(im_modif)) < 12:
                    print("{}, {}".format(onlyfiles[idx], onlyfiles[idx + idx1]))

def hamming_distance(chaine1, chaine2):
    return len(list(filter(lambda x : ord(x[0])^ord(x[1]), zip(chaine1, chaine2))))
#%%
def main():
    parser = argparse.ArgumentParser(description='Test task for image similarity')
    parser.add_argument("--path", help='folder with images', required=True)
    args = parser.parse_args()
    if args.path:
        checkModification(args.path)


#%%
if __name__ == "__main__":
    main()