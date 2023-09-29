import RPi.GPIO as GPIO
import time
import numpy as np
import sounddevice as sd
 
# Set the GPIO mode
GPIO.setmode(GPIO.BCM)
 
# Define GPIO pins for the ultrasonic sensor
TRIG = 17
ECHO = 27

#Constants for adjustment
FAST_SPEED_THRESHOLD = 2  # cm/sec
PITCH_ADJUSTMENT = 5  # Example value, adjust as needed
FILTER_CUTOFF_ADJUSTMENT = 5  # Example value
VOLUME_ADJUSTMENT = 0.1  # Example value
PANNING_ADJUSTMENT = 0.1  # Example value
RESONANCE_ADJUSTMENT = 0.1  # Example value
REVERB_ADJUSTMENT = 0.1  # Example value
ECHO_ADJUSTMENT = 0.1 


# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
# Parameters
chunk_duration = 0.1  # seconds, set to 0.1 for 100ms chunks
sampling_rate = 44000  # typical value for audio
 
 
def get_distance():
    # Send a short pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
 
    # Listen for the echo and calculate the duration
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()
 
    # Calculate distance
    distance = (end_time - start_time) * 34300 / 2
    return distance
 
def map_distance_to_frequency(distance):
    # Define a minimum and maximum frequency (in Hz)
    min_freq = 55.0  # for farthest distance
    max_freq = 555.0  # for closest distance
 
    # Define a minimum and maximum distance (in cm)
    min_distance = 2  # closest distance
    max_distance = 100  # farthest distance
 
    # Map the distance to the frequency
    frequency = ((distance - min_distance) / (max_distance - min_distance)) * (max_freq - min_freq) + min_freq
    return frequency
 
def calculate_speed_based_on_previous_position(prev_position, curr_position):
    delta_distance = curr_position - prev_position
    speed = delta_distance / chunk_duration
    return speed

