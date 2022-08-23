import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft

ADC_BITS =12
SIM_TIME = 0.1
OUT_FREQ = 2.7E3
DAC_FREQ = 5.4E4
SAMPLING_FREQ = 5.4E5
NYQUIST_FREQ = SAMPLING_FREQ / 2
SAMPLES = int(SAMPLING_FREQ * SIM_TIME)
assert SIM_TIME // SAMPLES == 0

def dac_out(f_dac, f_out, t):
    assert f_dac % f_out == 0
    n = int(f_dac // f_out)
    angles = np.linspace(0, np.pi*2, n)
    sintab = (np.sin(angles) * (2**ADC_BITS)).astype(int)
    sintab = sintab.astype(float) / (2**ADC_BITS)
    dac_timestep = np.floor(t * f_dac)
    idx = (np.remainder(dac_timestep, n)).astype(int)
    return sintab[idx]

t = np.linspace(0, SIM_TIME, SAMPLES)
a = dac_out(DAC_FREQ, OUT_FREQ, t)
f = np.linspace(0, NYQUIST_FREQ, SAMPLES//2)
wa = np.abs(fft(a))[0: SAMPLES//2]
wa = wa / np.max(wa)

plt.title('Amplitude vs time')
plt.ylabel('Amplitude')
plt.xlabel('Time [sec]')
plt.plot(t, a)
plt.show()

plt.title('Amplitude vs frequency')
plt.ylabel('Amplitude')
plt.xlabel('Frequency')
plt.plot(f, wa)
plt.show()
print("ds")
