import pygame.mixer

# Initialize the pygame mixer
pygame.mixer.init()

# Load the audio file
pygame.mixer.music.load("song.wav")  # Replace with the path to your audio file

# Set the volume (0.0 to 1.0)
pygame.mixer.music.set_volume(0.8)

# Play the audio file on repeat
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Keep the program running to continue playing the music
try:
    while pygame.mixer.music.get_busy():
        pass
except KeyboardInterrupt:
    # If user presses Ctrl+C, stop the music and exit
    pygame.mixer.music.stop()