def determine_current_interval(curr_position):
    # Example: if we're using 10cm intervals, then position 25cm would return interval 2
    return int(curr_position // 10)

def adjust_sound_parameters(pitch=None, filter_cutoff=None, volume=None, panning=None, resonance=None, reverb=None, echo=None):
    """
    Adjusts the sound parameters based on the provided values.
    """
    # Here, you'd integrate with the sound library to make the actual adjustments.
    # For now, we'll just print the adjustments for clarity.
    if pitch: print(f"Adjusting pitch to {pitch}")
    if filter_cutoff: print(f"Adjusting filter cutoff to {filter_cutoff}")
    if volume: print(f"Adjusting volume to {volume}")
    if panning: print(f"Adjusting panning to {panning}")
    if resonance: print(f"Adjusting resonance to {resonance}")
    if reverb: print(f"Adjusting reverb to {reverb}")
    if echo: print(f"Adjusting echo to {echo}")

def adjust_parameters_based_on_position(curr_position, index_interval):
    """
    Adjusts sound parameters based on the current position and index interval.
    """
    # Adjust parameters based on Index Interval
    pitch = adjust_pitch_based_on_interval(index_interval)
    filter_cutoff = adjust_filter_cutoff_based_on_interval(index_interval)
    volume = adjust_volume_based_on_interval(index_interval)
    panning = adjust_panning_based_on_position_in_interval(curr_position)
    
    adjust_sound_parameters(pitch=pitch, filter_cutoff=filter_cutoff, volume=volume, panning=panning)

def adjust_parameters_based_on_speed(speed):
    """
    Adjusts sound parameters based on the speed of hand movement.
    """
    if speed > 10:  # Define a threshold for "fast" speed
        pitch = introduce_vibrato_to_pitch()
        resonance = increase_resonance()
        reverb = reduce_reverb()
        echo = introduce_echo()
    else:
        pitch = maintain_steady_pitch()
        resonance = maintain_normal_resonance()
        reverb = maintain_normal_reverb()
        echo = reduce_or_remove_echo()
    
    adjust_sound_parameters(pitch=pitch, resonance=resonance, reverb=reverb, echo=echo)

def generate_sound_chunk(pitch, filter_cutoff, volume, panning, resonance, reverb, echo):
    # Generate a time array for the chunk
    t = np.linspace(0, chunk_duration, int(sampling_rate * chunk_duration), endpoint=False)
    
    # Generate a sine wave based on the pitch
    sine_wave = np.sin(2 * np.pi * pitch * t)
    
    # TODO: Apply filter based on filter_cutoff
    # TODO: Apply resonance
    # TODO: Apply reverb
    # TODO: Apply echo
    
    # Adjust volume
    sine_wave *= volume
    
    # Adjust panning (for simplicity, we'll just adjust volume for left and right channels)
    left_channel = sine_wave * (1 - panning)
    right_channel = sine_wave * panning
    
    # Combine channels into stereo sound
    stereo_sound = np.vstack((left_channel, right_channel)).T
    
    return stereo_sound.astype(np.float32).copy()


def adjust_pitch_based_on_interval(index_interval):
    # Placeholder logic: Increase pitch by a fixed amount for each interval
    return PITCH_ADJUSTMENT * index_interval

def adjust_filter_cutoff_based_on_interval(index_interval):
    return FILTER_CUTOFF_ADJUSTMENT * index_interval

def adjust_volume_based_on_interval(index_interval):
    return VOLUME_ADJUSTMENT * index_interval

def adjust_panning_based_on_position_in_interval(curr_position):
    # Placeholder logic: Pan based on position in the current interval
    return PANNING_ADJUSTMENT * (curr_position % 10)  # Assuming 10cm intervals

def introduce_vibrato_to_pitch():
    # Placeholder logic: Introduce a vibrato effect by adjusting pitch
    return PITCH_ADJUSTMENT * 2

def increase_resonance():
    return RESONANCE_ADJUSTMENT

def reduce_reverb():
    return -REVERB_ADJUSTMENT

def introduce_echo():
    return ECHO_ADJUSTMENT

def maintain_steady_pitch():
    return 0  # No change in pitch

def maintain_normal_resonance():
    return 0  # No change in resonance

def maintain_normal_reverb():
    return 0  # No change in reverb

def reduce_or_remove_echo():
    return -ECHO_ADJUSTMENT

stream = sd.OutputStream(samplerate=sampling_rate, channels=2)
stream.start()
# State Variables
previous_position = 0
previous_time = time.time()

# Main Loop
while True:
    current_position = get_distance()
    current_time = time.time()
    
    # Calculate speed based on previous position
    speed = (current_position - previous_position) / (current_time - previous_time)
    
    # Determine current interval
    index_interval = int(current_position // 10)  # Assuming 10cm intervals
    
    # Adjust parameters based on Index Interval
    pitch = adjust_pitch_based_on_interval(index_interval)
    filter_cutoff = adjust_filter_cutoff_based_on_interval(index_interval)
    volume = adjust_volume_based_on_interval(index_interval)
    panning = adjust_panning_based_on_position_in_interval(current_position)
    
    # Adjust parameters based on Speed
    if speed > FAST_SPEED_THRESHOLD:
        pitch += introduce_vibrato_to_pitch()
        resonance = increase_resonance()
        reverb = reduce_reverb()
        echo = introduce_echo()
    else:
        pitch += maintain_steady_pitch()
        resonance = maintain_normal_resonance()
        reverb = maintain_normal_reverb()
        echo = reduce_or_remove_echo()
    
    # Here, integrate with the sound library to adjust the sound parameters in real-time
    # For example, using the sounddevice library:
    sound_chunk = generate_sound_chunk(pitch, filter_cutoff, volume, panning, resonance, reverb, echo)
    stream.write(sound_chunk)
    
    # Update state variables for the next iteration
    previous_position = current_position
    previous_time = current_time
    
    time.sleep(0.1)  # Sleep for a short duration before the next measurement
