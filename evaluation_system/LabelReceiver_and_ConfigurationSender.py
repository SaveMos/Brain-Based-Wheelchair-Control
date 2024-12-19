"""
Author: Giovanni Ligato
"""


from flask import Flask, request, jsonify
import threading
import requests
from typing import Optional, Dict
import queue
import jsonschema
from EvaluationSystemParameters import EvaluationSystemParameters
from Label import Label
import json


class LabelReceiver_and_ConfigurationSender:
    """
    Evaluation System module responsible for receiving labels and sending configuration.
    """

    def __init__(self, host: str = '0.0.0.0', port: int = 8006):
        """
        Initialize the Flask communication server.

        :param host: The host address for the Flask server.
        :param port: The port number for the Flask server.
        """
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        # Queue to store received labels
        self.label_queue = queue.Queue()

        # Path of the JSON schema for the labels
        self.label_schema_path = "schemas/label_schema.json"

        # Define a route to receive labels
        @self.app.route('/EvaluationSystem', methods=['POST'])
        def receive_label():

            # Get the sender's IP
            sender_ip = request.remote_addr

            # Get the label from the request
            json_label = request.get_json()

            # Validate the label
            if self._validate_json_label(json_label):
                # JSON label is valid

                # Check if the label is an expert label (coming from the Ingestion System)
                # or a classifier label (coming from the Production System)
                if EvaluationSystemParameters.INGESTION_SYSTEM_IP == sender_ip:
                    expert = True
                elif EvaluationSystemParameters.PRODUCTION_SYSTEM_IP == sender_ip:
                    expert = False
                else:
                    return jsonify({"status": "error", "message": "Invalid sender IP"}), 400

                # Create a Label object from the JSON label
                label = Label(uuid=json_label['uuid'], movements=json_label['movements'], expert=expert)
                self.label_queue.put(label)

                return jsonify({"status": "received"}), 200
            else:
                # JSON label is invalid
                return jsonify({"status": "error", "message": "Invalid JSON label"}), 400

    def start_server(self):
        """
        Start the Flask server in a separate thread.
        """
        thread = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port}, daemon=True)
        thread.start()

    def _validate_json_label(self, json_label: Dict) -> bool:
        """
        Validate a JSON label received from a sender.

        :param json_label: The JSON label to validate.
        """

        with open(self.label_schema_path, "r") as schema_file:
            label_schema = json.load(schema_file)

        try:
            jsonschema.validate(json_label, label_schema)
            return True
        except jsonschema.ValidationError as e:
            print(f"Invalid JSON label: {e}")
            return False

    def send_configuration(self) -> bool:
        """
        Send the configuration "restart" message to the Messaging System.

        :return: True if the message was sent successfully, False otherwise.
        """

        url = f"http://{EvaluationSystemParameters.MESSAGING_SYSTEM_IP}:\
              {EvaluationSystemParameters.MESSAGING_SYSTEM_PORT}/MessagingSystem"

        configuration = {
            "configuration": "restart"
        }

        try:
            response = requests.post(url, json=configuration)
            if response.status_code == 200:
                return True
        except requests.RequestException as e:
            print(f"Error sending configuration: {e}")
        return False


    def get_label(self) -> Optional[Label]:
        """
        Get the last label received by the server. Blocks until a label is available.

        :return: A Label object containing the UUID, movements, and expert fields.
        """
        return self.label_queue.get(block=True)


    # Testing method
    def send_timestamp(self, timestamp: int, phase: str) -> bool:
        """
        Send the timestamp to the Messaging System.

        :param timestamp: The timestamp to send.
        :param phase: The phase of the timestamp
        :return: True if the timestamp was sent successfully, False otherwise.
        """
        url = f"http://{EvaluationSystemParameters.TESTING_SYSTEM_IP}:\
              {EvaluationSystemParameters.TESTING_SYSTEM_PORT}/TestingSystem"

        timestamp_message = {
            "system": "Evaluation System",
            "timestamp": timestamp,
            "phase": phase
        }

        try:
            response = requests.post(url, json=timestamp_message)
            if response.status_code == 200:
                return True
        except requests.RequestException as e:
            print(f"Error sending timestamp: {e}")
        return False




if __name__ == "__main__":

    # Module A (Sender)
    from time import sleep

    # Create a MessageBroker instance and start the server
    module_a = MessageBroker(host='0.0.0.0', port=5001)
    module_a.start_server()

    # Send a message to Module B
    response = module_a.send_message(target_ip='127.0.0.1', target_port=5002, message='{"action": "test"}')
    print("Response from Module B:", response)

    # Keep the server running
    while True:
        sleep(1)

    ########################################################

    # Module B (Receiver)
    from time import sleep

    # Create a MessageBroker instance and start the server
    module_b = MessageBroker(host='0.0.0.0', port=5002)
    module_b.start_server()

    # Keep the server running and print messages received
    while True:
        message = module_b.get_last_message()
        if message:
            print("Message received:", message)
            # Reset last message to avoid printing repeatedly
            module_b.last_message = None
        sleep(1)


