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
        
        tmp = 2.0j*np.pi*POSI_Z/WAVE_LEN*np.sqrt(1.0-const[0]*(i-HEIGHT/2)**2 - const[1]*(j-WIDTH/2)**2)
        trans[i][j] = np.exp(tmp)


with open(IMAGE_PATH,"wb") as fw:
    fw.write(header)
    fw.write(bytes(image))

object = np.fft.fft2(object)
object = np.fft.fftshift(object)

hologram = object*trans

hologram = np.fft.fftshift(hologram)
hologram = np.fft.ifft2(hologram)


for i in range(HEIGHT):
    for j in range(WIDTH):
        image[i*WIDTH + j] = int(PEAK_BRIGHT*abs(hologram[i][j] + 1))

with open(HOLOGRAM_PATH,"wb") as fw:
    fw.write(header)
    fw.write(bytes(image))