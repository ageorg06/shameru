from pyo import *
import time
import random

# Initialize the pyo server
s = Server().boot()
s.start()

# Define default sound parameters
base_freq = 220.0  # A3 note for a deeper tone

# Create multiple oscillators with different harmonics
osc1 = Sine(freq=base_freq, mul=0.1)
osc2 = Sine(freq=base_freq * 1.5, mul=0.075)  # Perfect fifth
osc3 = Sine(freq=base_freq * 2, mul=0.05)     # Octave

# Frequency modulation for a richer sound
fm = FM(carrier=base_freq, ratio=[0.2498, 0.2503], index=10, mul=0.3)

# Combine oscillators and FM
drone_sound = osc1 + osc2 + osc3 + fm

# Low-pass filter for a smoother, darker sound
filter = Biquad(drone_sound, freq=800, q=5, type=0)

# Enhanced reverb for spaciousness
reverb = STRev(filter, inpos=[0, 1], revtime=2, cutoff=4000, bal=0.5).out()

# Rhythmic element
metro = Metro(time=0.5).play()
envelope = TrigEnv(metro, table=HannTable(), dur=0.5, mul=0.5)
rhythm = osc1 * envelope

def update_sound(distances):
    """
    Update the sound parameters based on the distances from the sensors.
    :param distances: List containing distance readings from the 6 sensors.
    """
    # Modulate osc1 frequency and amplitude based on Sensor 1
    osc1.setFreq(base_freq * distances[0])
    osc1.setMul(distances[0] * 0.01)

    # Modulate osc2 frequency and amplitude based on Sensor 2
    osc2.setFreq((base_freq * 1.5) * distances[1])
    osc2.setMul(distances[1] * 0.0075)

    # Modulate osc3 frequency and amplitude based on Sensor 3
    osc3.setFreq((base_freq * 2) * distances[2])
    osc3.setMul(distances[2] * 0.005)

    # Modulate FM based on Sensor 4
    fm.setCarrier(base_freq * distances[3])
    fm.setMul(distances[3] * 0.01)

    # Modulate filter frequency based on Sensor 5
    filter.setFreq(400 + distances[4] * 15)

    # Modulate reverb depth based on Sensor 6
    reverb.setBal(distances[5] * 0.01)

# Main loop
while True:
    # Placeholder for distance readings (replace with actual sensor readings)
    distances = [random.uniform(0, 4) for _ in range(6)]
    
    # Update the sound parameters based on distances
    update_sound(distances)

    # Sleep for a short duration before updating again
    time.sleep(0.4)
