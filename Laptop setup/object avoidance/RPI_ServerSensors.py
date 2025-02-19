# server.py

import socket
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

def distance(trigger,echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


HOST = "192.168.7.3"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Setting up the connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print(f"Connected by {addr}")

# Setting up sensors
GPIO_TRIGGER_LIST = [22, 18, 17, 5, 25, 2]
GPIO_ECHO_LIST = [27, 23, 4, 19, 8, 3]

# Initializing distances
dist_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

while True:
    # Waiting for request
    data = conn.recv(1024)
    if not data:
        break

    # Updating distances
    for k in range(0,len(GPIO_TRIGGER_LIST)):
        trigger = GPIO_TRIGGER_LIST[k]
        echo = GPIO_ECHO_LIST[k]

        # Set GPIO direction (IN / OUT)
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

        dist_list[k] = round(distance(trigger,echo),1)

    # Sending response
    res = " ".join([str(d) for d in dist_list])
    conn.sendall(bytearray(res,'utf8'))
