import pygame
from pyo import *
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen dimensions
WIDTH = 400
HEIGHT = 400

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultrasonic Sensor Simulation")

# Define the Sensor class
class Sensor:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 10)
        if self.orientation == "horizontal":
            pygame.draw.line(screen, GREEN, (self.x, self.y), (WIDTH, self.y), 2)
        else:
            pygame.draw.line(screen, GREEN, (self.x, self.y), (self.x, HEIGHT), 2)

    def detect(self, person):
        if self.orientation == "horizontal":
            if self.y - 5 < person.y < self.y + 5:
                return abs(self.x - person.x)
        else:
            if self.x - 5 < person.x < self.x + 5:
                return abs(self.y - person.y)
        return 400

# Define the Person class
class Person:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Change direction if person hits an edge
        if self.x <= 0 or self.x >= WIDTH:
            self.dx = -self.dx
        if self.y <= 0 or self.y >= HEIGHT:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 5)

# Create sensors and people
sensors = [
    Sensor(WIDTH // 4, 0, "horizontal"),
    Sensor(2 * WIDTH // 4, 0, "horizontal"),
    Sensor(3 * WIDTH // 4, 0, "horizontal"),
    Sensor(0, HEIGHT // 4, "vertical"),
    Sensor(0, 2 * HEIGHT // 4, "vertical"),
    Sensor(0, 3 * HEIGHT // 4, "vertical")
]
people = [Person() for _ in range(5)]

font = pygame.font.SysFont(None, 25)

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
    osc1.setFreq(map_value(measurements[0], 0, 400, 100, 500))
    osc2.setFreq(map_value(measurements[1], 0, 400, 50, 250))
    osc3.setFreq(map_value(measurements[2], 0, 400, 25, 125))
    fm.setCarrier(map_value(measurements[3], 0, 400, 100, 500))
    reverb.setRevtime(map_value(measurements[4], 0, 400, 0.5, 5))
    delay.setDelay(map_value(measurements[5], 0, 400, 0.1, 1))

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for sensor in sensors:
        sensor.draw()

    measurements = []
    for person in people:
        person.move()
        person.draw()
        for sensor in sensors:
            distance = sensor.detect(person)
            measurements.append(distance)
            if distance != 400:
                text = font.render(f"{distance} cm", True, BLACK)
                screen.blit(text, (sensor.x + 10, sensor.y + 10))

    # Modulate sound based on measurements
    modulate_sound(measurements)

    pygame.display.flip()
    pygame.time.wait(50)

pygame.quit()
s.stop()
