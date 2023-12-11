""" This file is use to define a set of conditions and the corresponding results 
   to those conditions. This is like the dictionary or set of rules of the Code """

[
    # First condition block: If the potentiometer value is giving greater than 200

    {
        "conditions": [

            {
                "topic": "terra/hum",     # Specify the topic for the potentiometer
                "comparison": ">",        # Set the comparison operator to greater than
                "value": 200              # Set the threshold value to 200
            }

        ],

        # Execute this result: Turn the LED on

        "results": [

            {
                "topic": "terra/led",     # Specify the topic for the LED
                "value": "on"             # Set the value to turn the LED on
            }
        ]

    },


    # Second condition block: If potentiometer value is less than 200

    {
        "conditions": [

            {
                "topic": "terra/hum",     # Specify the topic for the potentiometer
                "comparison": "<",        # Set the comparison operator to less than
                "value": 200              # Set the threshold value to 200
            }

        ],

        # Execute this result: Turn the LED off

        "results": [
            {
                "topic": "terra/led",    # Specify the topic for the LED
                "value": "off"           # Set the value to turn the LED off
            }
        ]
    }
]
