from pyo import *
import time
import random 

# Initialize the pyo server
s = Server().boot()
s.start()

# Define default sound parameters
default_freq = 100
default_reverb_size = 0.5
default_filter_cutoff = 5000

# Create multiple oscillators with different waveforms and frequencies
osc1 = Sine(freq=default_freq, mul=0.1)
osc2 = LFO(freq=50, type=3, mul=0.1)  # Sawtooth wave
osc3 = Osc(table=SquareTable(), freq=25, mul=0.1)

# Combine the oscillators
drone_sound = osc1 + osc2 + osc3

# Apply frequency modulation
fm = FM(carrier=default_freq, ratio=[0.2498, 0.2503], index=10, mul=0.3)
drone_sound += fm

# Apply reverb and delay effects
reverb = STRev(drone_sound, inpos=[0, 1], revtime=default_reverb_size, cutoff=default_filter_cutoff, bal=0.3).out()
delay = Delay(reverb, delay=0.5, feedback=0.5).out()

def start_sound():
    """
    Start playing the sound with default parameters.
    """
    # The sound is already initialized with default parameters

def update_sound(distance_percentage):
    """
    Update the sound parameters based on the percentage of distance.
    
    :param distance_percentage: Percentage of distance (0 to 100).
    """
    # Map distance_percentage to sound parameters
    freq = map(distance_percentage, 0, 100, default_freq, default_freq * 2)
    reverb_size = map(distance_percentage, 0, 100, default_reverb_size, 1)
    filter_cutoff = map(distance_percentage, 0, 100, default_filter_cutoff, 10000)
    
    # Update sound parameters
    osc1.setFreq(freq)
    osc2.setFreq(freq / 2)
    osc3.setFreq(freq / 4)
    fm.setCarrier(freq)
    reverb.setRevtime(reverb_size)
    reverb.setCutoff(filter_cutoff)
    delay.setDelay(map(distance_percentage, 0, 100, 0.5, 1))

def map(value, in_min, in_max, out_min, out_max):
    """
    Map a value from one range to another.
    
    :param value: Input value.
    :param in_min: Minimum of the input range.
    :param in_max: Maximum of the input range.
    :param out_min: Minimum of the output range.
    :param out_max: Maximum of the output range.
    :return: Mapped value.
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Start playing the sound
start_sound()
distance_percentage = 0
# Update the sound in a loop (replace with actual sensor reading logic)
while True:
    # Placeholder for distance_percentage (replace with actual sensor reading)
    distance_percentage =  random.uniform(0, 100)
    
    # Update the sound parameters based on distance_percentage
    update_sound(distance_percentage)
    
    # Sleep for a short duration before updating again
    time.sleep(1)
