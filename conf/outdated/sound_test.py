import numpy as np
import sounddevice as sd
 
# Parameters
duration = 10  # seconds
sampling_rate = 44100  # typical value for audio
 
# Generate a time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
 
# Create a low-frequency sine wave (for a dark ambient feel)
freq = 55.0  # A low frequency, like 55Hz (A1 note)
sine_wave = 0.5 * np.sin(2 * np.pi * freq * t)
 
# Create some white noise for texture
white_noise = 0.1 * np.random.randn(t.shape[0])
 
# Combine the sine wave and white noise
ambient_sound = sine_wave + white_noise
 
# Normalize the sound to prevent clipping
ambient_sound = ambient_sound / np.max(np.abs(ambient_sound))
 
# Play the sound
sd.play(ambient_sound, samplerate=sampling_rate)
 
# Use this line to block execution until audio is finished playing
sd.wait()