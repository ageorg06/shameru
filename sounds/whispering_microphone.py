from pyo import *
import time

# Initialize the pyo server
s = Server().boot()
s.start()

# Capture live audio input
mic_input = Input()

# Apply a noise gate for noise reduction
threshold = -40  # Threshold level in dB
risetime = 0.1  # Time taken to go from closed to open, in seconds
falltime = 0.1  # Time taken to go from open to closed, in seconds
gated_input = Gate(mic_input, thresh=threshold, risetime=risetime, falltime=falltime)

# Create Low Frequency Oscillators (LFOs) to modulate the amplitude and center frequency
amp_lfo = Sine(freq=0.2, mul=0.15, add=0.15)  # Slow sine wave LFO for amplitude modulation
freq_lfo = Sine(freq=0.1, mul=200, add=1000)  # Slow sine wave LFO for frequency modulation

# Apply a bandpass filter for equalization
filtered_input = ButBP(gated_input, freq=freq_lfo, q=2)

# Apply amplitude modulation
modulated_input = filtered_input * amp_lfo

# Apply a compressor for dynamic range control
ratio = 4  # Compression ratio
attack = 0.01  # Attack time in seconds
release = 0.1  # Release time in seconds
compressed_input = Compress(modulated_input, thresh=threshold, ratio=ratio, risetime=attack, falltime=release)

# Output the processed sound
compressed_input.out()

# Keep the program running to continue processing the live input
while True:
    time.sleep(0.1)
