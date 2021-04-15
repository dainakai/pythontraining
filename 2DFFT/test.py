import numpy as np
import matplotlib.pyplot as plt

N = 512
T_LEN = 1.0

volt = np.zeros(N)
time = np.zeros(N)
for i in range(N):
    volt[i] = np.sin(2*np.pi*1*i/N) + np.sin(2*np.pi*3*i/N) + np.sin(2*np.pi*6*i/N)
    time[i] = i*T_LEN/N

plt.plot(time,volt,label = "time series")
plt.legend()
plt.show()

data = np.fft.fft(volt)

freq = np.zeros(N)
for i in range(N):
    freq[i] = i/T_LEN

data = abs(data)**2

plt.plot(freq,data,label = "Frequency")
# plt.xlim(0,10)
plt.legend()
plt.show()








