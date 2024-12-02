
### Sections in the `README.md`:
# Winter Supplement Calculator Rules Engine

## Project Overview
This project implements a **Rules Engine** for calculating the winter supplement based on predefined eligibility and calculation rules. It communicates with the **Winter Supplement Web App** via MQTT to receive input data and return calculation results.

### Key Features:
- **Event-Driven Architecture**: The rules engine listens to MQTT topics to receive input data and publishes results to a corresponding topic.
- **Eligibility Determination**: The engine calculates eligibility based on predefined rules.
- **Supplement Calculation**: Calculates the base amount and additional amounts for children, returning the total supplement amount.
- **MQTT Integration**: Uses MQTT protocol to communicate with the Winter Supplement Web App for input and output data exchange.

## Prerequisites

The following Python libraries are required to run the project:

paho-mqtt: For MQTT communication
unittest: For running unit tests

### Python Version
This project requires Python 3.x (preferably 3.12.7 or higher). You can check the version by running:
```bash
python --version3. **Setup**: Instructions to clone the repo, install dependencies, and configure the project.

4. **Running the Rules Engine**: python run_engine.py
5. **Code Structure**:

mqtt_engine.py: The main script to run the rules engine. It handles MQTT communication, subscribing to topics, and publishing the results.
mqtt_engine.py: Contains the logic for calculating eligibility and supplement amounts based on input data.
tests.py: Contains unit tests for the rules engine functionality, including eligibility checks and supplement calculations.

6. **How to Test**: python -m unittest tests.py
7. **Example Input/Output**: 
Input : 
{
  "id": "789",
  "numberOfChildren": 2,
  "familyComposition": "couple",
  "familyUnitInPayForDecember": true
}

Output:

{
  "id": "789",
  "isEligible": true,
  "baseAmount": 120.0,
  "childrenAmount": 40.0,
  "supplementAmount": 160.0
}

8. **Troubleshooting**:

MQTT Connection Failures: Ensure your network allows connections to the broker test.mosquitto.org on port 1883.
Invalid Input Data: Ensure that the input data follows the correct schema

