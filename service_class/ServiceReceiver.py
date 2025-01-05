"""
Author: Giovanni Ligato
"""

import time
import json
import queue
import threading
import jsonschema
from flask import Flask, request, jsonify

from service_class.ServiceClassParameters import ServiceClassParameters


class ServiceReceiver:
    """
    Service Class module responsible for the reception of timestamps, configuration messages and labels.

    """

    def __init__(self, host: str = '0.0.0.0', port: int = None, basedir: str = "."):
        """
        Initialize the Flask communication server.

        :param host: The host address for the Flask server.
        :param port: The port number for the Flask server.
        :param basedir: The base directory for the Flask server.
        """

        if port is None:
            port = ServiceClassParameters.LOCAL_PARAMETERS["Service Class"]["port"]

        self.app = Flask(__name__)
        self.host = host
        self.port = port

        # Queue to store received configuration messages
        self.configuration_queue = queue.Queue()

        # Queue to store received labels
        self.label_queue = queue.Queue()

        # Path of the JSON schema for the timestamp
        self.timestamp_schema_path = f"{basedir}/schemas/timestamp_schema.json"

        # Path of the JSON schema for the configuration
        self.configuration_schema_path = f"{basedir}/schemas/configuration_schema.json"

        # Path of the JSON schema for the label
        self.label_schema_path = f"{basedir}/schemas/label_schema.json"

        # Path of the timestamp log
        self.timestamp_log_path = f"{basedir}/log/timestamp_log.txt"

        # Define a route to receive timestamps
        @self.app.route('/Timestamp', methods=['POST'])
        def receive_timestamp():

            # Get the json timestamp from the request
            json_timestamp = request.get_json()

            # Validate the timestamp
            if self._validate_json(json_timestamp, self.timestamp_schema_path):
                # JSON timestamp is valid

                # Write the timestamp to the log
                with open(self.timestamp_log_path, "a") as log_file:
                    log_file.write(f"{json_timestamp['timestamp']},{json_timestamp["system_name"]},{json_timestamp["status"]}\n")

                return jsonify({"status": "received"}), 200

            else:
                # JSON timestamp is invalid
                return jsonify({"status": "error", "message": "Invalid JSON timestamp"}), 400

        # Define a route to receive configuration messages
        @self.app.route('/MessagingSystem', methods=['POST'])
        def receive_configuration():

            # Get the json configuration from the request
            json_configuration = request.get_json()

            # Validate the configuration
            if self._validate_json(json_configuration, self.configuration_schema_path):
                # JSON configuration is valid

                print(f"Received configuration: {json_configuration}")

                with open(self.timestamp_log_path, "a") as log_file:
                    log_file.write(f"{time.time()},Service Class,{json_configuration['configuration']}\n")

                # Add the configuration to the queue
                self.configuration_queue.put(json_configuration)

                return jsonify({"status": "received"}), 200

            return jsonify({"status": "error", "message": "Invalid JSON configuration"}), 400

        # Define a route to receive labels from the Production System
        @self.app.route('/ClientSide', methods=['POST'])
        def receive_label():

            # Get the json label from the request
            json_label = request.get_json()

            # Validate the label
            if self._validate_json(json_label, self.label_schema_path):
                # JSON label is valid

                print(f"Received label: {json_label}")

                # Add the label to the queue
                self.label_queue.put(json_label)

                return jsonify({"status": "received"}), 200

            else:
                # JSON label is invalid
                return jsonify({"status": "error", "message": "Invalid JSON label"}), 400

    def start_server(self):
        """
        Start the Flask server in a separate thread.
        """

        # Writing the start time in the log
        with open(self.timestamp_log_path, "a") as log_file:
            log_file.write(f"{time.time()},Service Class,start\n")

        thread = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port}, daemon=True)
        thread.start()

    def get_label(self) -> dict:
        """
        Get last label from the queue.

        :return: The last label received.
        """

        return self.label_queue.get(block=True)

    def get_configuration(self) -> dict:
        """
        Get last configuration from the queue.

        :return: The last configuration received.
        """

        return self.configuration_queue.get(block=True)

    def _validate_json(self, json_data: dict, schema_path: str) -> bool:
        """
        Validate a JSON object against a JSON schema.

        :param json_data: The JSON object to validate.
        :param schema_path: The path of the JSON schema to use for validation.
        :return: True if the JSON object is valid, False otherwise.
        """

        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        try:
            jsonschema.validate(json_data, schema)
            return True
        except jsonschema.ValidationError as e:
            print(f"Invalid JSON data: {e}")
            return

