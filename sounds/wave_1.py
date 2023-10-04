from pyo import *
import time

# Initialize the pyo server
s = Server().boot()
s.start()

# Create a noise source
noise = PinkNoise(mul=2)

# Create a Low Frequency Oscillator (LFO) to modulate the amplitude of the noise
amp_lfo = Sine(freq=0.1, mul=0.6, add=0.6)  # Slow sine wave LFO for amplitude modulation

# Modulate the amplitude of the noise source with the LFO
modulated_noise = noise * amp_lfo

# Apply a bandpass filter to the modulated noise to create a "wave" sound
center_freq = 150  # Center frequency of the bandpass filter
q = 0.7  # Quality factor of the bandpass filter
wave_sound = ButBP(modulated_noise, freq=center_freq, q=q).out()

# Play the wave sound indefinitely
while True:
    time.sleep(0.1)
