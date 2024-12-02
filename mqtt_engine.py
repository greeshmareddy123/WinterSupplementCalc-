import json

import paho.mqtt.client as mqtt



# MQTT Broker Details

BROKER = "test.mosquitto.org"

PORT = 1883



def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to MQTT Broker!")

        client.subscribe(userdata["subscribe_topic"])

        print(f"Subscribed to topic: {userdata['subscribe_topic']}")

    else:

        print(f"Failed to connect, return code {rc}")



def on_message(client, userdata, msg):

    try:

        # Decode and process input

        input_data = json.loads(msg.payload.decode())

        print(f"Received Input: {input_data}")



        # Check the "In Pay December" checkbox

        if not input_data.get("familyUnitInPayForDecember", False):

            # Publish ineligible output if checkbox is not selected

            output_data = {

                "id": input_data.get("id"),

                "isEligible": False,

                "baseAmount": 0.0,

                "childrenAmount": 0.0,

                "supplementAmount": 0.0,

            }

            print(f"Publishing Output for Ineligible Client: {output_data}")

        else:

            # Process eligible input

            output_data = process_input(input_data)

            print(f"Publishing Output for Eligible Client: {output_data}")



        # Publish the output data

        output_topic = userdata["publish_topic"]

        client.publish(output_topic, json.dumps(output_data), qos=1, retain=True)



    except Exception as e:

        print(f"Error in on_message: {e}")



def process_input(input_data):

    try:

        id = input_data.get("id")

        number_of_children = input_data.get("numberOfChildren", 0)

        family_composition = input_data.get("familyComposition", "single")



        # Base amount calculation based on family composition

        if family_composition == "single":

            base_amount = 60.0

        elif family_composition == "couple":

            base_amount = 120.0

        else:

            base_amount = 0.0



        # Additional amount for children

        children_amount = 20.0 * number_of_children



        # Total supplement amount

        supplement_amount = base_amount + children_amount



        return {

            "id": id,

            "isEligible": True,

            "baseAmount": base_amount,

            "childrenAmount": children_amount,

            "supplementAmount": supplement_amount

        }

    except Exception as e:

        print(f"Error in processing input: {e}")

        return {}



def run_engine():

    try:

        mqtt_topic_id = input("Enter the MQTT Topic ID: ").strip()



        # Define subscription and publishing topics

        subscribe_topic = f"BRE/calculateWinterSupplementInput/{mqtt_topic_id}"

        publish_topic = f"BRE/calculateWinterSupplementOutput/{mqtt_topic_id}"



        # MQTT client setup

        client = mqtt.Client(userdata={"subscribe_topic": subscribe_topic, "publish_topic": publish_topic})

        client.on_connect = on_connect

        client.on_message = on_message



        print("Connecting to MQTT Broker...")

        client.connect(BROKER, PORT, 60)



        print(f"Subscribing to topic: {subscribe_topic}")

        print(f"Publishing to topic: {publish_topic}")



        client.loop_forever()

    except Exception as e:

        print(f"Error in run_engine: {e}")



if __name__ == "__main__":

    run_engine()

