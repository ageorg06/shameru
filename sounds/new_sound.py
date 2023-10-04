import pyo
import random
import time
from ultrasonic import get_sensor_percentages, initialize_pyo_server

def initialize_pyo_server():
    """Initialize the pyo server."""
    server = pyo.Server().boot()
    server.start()
    return server

def create_base_sound():
    """Create a rhythmic atmospheric base sound with reverb and echo."""
    # Multiple oscillators for rhythmic pattern
    sine_wave1 = pyo.Sine(freq=110, mul=0.8)
    sine_wave2 = pyo.Sine(freq=115, mul=0.8)
    sine_wave3 = pyo.Sine(freq=120, mul=0.8)
    
    # Different LFO rates for varied amplitude modulation
    lfo1 = pyo.Sine(freq=0.5, mul=0.4, add=0.6)
    lfo2 = pyo.Sine(freq=0.6, mul=0.4, add=0.6)
    lfo3 = pyo.Sine(freq=0.7, mul=0.4, add=0.6)

    rhythmic_sine1 = sine_wave1 * lfo1
    rhythmic_sine2 = sine_wave2 * lfo2
    rhythmic_sine3 = sine_wave3 * lfo3

    combined_wave = rhythmic_sine1 + rhythmic_sine2 + rhythmic_sine3

    # UFO-like sweeping frequency modulation
    sweep = pyo.Sine(freq=0.1, mul=50, add=115)  # Slow LFO with a wide frequency range
    ufo_wave = pyo.Sine(freq=sweep, mul=0.6).mix(2)  # Sine wave modulated by the sweeping LFO

    # Noise generator for wind
    noise = pyo.Noise(mul=0.25)
    
    # Adjusted bandpass filter to shape the noise into wind
    wind = pyo.Biquad(noise, freq=800, q=0.5, type=2).mix(2)  # Adjusted frequency and q value

    # Amplitude modulation for dynamic wind variations
    lfo_wind_amplitude = pyo.Sine(freq=0.1, mul=0.2, add=0.6)  # Slower LFO for amplitude variations
    modulated_wind_amplitude = wind * lfo_wind_amplitude

    # Frequency modulation for dynamic wind variations
    lfo_wind_frequency = pyo.Sine(freq=0.05, mul=200, add=800)  # Slow LFO for frequency variations
    modulated_wind = pyo.Biquad(modulated_wind_amplitude, freq=lfo_wind_frequency, q=0.5, type=2).mix(2)

    # The constant part of the sound
    constant_sound = combined_wave + modulated_wind

    # The part of the sound to which effects will be applied
    effect_sound = ufo_wave

    # Combine the constant and effect sounds
    combined_sound = constant_sound + effect_sound

    # Add reverb for a dark atmospheric effect
    reverb = pyo.Freeverb(combined_sound, size=0.99, damp=0.85, bal=0.8)
    
    # Add echo for a more expansive sound
    echo = pyo.Delay(reverb, delay=0.5, feedback=0.5, mul=0.5).out()

    return constant_sound, effect_sound

def create_atmospheric_beat():
    """Create a soft atmospheric beat."""
    # Sine wave for a deep kick drum sound
    kick = pyo.Sine(freq=50, mul=0.5).play(delay=0.5, dur=0.1)

    # Noise for a snare sound, filtered to make it softer
    snare_noise = pyo.Noise(mul=0.3)
    snare = pyo.Biquad(snare_noise, freq=2000, q=5, type=0).play(delay=1.0, dur=0.1)

    # Combine the kick and snare
    beat = kick + snare

    return beat

def pitch_shift_effect(sound, percentage):
    """Apply a pitch shift effect to the sound based on the given percentage."""
    # Adjust the shift value calculation to handle negative percentages
    shift_value = percentage * 5  # This will give a range from -500 to 500
    pitch_shifted = pyo.FreqShift(sound, shift=shift_value)
    return pitch_shifted

def phaser_effect(sound, percentage):
    """Apply a phaser effect to the sound based on the given percentage."""
    # Adjust the frequency value calculation to handle negative percentages
    freq_value = 0 + (percentage / 100 * 1)  # This will give a range from 0.1 to 2.1
    phaser = pyo.Phaser(sound, freq=freq_value, spread=1.5, q=5, feedback=0.5, num=32).out()
    return phaser

def filter_sweep_effect(sound, percentage):
    """Apply a filter sweep effect to the sound based on the given percentage."""
    # Adjust the frequency value calculation to handle negative percentages
    freq_value = 0 + (percentage / 100 * 950)  # This will give a range from 100 to 2000
    filtered_sound = pyo.Biquad(sound, freq=freq_value, q=5, type=0).out()  # type=0 is a lowpass filter
    return filtered_sound

def panning_effect(sound, percentage):
    """
    Apply a panning effect to the sound based on the given percentage.
    
    Args:
    - sound: The sound source to which the panning will be applied.
    - percentage: A value between -100 and 100. Negative values pan to the left, positive values pan to the right.
    
    Returns:
    - A sound object with the panning effect applied.
    """
    # Map the percentage to a pan value (from 0 to 1, where 0.5 is center, 0 is left, and 1 is right)
    pan_value = 0.5 + (percentage / 200)
    panned_sound = pyo.Pan(sound, pan=pan_value).out()
    return panned_sound


def play_interactive_sound(server):
    initialize_pyo_server()
    constant_sound, effect_sound = create_base_sound()
    constant_sound.out()
    
    pitch_shifted = pitch_shift_effect(effect_sound, 0)
    phasered = phaser_effect(effect_sound, 0)
    filtered = filter_sweep_effect(effect_sound, 0)
    panned = panning_effect(effect_sound, 0)
    
    pitch_shifted.out()
    phasered.out()
    filtered.out()
    panned.out()

    print("Playing the sound with effects intensity based on ultrasonic sensor readings. Press Ctrl+C to stop.")
    
    rhythmic_pattern = [0.5, 0.75, 0.5, 1.0]
    pattern_index = 0

    try:
        while True:
            percentages = get_sensor_percentages()
            
            pitch_shifted.setShift(-500 + (percentages[0] * 10))
            phasered.setFreq(0.1 + (percentages[1] / 100 * 1.9))
            filtered.setFreq(100 + (percentages[2] / 100 * 1900))
            pan_value = 0.5 + (percentages[3] / 200)
            panned.setPan(pan_value)

            print(f"Sensor readings - Pitch Shift: {percentages[0]:.2f}%, Phaser: {percentages[1]:.2f}%, Filter Sweep: {percentages[2]:.2f}%, Panning: {percentages[3]:.2f}%")
            
            time.sleep(rhythmic_pattern[pattern_index])
            pattern_index = (pattern_index + 1) % len(rhythmic_pattern)

    except KeyboardInterrupt:
        print("Stopping the sound...")
        server.stop()
if __name__ == "__main__":
    server = initialize_pyo_server()
    play_interactive_sound(server)
