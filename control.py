
""" This code establishes an MQTT connection, subscribes to specified topics, and executes actions 
based on predefined conditions and results stored in a configuration file (in this case, "config.json") """


""" --------------------------------------------------------------------------------------------------------------- """


# Import the necessary libraries

import paho.mqtt.client as mqtt  # MQTT client library
import json                      # JSON handling library


""" --------------------------------------------------------------------------------------------------------------- """


# Define a class for the IoT Controller

class IoT_Controller:

    # Class-level variables

    configuration = []  # Store the loaded configuration
    client = None       # MQTT client instance
    mqtt_data = {}      # Dictionary to store MQTT data received


""" --------------------------------------------------------------------------------------------------------------- """


    # Method to configure the IoT Controller with a given filename

    def configure(filename):

        # Configure the MQTT client and load the configuration from a file

        IoT_Controller.client = mqtt.Client()
        with open(filename, 'r') as file:

            IoT_Controller.configuration = json.load(file)

        IoT_Controller.client.on_message = IoT_Controller.on_message
        IoT_Controller.client.connect("localhost", 1883)

        for rule in IoT_Controller.configuration:
            for condition in rule["conditions"]:

                IoT_Controller.client.subscribe(condition["topic"])
                print(condition["topic"])


""" --------------------------------------------------------------------------------------------------------------- """


    # Method to run the IoT Controller
    
    def run():

        # Start the MQTT client loop

        print("run method before loop_forever")  // To verify before
        IoT_Controller.client.loop_forever()     // Running
        print("run method after loop_forever")   // To verify after


""" --------------------------------------------------------------------------------------------------------------- """

    # Method called when a new MQTT message is received
    
    def on_message(client, userdata, message):

        # Process incoming MQTT messages

        value = int(message.payload.decode("utf-8"))
        topic = message.topic
        IoT_Controller.mqtt_data[topic] = value
        IoT_Controller.run_rules()

""" --------------------------------------------------------------------------------------------------------------- """
    # Method to run the rules based on the received MQTT data
    
    def run_rules():

        # Evaluate conditions and execute corresponding results

        for rule in IoT_Controller.configuration:
            conditions_met = all(IoT_Controller.evaluate_condition(IoT_Controller.mqtt_data, condition) for condition in rule["conditions"])

            if conditions_met:

                # Execute the results for the matched rule

                for message in rule["results"]:
                    IoT_Controller.client.publish(message["topic"], message["value"])


""" --------------------------------------------------------------------------------------------------------------- """

    # Method to evaluate a single condition based on MQTT data
    
    def evaluate_condition(data, condition):

        # Extract relevant information from the condition

        topic = condition["topic"]
        value = data.get(topic, None)
        if value is None:
            return False

        # Compare the value with the condition and return the result

        comparison = condition["comparison"]
        if comparison == "<":
            return value < condition["value"]
        elif comparison == "<=":
            return value <= condition["value"]
        elif comparison == "==":
            return value == condition["value"]
        elif comparison == "!=":
            return value != condition["value"]
        elif comparison == ">":
            return value > condition["value"]
        elif comparison == ">=":
            return value >= condition["value"]
        else:
            return False

""" --------------------------------------------------------------------------------------------------------------- """

# Main function to execute when the script is run

def main():

    # Configure and run the IoT Controller

    IoT_Controller.configure("config.json")
    IoT_Controller.run()

# Entry point for the script

if __name__ == "__main__":
    main()

""" --------------------------------------------------------------------------------------------------------------- """

