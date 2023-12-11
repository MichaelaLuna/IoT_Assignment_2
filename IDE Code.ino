
/* This code essentially turns the ESP32 into an MQTT-enabled device that periodically 
   publishes sensor data to a specified topic. The device connects to Wi-Fi and establishes 
   an MQTT connection, ensuring the continuous flow of data. */



/* ----------------------------------------------------------------------------------------- */

// Libraries to integrate functionality

#include <WiFi.h>         // For the wifi connection
#include <PubSubClient.h> // For the MQTT messaging
#include <Arduino.h>      // For the Input and output

/* ----------------------------------------------------------------------------------------- */

// Wi-Fi credentials: replace with those of your network

const char* ssid = "iot_wireless";  // The name of the WiFi network
const char* password = "Unsecure!"; // The WiFi network passkey

/* ----------------------------------------------------------------------------------------- */

// MQTT broker details: replace with your own

const char* mqtt_server = "michaela-pi.local"; // The MQTT broker's hostname or IP address
const int mqtt_port = 1883;                    // MQTT broker port (1883 is default)
const char* mqtt_topic = "terra/hum";          // MQTT topic to publish messages

/* ----------------------------------------------------------------------------------------- */


// MQTT client name prefix (will add MAC address)

String name = "ESP32Client_";

WiFiClient espClient;            // Create an instance of the WiFiClient class
PubSubClient client(espClient);  // Create an instance of the PubSubClient class

// Timer for publishing every 5 seconds

unsigned long previousMillis = 0;
const long interval = 5000;

String Message;


/* ----------------------------------------------------------------------------------------- */

void setup() {           // Start Serial Communication

  Serial.begin(115200);  // Set to this Baud Rate
  pinMode(34,INPUT);     // Set GPIO pin 34 of ESP32 Board

  // Read the MAC address

  uint8_t mac[6];
  esp_read_mac(mac, ESP_MAC_WIFI_STA);

  // Convert MAC address to a string

  char macStr[18];        // MAC address is 12 characters long without separators, plus null terminator

  snprintf(macStr, sizeof(macStr), "%02X:%02X:%02X:%02X:%02X:%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]); 

  name = name + macStr;   // Concatenate the name prefix with the MAC address
  

  /* ----------------------------------------------------------------------------------------- */
  

  // Connect to Wi-Fi

  WiFi.begin(ssid, password);                // Set the ssid and password to this
  while (WiFi.status() != WL_CONNECTED) {    // The Condition
    delay(1000);                             // Delay for 1 second
    Serial.println("Connecting to WiFi..."); // To Verify if a Connection is being establish
  }                                          // End of While

  Serial.println("Connected to WiFi");       // To Verify if the Connection is Established

  client.setServer(mqtt_server, mqtt_port);  // Set MQTT server and port

}                                            // End of Setup


/* ----------------------------------------------------------------------------------------- */


void loop() {                  // Connect to MQTT if necessary

  if (!client.connected()) {   // If this is the Situation
    connect();                 // Do this
  }                            // End of If

  unsigned long currentMillis = millis();  // Get the current time

  // Publish a message every 5 seconds

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    String message = "Hello all from " + name;   // Your message to publish

    // Publish the message to the MQTT topic

    client.publish("terra/hum", Message.c_str());
    Serial.println("Message sent: Hello all from " + name);

  }  // End of If
  

  /* ----------------------------------------------------------------------------------------- */
  

  // Allow the PubSubClient to process incoming messages

  client.loop();                  
  Message = String(analogRead(34));

  Serial.println(analogRead(34));   // To Verify if the GPIO pin 34 is Outputting

  Serial.println("Analog Sensor Value: " + String(analogRead(34)));  // Print the analog sensor value to Serial Monitor

}  // End of Loop


/* ----------------------------------------------------------------------------------------- */


void connect() {   // Function to Connect

  // Loop until we're reconnected

  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");  // To Verify if Connection is Being Establish

    // Attempt to connect

    if (client.connect(name.c_str())) {                // If this is the Case
      Serial.println("Connected to MQTT broker");      // Print this

    } else {                                                    // If it is not, then..
      Serial.print("Failed to connect to MQTT broker, rc=");    // Print that it Failed to Connect
      Serial.print(client.state());                             // And the State 
      Serial.println("Try again in 5 seconds");                 // And that it Would Try to Connect Again
      delay(5000);                                              // Delay for 5 Seconds
    }                                                           // End of Else
  }                                                             // End of While
}                                                               // End of Connect Function


/* ----------------------------------------------------------------------------------------- */
