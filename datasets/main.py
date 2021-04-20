import numpy as np
import cv2

HOLOGRAMS_DIR = "./holograms"
PARTICLE_DIR = "./dat"
FFTS_DIR = "./fft"

ITR = 100

HEIGHT =512
WIDTH = 512
DEPTH = 1
DIST = 1000
NUM = 100
DX = 10.0
DZ = 10.0
DIAM = 80.0
WAVE_LEN = 0.6328
PEAK_BRIGHT = 127

def trans_func(posi_z):
    z = np.full([HEIGHT,WIDTH],0.+0.j)
    for i in range(HEIGHT):
        for k in range(WIDTH):
            tmp = 2.0j*np.pi*posi_z/WAVE_LEN*np.sqrt(1.0-((k - WIDTH/2)*WAVE_LEN/WIDTH/DX)**2 -((i - HEIGHT/2)*WAVE_LEN/HEIGHT/DX)**2 )
            z[i,k] = np.exp(tmp)
    return z

for itr in range(ITR):
    index = np.arange(NUM)
    x_cordnt = np.random.randint(0,WIDTH,NUM)
    y_cordnt = np.random.randint(0,HEIGHT,NUM)
    z_cordnt = np.random.randint(0,DEPTH,NUM)

    prtcl_vol = np.full([DEPTH,HEIGHT,WIDTH],0.+0.j)
    for n in range(NUM):
        for i in range(DEPTH):
            for j in range(HEIGHT):
                for k in range(WIDTH):
                    if (k - x_cordnt[n])**2 + (j - y_cordnt[n])**2 + (i - z_cordnt[n])**2 < (DIAM/2/DX)**2:
                        prtcl_vol[i,j,k] = 1.0 + 0.j

    prtcl_vol = 1.0 - prtcl_vol

    np.save("./dat/"+str(itr),prtcl_vol)

    trans = trans_func(DZ)
    transdist = trans_func(DIST)
    wave_field = np.full([HEIGHT,WIDTH],1.+0.j)
    for i in range(DEPTH):
        wave_field = wave_field*prtcl_vol[i,:,:]
        wave_field = np.fft.fft2(wave_field)
        wave_field = np.fft.fftshift(wave_field)

        wave_field = wave_field * trans

        wave_field = np.fft.fftshift(wave_field)
        wave_field = np.fft.ifft2(wave_field)

    wave_field = np.fft.fft2(wave_field)
    wave_field = np.fft.fftshift(wave_field)
    wave_field = wave_field * transdist
    wave_field = np.fft.fftshift(wave_field)
    wave_field = np.fft.ifft2(wave_field)

    hologram = PEAK_BRIGHT* np.abs(wave_field)

    intensity = np.fft.fft2(hologram)
    intensity = np.fft.fftshift(intensity)
    intensity = np.abs(intensity)
    intensity = np.log(intensity+1)
    intensity = 255*(intensity - np.min(intensity))/(np.max(intensity) - np.min(intensity))

    char1 = "./holograms/" + str(itr)+".bmp"
    char2 = "./fft/" + str(itr)+".bmp"
    cv2.imwrite(char1,hologram)
    cv2.imwrite(char2,intensity)



