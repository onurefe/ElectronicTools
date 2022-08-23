import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft

SIM_TIME = 0.1
OUTPUT_FREQ = 32e3
TIM_FREQ = 64e6
UPDATE_FREQ = 512e3
NYQUIST_FREQ = TIM_FREQ / 2
SAMPLES = int(TIM_FREQ * SIM_TIME)
AMPLITUDE = 3.3

assert SIM_TIME // SAMPLES == 0


def pwm_out(f_update, f_out, t):
    t_update = 1.0 / f_update
    triangular_wave = (t % t_update) / t_update
    sine_wave = (1 + np.sin(2 * np.pi * f_out * t)) / 2
    return triangular_wave < sine_wave


t = np.linspace(0, SIM_TIME, SAMPLES, endpoint=False)
out = pwm_out(UPDATE_FREQ, OUTPUT_FREQ, t)
f = np.linspace(0, NYQUIST_FREQ, SAMPLES // 2)
wout = np.abs(fft(out))[0 : SAMPLES // 2]
wout = wout / np.max(wout)

plt.title("Amplitude vs time")
plt.ylabel("Amplitude")
plt.xlabel("Time [sec]")
plt.plot(t, out)
plt.show()

plt.title("Amplitude vs frequency")
plt.ylabel("Amplitude")
plt.xlabel("Frequency")
plt.plot(f, wout)
plt.show()
print("ds")
