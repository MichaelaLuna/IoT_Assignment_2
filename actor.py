import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)






# Define the MQTT broker and topic
broker_address = "localhost"  # Replace with the Raspberry Pi's IP if not running locally
topic = "terra/led"  # Replace with the desired MQTT topic

# Callback functions for MQTT client
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, message):
    value = message.payload.decode("utf-8")
    if value == "on":
       GPIO.output(2,1)
    elif value == "off":
       GPIO.output(2,0)
    print(f"Received message on topic '{message.topic}': {message.payload.decode()}")
