from pyo import *
import time

# Initialize the pyo server
s = Server().boot()
s.start()

# Create a noise source with lower amplitude for a calmer whispering sound
noise = Noise(mul=0.5)

# Define base formant frequencies for whispering (in Hz)
f1 = 650  # First formant
f2 = 1200  # Second formant
f3 = 2600  # Third formant

# Create LFOs to modulate formant frequencies and amplitude for variability
lfo_freq = Sine(freq=0.2, mul=50, add=1)  # LFO for frequency modulation
lfo_amp = Sine(freq=0.1, mul=0.05, add=0.05)  # LFO for amplitude modulation

# Apply bandpass filters with modulated frequencies to create formant peaks
whisper_f1 = ButBP(noise * lfo_amp, freq=f1 * lfo_freq, q=5).out()
whisper_f2 = ButBP(noise * lfo_amp, freq=f2 * lfo_freq, q=5).out()
whisper_f3 = ButBP(noise * lfo_amp, freq=f3 * lfo_freq, q=5).out()

# Mix the formants to create the final whispering sound
whisper_sound = Mix([whisper_f1, whisper_f2, whisper_f3], voices=1).out()

# Play the whispering sound indefinitely
while True:
    time.sleep(0.1)
