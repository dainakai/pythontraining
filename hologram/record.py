import numpy as np
import cv2 

HEIGHT = 512
WIDTH = 512
WAVE_LEN = 0.6328
DX = 10.0
POSI_X1 = 2560.0
POSI_Y1 = 2560.0
POSI_X2 = 2500.0
POSI_Y2 = 2500.0
POSI_Z1 = 10000.0
POSI_Z2 = 10000.0
POSI_Z3 = 7000.0
DIAM = 80.0
PEAK_BRIGHT1 = 63
PEAK_BRIGHT2 = 127

def trans_func(posi_x, posi_y, posi_z):
    z = np.full([HEIGHT,WIDTH],0.+0.j)
    for i in range(HEIGHT):
        for k in range(WIDTH):
            tmp = 2.0j*np.pi*posi_z/WAVE_LEN*np.sqrt(1.0-((k - posi_x/DX)*WAVE_LEN/WIDTH/DX)**2 -((i - posi_y/DX)*WAVE_LEN/HEIGHT/DX)**2 )
            z[i,k] = np.exp(tmp)
    return z

def object (posi_x,posi_y):
    z = np.full([HEIGHT,WIDTH],0.+0.j)
    for i in range(HEIGHT):
        for k in range(WIDTH):
            if (i*DX-posi_y)**2 + (k*DX-posi_x)**2 > (DIAM/2)**2 :
                z[i,k] = 1.0+0.j
    return z

trans1 = trans_func(POSI_X1,POSI_Y1,POSI_Z1)
trans2 = trans_func(POSI_X2,POSI_Y2,POSI_Z2)
trans3 = trans_func(POSI_X2,POSI_Y2,POSI_Z3)

object1 = object(POSI_X1,POSI_Y1)
object2 = object(POSI_X2,POSI_Y2)

object1 = np.fft.fft2(object1)
object2 = np.fft.fft2(object2)
object1 = np.fft.fftshift(object1)
object2 = np.fft.fftshift(object2)

hologram1 = object1*trans1 + object2*trans2
hologram2 = object1*trans1 + object2*trans3

hologram1 = np.fft.fftshift(hologram1)
hologram1 = np.fft.ifft2(hologram1)
hologram2 = np.fft.fftshift(hologram2)
hologram2 = np.fft.ifft2(hologram2)


rehologram1 = PEAK_BRIGHT1* np.abs(hologram1)
rehologram2 = PEAK_BRIGHT2* np.abs(hologram2)

cv2.imwrite("1.bmp",rehologram1)
cv2.imwrite("2.bmp",rehologram2)

