import numpy as np
import cv2

data = cv2.imread("1.bmp",0)
data = np.fft.fft2(data)
data = np.fft.fftshift(data)
data2 = np.abs(data)
data2 = np.log(data2+1)
data2 = 255*(data2 - np.min(data2))/(np.max(data2) - np.min(data2))
cv2.imwrite("1FFT.bmp",data2)

data = cv2.imread("2.bmp",0)
data = np.fft.fft2(data)
data = np.fft.fftshift(data)
data2 = np.abs(data)
data2 = np.log(data2+1)
data2 = 255*(data2 - np.min(data2))/(np.max(data2) - np.min(data2))
cv2.imwrite("2FFT.bmp",data2)