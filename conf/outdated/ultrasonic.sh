#!/bin/bash
 
# Define GPIO pins
TRIG=17
ECHO=27
 
# Set up the GPIO pins
raspi-gpio set $TRIG op
raspi-gpio set $ECHO ip
 
while true; do
    # Send a 10us pulse to TRIG
    raspi-gpio set $TRIG dh
    sleep 0.00001
    raspi-gpio set $TRIG dl
 
    # Wait for ECHO to go high
    while [ $(raspi-gpio get $ECHO | awk '{print $NF}') == "l" ]; do
        pulse_start=$(date +%s%N)
    done
 
    # Wait for ECHO to go low
    while [ $(raspi-gpio get $ECHO | awk '{print $NF}') == "h" ]; do
        pulse_end=$(date +%s%N)
    done
 
    pulse_duration=$((pulse_end - pulse_start))
    # Convert to seconds
    pulse_duration=$(echo "scale=10; $pulse_duration/1000000000" | bc)
    distance=$(echo "scale=2; $pulse_duration * 17150" | bc)
 
    # Send distance to Pure Data using pdsend
    echo "$distance;" | pdsend 3000 localhost udp
 
    sleep 1
done
#!/bin/bash
 
# Define GPIO pins
TRIG=17
ECHO=27
 
# Set up the GPIO pins
raspi-gpio set $TRIG op
raspi-gpio set $ECHO ip
 
while true; do
    # Send a 10us pulse to TRIG
    raspi-gpio set $TRIG dh
    sleep 0.00001
    raspi-gpio set $TRIG dl
 
    # Wait for ECHO to go high
    while [ $(raspi-gpio get $ECHO | awk '{print $NF}') == "l" ]; do
        pulse_start=$(date +%s%N)
    done
 
    # Wait for ECHO to go low
    while [ $(raspi-gpio get $ECHO | awk '{print $NF}') == "h" ]; do
        pulse_end=$(date +%s%N)
    done
 
    pulse_duration=$((pulse_end - pulse_start))
    # Convert to seconds
    pulse_duration=$(echo "scale=10; $pulse_duration/1000000000" | bc)
    distance=$(echo "scale=2; $pulse_duration * 17150" | bc)
 
    # Send distance to Pure Data using pdsend
    echo "$distance;" | pdsend 3000 localhost udp
 
    sleep 1
done