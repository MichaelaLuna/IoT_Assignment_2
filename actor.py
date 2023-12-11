
""" The overall purpose of this code is to set up a connection 
to an MQTT broker, subscribe to a specific topic, and control a GPIO pin 
on a Raspberry Pi based on the received MQTT messages (turning it on or off) """



# Import the necessary libraries

import paho.mqtt.client as mqtt   # MQTT client library
import RPi.GPIO as GPIO           # GPIO library for Raspberry Pi
GPIO.setmode(GPIO.BCM)            # Set GPIO mode to BCM
GPIO.setup(2, GPIO.OUT)           # Set up GPIO pin 2 as an output pin


""" ----------------------------------------------------------------------------------------------------------- """


# Define the MQTT broker and topic

broker_address = "localhost"   # Replace with the Raspberry Pi's IP if not running locally
topic = "terra/led"            # Replace with the desired MQTT topic


""" ----------------------------------------------------------------------------------------------------------- """


# Callback functions for MQTT client

""" Callback functions are used to define how the script should react to 
    MQTT events such as connecting to the broker and receiving messages """


def on_connect(client, userdata, flags, rc): # Callback function called when the MQTT client connects to the broker
    
    print("Connected to MQTT broker with result code " + str(rc)) # Prints if its connected or not
    client.subscribe(topic)                                       # Subscribes to the specific topic
    

""" ----------------------------------------------------------------------------------------------------------- """


def on_message(client, userdata, message): # Callback function called when a message is received on the subscribed topic

    # Decodes the payload and, based on its value, turns GPIO pin 2 on or off. 
    
    value = message.payload.decode("utf-8")
    
    if value == "on":
       GPIO.output(2, 1)  # Turn GPIO pin 2 on
        
    elif value == "off":
       GPIO.output(2, 0)  # Turn GPIO pin 2 off
        
    print(f"Received message on topic '{message.topic}': {message.payload.decode()}") # Prints if message is received




