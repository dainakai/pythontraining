import math
import cmath
import sys
import numpy as np
import matplotlib.pyplot as plt

N = 512
T_LEN = 1.0

#complex def
def oneDFFT(z, N, flag):
    rot = [0]*N
    
    nhalf = N/2
    num = N/2
    sc = 2.0*math.pi/N

    while num>=1:
        for j in range(0,N,int(2*num)):
            phi = rot[j]/2
            phi0 = phi + nhalf
            e = cmath.exp(sc*phi*flag)

            for k in range(j,int(j+num)):
                k1 = int(k + num)
                z0 = z[k1]*e
                z[k1] = z[k] - z0
                z[k] += z0
                rot[k] = phi
                rot[k1] = phi0
        
        num /= 2
    
    if flag < 0 :
        for i in range(N):
            z[i] /= float(N)
    
    tmp = 0. + 0.j
    for i in range(N-1):
        if rot[i] > i :
            j = int(rot[i])
            tmp = z[i]
            z[i] = z[j]
            z[j] = tmp

    return z

def oneDFFTsep(ak, bk, N, flag):
    # ak = np.zeros(N)
    # bk = np.zeros(N)
    # ak = re
    # bk = im
    rot = np.zeros(N,dtype="int32")
    nhalf = N//2
    num = N//2
    sc = 2.0*math.pi/N

    while num >= 1 :
        for j in range(0,N,2*num):
            phi = rot[j]//2
            phi0 = phi + nhalf
            c = np.cos(sc*phi)
            s = np.sin(sc*phi*flag)

            for k in range(j,j+num):
                k1 = k + num
                a0 = ak[k1]*c - bk[k1]*s
                b0 = ak[k1]*s + bk[k1]*c
                ak[k1] = ak[k] - a0
                bk[k1] = ak[k] - b0
                ak[k] += a0
                bk[k] += b0
                rot[k] = phi
                rot[k1] = phi0

        num //= 2

    if flag < 0 :
        for i in range(N):
            ak[i] /= N
            bk[i] /= N
    
    for i in range(N-1):
        j = rot[i]
        if j > i:
            # tmp1, tmp2 = re[i], im[i]
            # re[i],im[i] = re[j],im[j]
            # re[j],im[j] = tmp1,tmp2
            tmp = ak[i]
            ak[i] = ak[j]
            ak[j] = tmp
            tmp = bk[i]
            bk[i] = bk[j]
            bk[j] = tmp

    return ak, bk

def oneDDFT(re,im,N):
    re_data = np.zeros(N)
    im_data = np.zeros(N)
    for i in range(N):
        for j in range(N):
            re_data[i] += re[j]*math.cos(2.0*math.pi*i*j/N) + im[j]*math.sin(2.0*math.pi*i*j/N)
            im_data[i] += im[j]*math.cos(2.0*math.pi*i*j/N) - re[j]*math.sin(2.0*math.pi*i*j/N)
    
    return re_data,im_data



volt = np.zeros(N)
time = np.zeros(N)
for i in range(N):
    volt[i] = math.sin(2*math.pi*1*i/N) + math.sin(2*math.pi*3*i/N) + math.sin(2*math.pi*6*i/N)
    time[i] = i*T_LEN/N

plt.plot(time,volt,label = "time series")
plt.legend()
plt.show()

data = np.full(N,0.+0.j)
for i in range(N):
    data[i] = volt[i] + 0.j

data = oneDFFT(data,N,1)

re_data = np.zeros(N)
im_data = np.zeros(N)
re_data = volt

re_data, im_data = oneDFFTsep(re_data,im_data,N,1)

output1 = np.zeros(N)
output1 = abs(volt)**2

freq = np.zeros(N)
for i in range(N):
    freq[i] = i/T_LEN

# freq = np.fft.fftfreq(N)

# re_data = np.fft.fft(volt)

# plt.plot(freq,re_data,label = "Frequency")
# plt.legend()
# plt.show()

output2 = np.zeros(N)
output2 = re_data**2 + im_data**2

plt.plot(freq,output1,label = "Frequency")
# plt.xlim(0,10)
plt.legend()
plt.show()








