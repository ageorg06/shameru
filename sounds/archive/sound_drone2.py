from pyo import *

import time
import random 

# Initialize the pyo server
s = Server().boot()
s.start()

notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C4 to C5
note_counter = 0

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

def midiToHz(midi_note):
    return Sig(440.0) * Pow(2.0, (midi_note - 69) / 12.0)
    
# Define rhythm pattern and amplitude variation
metro = Metro(time=0.5).play()  # Metronome for rhythm
trig_noise = TrigXnoiseMidi(metro, dist=12, mrange=(60, 96))  # Triggered noise for amplitude variation
freq = midiToHz(trig_noise)  # Convert MIDI to frequency in Hz
amp = freq * 0.05  # Amplitude variation based on frequency
print("Frequency:", freq)

# Apply amplitude variation to sound elements
osc1.setMul(amp)
osc2.setMul(amp)
osc3.setMul(amp)
fm.setMul(amp)



def start_sound():
    """
    Start playing the sound with default parameters.
    """
    # The sound is already initialized with default parameters


def update_sound():
    """
    Update the sound parameters to create a base sound with random variations.
    """
    # Define a base frequency for the sound
    base_freq = 440.0  # A4 note as the base frequency
    
    # Randomly vary the frequency around the base frequency
    freq_variation = random.uniform(0.95, 1.05)  # Vary between 95% and 105% of the base frequency
    freq = base_freq * freq_variation
    
    # Randomly vary the amplitude
    amp = random.uniform(0.05, 0.1)  # Vary the amplitude between 0.05 and 0.1
    
    # Update sound parameters
    osc1.setFreq(freq)
    osc2.setFreq(freq / 2)
    osc3.setFreq(freq / 4)
    fm.setCarrier(freq)
    osc1.setMul(amp)
    osc2.setMul(amp)
    osc3.setMul(amp)
    fm.setMul(amp)

        
    # Apply filter
    filter_freq = random.uniform(200, 2000)
    filter_q = random.uniform(0.5, 5)
    filter.freq = filter_freq
    filter.q = filter_q
    
    # Apply envelope
    attack = random.uniform(0.01, 0.1)
    decay = random.uniform(0.1, 0.5)
    sustain = random.uniform(0.5, 1)
    release = random.uniform(0.1, 0.5)
    envelope.setAttack(attack)
    envelope.setDecay(decay)
    envelope.setSustain(sustain)
    envelope.setRelease(release)

distance_percentage = 0 
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
    update_sound()

    osc1.setFreq(notes[note_counter % len(notes)])

    note_counter = note_counter + 1
    # Sleep for a short duration before updating again
    time.sleep(1)
