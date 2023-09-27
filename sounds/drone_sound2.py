from pyo import *
import time  # Import the time module

# Start the pyo server
s = Server().boot()
s.start()

# Create multiple oscillators with different waveforms and frequencies
osc1 = Sine(freq=100, mul=0.3)
osc2 = LFO(freq=50, type=3, mul=0.9)  # Using LFO with type=3 for sawtooth wave
osc3 = Osc(table=SquareTable(), freq=25, mul=0.3)

# Combine the oscillators
drone_sound = osc1 + osc2 + osc3

# Apply frequency modulation
fm = FM(carrier=100, ratio=[0.2498, 0.2503], index=10, mul=0.3)
drone_sound += fm

# Apply reverb and delay effects
reverb = STRev(drone_sound, inpos=[0, 1], revtime=2, cutoff=5000, bal=0.3).out()
delay = Delay(reverb, delay=0.5, feedback=0.5).out()

# Play the sound for a duration (e.g., 30 seconds)
s.recstart()
time.sleep(30)
s.recstop()

# Keep the program running
s.gui(locals())
