import unittest
from unittest.mock import Mock, patch, call
import json
import mqtt_engine  # Assuming the file name is mqtt_engine.py


class TestMQTTRulesEngine(unittest.TestCase):

    @patch("mqtt_engine.mqtt.Client")
    def test_on_connect(self, mock_mqtt_client):
        userdata = {"subscribe_topic": "BRE/calculateWinterSupplementInput/test123"}
        mock_client = Mock()
        mqtt_engine.on_connect(mock_client, userdata, None, 0)

        mock_client.subscribe.assert_called_with(userdata["subscribe_topic"])
        print("Test: on_connect passed.")

    def test_process_input_eligible_single(self):
        input_data = {
            "id": "123",
            "numberOfChildren": 2,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        expected_output = {
            "id": "123",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 40.0,
            "supplementAmount": 100.0
        }

        result = mqtt_engine.process_input(input_data)
        self.assertEqual(result, expected_output)
        print("Test: process_input (eligible, single) passed.")

    def test_process_input_eligible_couple(self):
        input_data = {
            "id": "456",
            "numberOfChildren": 1,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_output = {
            "id": "456",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 20.0,
            "supplementAmount": 140.0
        }

        result = mqtt_engine.process_input(input_data)
        self.assertEqual(result, expected_output)
        print("Test: process_input (eligible, couple) passed.")

  

    @patch("mqtt_engine.mqtt.Client")
    def test_on_message(self, mock_mqtt_client):
        # Mock client and userdata
        mock_client = Mock()
        userdata = {
            "publish_topic": "BRE/calculateWinterSupplementOutput/test123"
        }
        mock_msg = Mock()
        mock_msg.payload = json.dumps({
            "id": "test-id",
            "numberOfChildren": 2,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }).encode()

        with patch("mqtt_engine.process_input", return_value={
            "id": "test-id",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 40.0,
            "supplementAmount": 100.0
        }):
            mqtt_engine.on_message(mock_client, userdata, mock_msg)

        mock_client.publish.assert_called_once_with(
            "BRE/calculateWinterSupplementOutput/test123",
            json.dumps({
                "id": "test-id",
                "isEligible": True,
                "baseAmount": 60.0,
                "childrenAmount": 40.0,
                "supplementAmount": 100.0
            }),
            qos=1,
            retain=True
        )
        print("Test: on_message passed.")

   

if __name__ == "__main__":
    unittest.main()
