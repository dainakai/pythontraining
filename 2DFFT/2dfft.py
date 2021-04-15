import math
import cmath
import sys
import numpy as np

REF_IMAGE_PATH = "./512.bmp"
IMAGE_PATH = "./testimage.bmp"
HOLOGRAM_PATH = "./testhologram.bmp"
HEIGHT = 512
WIDTH = 512
DX = 10.0
DIAM = 80.0
POSI_X = 2560.0
POSI_Y = 2560.0
POSI_Z = 10000.0
WAVE_LEN = 0.6328
PEAK_BRIGHT = 127


def twoDimFFT(z, height, width, flag):
    if flag !=1 and flag !=-1 :
        print("flag of FFT must be either 1 or -1. Software quitting...")
        sys.exit()

    tmpary = np.full([height,width],0.+0.j)

    if flag == -1:
        for i in range(height//2):
            for j in range(width//2):
                tmpary[i][j] = z[i + height//2][j + width//2]
                z[i + height//2][j + width//2] = z[i][j]
                z[i][j] = tmpary[i][j]
        
        for i in range(height//2, height):
            for j in range(width//2):
                tmpary[i][j] = z[i - height//2][j + width//2]
                z[i - height//2][j + width//2] = z[i][j]
                z[i][j] = tmpary[i][j]

    tmp = np.full(max(height,width),0.+0.j)
    for i in range(height):
        for j in range(width):
            tmp[j] = z[i][j]
        if flag == 1:
            tmp = np.fft.fft(tmp)
        elif flag == -1:
            tmp = np.fft.ifft(tmp)
        for j in range(width):
            z[i][j] = tmp[j]

    for i in range(width):
        for j in range(height):
            tmp[j] = z[j][i]
        if flag == 1:
            tmp = np.fft.fft(tmp)
        elif flag == -1:
            tmp = np.fft.ifft(tmp)
        for j in range(height):
            z[j][i] = tmp[j]

    if flag == 1:
        for i in range(int(height/2)):
            for j in range(int(width/2)):
                tmpary[i][j] = z[i + int(height/2)][j + int(width/2)]
                z[i + height//2][j + width//2] = z[i][j]
                z[i][j] = tmpary[i][j]
        
        for i in range(int(height//2), height):
            for j in range(width//2):
                tmpary[i][j] = z[i - height//2][j + width//2]
                z[i - height//2][j + width//2] = z[i][j]
                z[i][j] = tmpary[i][j]

    return z


with open(REF_IMAGE_PATH,"rb") as f:
    header = f.read(1078)
    data = f.read(WIDTH*HEIGHT)

object = np.full([HEIGHT,WIDTH], 0. + 0.j)
trans = np.full([HEIGHT,WIDTH], 0. + 0.j)
hologram = np.full([HEIGHT,WIDTH], 0. + 0.j)
image = [0]*HEIGHT*WIDTH

const = [0] * 3
const[0] = WAVE_LEN**2/HEIGHT**2/DX**2
const[1] = WAVE_LEN**2/WIDTH**2/DX**2

for i in range(HEIGHT):
    for j in range(WIDTH):
        if (j*DX-POSI_X)**2 + (i*DX-POSI_Y)**2 > (DIAM/2.0)**2 :
            object[i][j] = 1.0 + 0.0j
        image[i*WIDTH + j] = int(PEAK_BRIGHT * object[i][j].real)
        
        tmp = 2.0j*math.pi*POSI_Z/WAVE_LEN*cmath.sqrt(1.0-const[0]*(i-HEIGHT/2)**2 - const[1]*(j-WIDTH/2)**2)
        trans[i][j] = cmath.exp(tmp)


with open(IMAGE_PATH,"wb") as fw:
    fw.write(header)
    fw.write(bytes(image))

object = twoDimFFT(object,HEIGHT,WIDTH,1)

hologram = object*trans

hologram = twoDimFFT(hologram,HEIGHT,WIDTH,-1)

for i in range(HEIGHT):
    for j in range(WIDTH):
        image[i*WIDTH + j] = int(PEAK_BRIGHT*abs(hologram[i][j] + 1))

with open(HOLOGRAM_PATH,"wb") as fw:
    fw.write(header)
    fw.write(bytes(image))