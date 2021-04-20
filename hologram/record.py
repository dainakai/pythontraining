import numpy as np
import cv2 

HEIGHT = 512
WIDTH = 512
WAVE_LEN = 0.6328
DX = 10.0
POSI_X1 = 2560.0
POSI_Y1 = 2560.0
POSI_X2 = 2470.0
POSI_Y2 = 2470.0
POSI_Z1 = 10000.0
POSI_Z2 = 7000.0
DIAM = 80.0
PEAK_BRIGHT1 = 63
PEAK_BRIGHT2 = 127

def trans_func(posi_z):
    z = np.full([HEIGHT,WIDTH],0.+0.j)
    for i in range(HEIGHT):
        for k in range(WIDTH):
            tmp = 2.0j*np.pi*posi_z/WAVE_LEN*np.sqrt(1.0-((k - WIDTH/2)*WAVE_LEN/WIDTH/DX)**2 -((i - HEIGHT/2)*WAVE_LEN/HEIGHT/DX)**2 )
            z[i,k] = np.exp(tmp)
    return z

def object (posi_x,posi_y):
    z = np.full([HEIGHT,WIDTH],0.+0.j)
    for i in range(HEIGHT):
        for k in range(WIDTH):
            if (i*DX-posi_y)**2 + (k*DX-posi_x)**2 > (DIAM/2)**2 :
                z[i,k] = 1.0+0.j
    return z

trans1 = trans_func(POSI_Z1)

object1 = object(POSI_X1,POSI_Y1)
object2 = object(POSI_X2,POSI_Y2)

object1fft = np.fft.fft2(object1)
object1fft = np.fft.fftshift(object1fft)

object2fft = np.fft.fft2(object2)
object2fft = np.fft.fftshift(object2fft)

hologram1 = (object1fft + object2fft)*trans1
hologram1 = np.fft.fftshift(hologram1)
hologram1 = np.fft.ifft2(hologram1)
rehologram1 = PEAK_BRIGHT1* np.abs(hologram1)
cv2.imwrite("1.bmp",rehologram1)

trans2 = trans_func(POSI_Z1-POSI_Z2)
trans3 = trans_func(POSI_Z2)

wave_at_1 = object1fft*trans2
wave_at_1 = np.fft.fftshift(wave_at_1)
wave_at_1 = np.fft.ifft2(wave_at_1)
wave_at_2 = wave_at_1*object2
wave_at_2 = np.fft.fft2(wave_at_2)
wave_at_2 = np.fft.fftshift(wave_at_2)

hologram2 = wave_at_2*trans3

hologram2 = np.fft.fftshift(hologram2)
hologram2 = np.fft.ifft2(hologram2)

rehologram2 = PEAK_BRIGHT2* np.abs(hologram2)

cv2.imwrite("2.bmp",rehologram2)

