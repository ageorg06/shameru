from pyo import *
import time

# Start the pyo server
s = Server().boot()
s.start()

# Initialize sound elements
osc1 = Sine(freq=100, mul=0.3)
osc2 = LFO(freq=50, type=3, mul=0.9)
osc3 = Osc(table=SquareTable(), freq=25, mul=0.3)
drone_sound = osc1 + osc2 + osc3
fm = FM(carrier=100, ratio=[0.2498, 0.2503], index=10, mul=0.3)
drone_sound += fm
reverb = STRev(drone_sound, inpos=[0, 1], revtime=2, cutoff=5000, bal=0.3).out()
delay = Delay(reverb, delay=0.5, feedback=0.5).out()

def modulate_sound(measurements):
    # Assuming measurements is a list of 6 values from the ultrasonic sensors
    osc1.setFreq(map_value(measurements[0], 0, 400, 100, 500))
    osc2.setFreq(map_value(measurements[1], 0, 400, 50, 250))
    osc3.setFreq(map_value(measurements[2], 0, 400, 25, 125))
    fm.setCarrier(map_value(measurements[3], 0, 400, 100, 500))
    reverb.setRevtime(map_value(measurements[4], 0, 400, 0.5, 5))
    delay.setDelay(map_value(measurements[5], 0, 400, 0.1, 1))

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Simulation loop
while True:
    # Placeholder for getting measurements from ultrasonic sensors
    # Replace this with actual sensor reading logic
    measurements = [random.uniform(0, 400) for _ in range(6)]
    
    # Modulate sound based on measurements
    modulate_sound(measurements)
    
    # Sleep for a short duration before the next iteration
    time.sleep(1)
