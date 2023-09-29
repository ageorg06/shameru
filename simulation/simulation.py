import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pygame.mixer
import math
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
from pydub.generators import Sine

# Initialize the pygame mixer
pygame.mixer.init()

# Load the audio file
song = AudioSegment.from_wav("song.wav")
pygame.mixer.music.load("song.wav")

# Set the volume (0.0 to 1.0)
pygame.mixer.music.set_volume(0.1)

# Play the audio file on repeat
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Room dimensions
room_width = 3.55
room_length = 3.25
base_frequencies = [110, 130.81, 146.83]

current_volume = 0.0
fig, ax = plt.subplots()
room = patches.Rectangle((0, 0), room_width, room_length, fill=False)
ax.add_patch(room)

# Entrance
entrance_width = 0.5
entrance_height = 0.1
entrance = patches.Rectangle((0, 0), entrance_width, entrance_height, fill=True, color='green')
ax.add_patch(entrance)

# Human dot
human_dot, = ax.plot(1, 1, 'ro', markersize=5)  # Initial position at (1m, 1m)

# Sensor positions and their corresponding "laser" lines with unique identifiers
sensors = {
    'left': [room_length * 1/3, room_length * 2/3],
    'top': [room_width * 1/5, room_width * 2/5, room_width * 3/5, room_width * 4/5]
}
lasers = []
sensor_ids = []

# Draw "laser" lines for sensors
sensor_count = 1
for y in sensors['left']:
    line, = ax.plot([0, room_width], [y, y], 'g-')  # Horizontal lasers
    lasers.append(line)
    sensor_ids.append(f"Sensor-{sensor_count}")
    sensor_count += 1

for x in sensors['top']:
    line, = ax.plot([x, x], [0, room_length], 'g-')  # Vertical lasers
    lasers.append(line)
    sensor_ids.append(f"Sensor-{sensor_count}")
    sensor_count += 1

def adjust_volume(percentage):
    """Adjust the volume based on the distance from the sensor."""
    volume = percentage / 100
    pygame.mixer.music.set_volume(volume)
    print(f"Volume set to: {volume*100}%")

def check_intersection(event):
    """
    Check if the person represented by a dot intersects with the ultrasonic sensors' signals.
    Adjust the sound based on the intersection.
    """
    # Check if event data is available
    if event.xdata is None or event.ydata is None:
        return
    
    # Get the person's position from the event
    person_x = event.xdata
    person_y = event.ydata
    
    # Define the positions and ranges of the ultrasonic sensors
    sensors = [
        {'x': sensor1_x, 'y': sensor1_y, 'range': sensor1_range},
        {'x': sensor2_x, 'y': sensor2_y, 'range': sensor2_range},
        # Add more sensors as needed
    ]
    
    # Iterate through each sensor and check for intersection
    for sensor in sensors:
        distance = calculate_distance(person_x, person_y, sensor['x'], sensor['y'])
        if distance <= sensor['range']:
            # The person is within the sensor's range, adjust the sound
            adjust_sound(sensor)


def check_intersection():
    """Check if the human dot intersects with any laser line."""
    x, y = human_dot.get_data()
    x = x[0]
    y = y[0]
    for idx, line in enumerate(lasers):
        lx, ly = line.get_data()
        if abs(lx[0] - lx[1]) < 0.01:  # Approximate check for vertical laser
            if abs(x - lx[0]) < 0.2 and 0 <= y <= room_length:  # Increased threshold
                line.set_color('red')
                distance = abs(y - ly[0])
                print(f"{sensor_ids[idx]} activated. Distance: {distance:.2f} meters.")
                if idx == 2:
                    max_distance = room_length

                    intensity = distance / max_distance
                    room_size = 100 * intensity
                    damping = 1 - intensity
                    
                    sine_wave = Sine(440)
                    sound = sine_wave.to_audio_segment(duration=1000) 
                    reverb_sound = sound._spawn(sound.raw_data, overrides={
                        "frame_rate": int(sound.frame_rate * (1 + intensity))
                    }).set_frame_rate(sound.frame_rate)

                    play(reverb_sound)
                
                if idx == 3:
                    max_distance = room_length
                    adjustment_factor = 1 - (distance / max_distance)

                    adjustment_factor = 1 - (distance / max_distance)

                    frequencies = [base_frequency * (1 + adjustment_factor) for base_frequency in base_frequencies]
                    volumes = [-20 + (0 - (-20)) * adjustment_factor for _ in base_frequencies]
                    
                    adjusted_drone_sound = sum(Sine(frequency).to_audio_segment(duration=5000, volume=volume) for frequency, volume in zip(frequencies, volumes))

                    play(adjusted_drone_sound)
            else:
                line.set_color('green')
        else:  # Horizontal laser
            if abs(y - ly[0]) < 0.2 and 0 <= x <= room_width:  # Increased threshold
                line.set_color('red')
                distance = abs(x - lx[0])
                print(f"{sensor_ids[idx]} activated. Distance: {distance:.2f} meters.")
                if idx == 0:
                    percentage = (distance/room_width) * 100
                    adjust_volume(100 - percentage)
                if idx == 1:
                    base_frequency = 440
                    max_frequency = 880
                    max_distance = room_width

                    frequency = base_frequency + (max_frequency - base_frequency) * (1 - distance / max_distance)
                    sample_rate = 44100
                    duration = 0.1  # duration of the beep in seconds
                    t = np.linspace(0, duration, int(sample_rate * duration), False)
                    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
                    stereo_waveform = np.vstack((waveform, waveform)).T
                    stereo_waveform = np.ascontiguousarray(stereo_waveform)
                    sound = pygame.sndarray.make_sound(np.int16(stereo_waveform * 32767))
                    sound.play()
            else:
                line.set_color('green')

# Variables to check if the dot is selected and should move
is_selected = False

def apply_echo(start_time_ms):
    song = AudioSegment.from_wav("song.wav")
    
    # Extract a segment starting from the current playback position
    segment = song[start_time_ms:start_time_ms + 5000]  # 5 seconds segment
    
    # Create the echo (a quieter version of the segment)
    echo = segment - 20
    
    # Combine the original segment with the echo starting 300ms later
    combined = segment.overlay(echo, position=300)
    
    # Play the combined sound
    play(combined)

def on_press(event):
    global is_selected
    if abs(event.xdata - human_dot.get_xdata()) < 0.1 and abs(event.ydata - human_dot.get_ydata()) < 0.1:
        is_selected = True

def on_release(event):
    global is_selected
    is_selected = False

def on_motion(event):
    if is_selected:
        human_dot.set_data(event.xdata, event.ydata)
        check_intersection()  # Check for intersection each time the dot moves
        fig.canvas.draw()

# Connect the event handlers to the figure
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

ax.set_xlim(0, room_width)
ax.set_ylim(0, room_length)
ax.set_aspect('equal')
plt.show()
