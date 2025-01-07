"""
    Class for managing the sending and receiving of messages
"""

import threading
import requests
import json
from flask import Flask, request, jsonify
from typing import Optional, Dict
from production_system.label import Label
from production_system.configuration_parameters import ConfigurationParameters


class ProductionSystemIO:
    """

        this class manage all sent/received json file
    """

    def __init__(self, host: str = '0.0.0.0', port: int = 5005):
        """
        Initialize the Flask communication server.

        :param host: The host address for the Flask server.
        :param port: The port number for the Flask server.
        """
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.last_message = None

        # Lock and condition for blocking behavior
        self.message_condition = threading.Condition()

        # Define a route to receive messages
        @self.app.route('/send', methods=['POST'])
        def receive_message():
            data = request.json
            sender_ip = request.remote_addr
            sender_port = data.get('port')
            message = data.get('message')


            with self.message_condition:
                self.last_message = {
                    'ip': sender_ip,
                    'port': sender_port,
                    'message': message
                }
                # Notify any threads waiting for a message
                self.message_condition.notify_all()

            return jsonify({"status": "received"}), 200

    def start_server(self):
        """
        Start the Flask server in a separate thread.
        """
        thread = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port}, daemon=True)
        thread.start()

    def send_configuration(self) -> Optional[Dict]:
        """
        Send start configuration to messaging system.

        :return: The response from the target, if any.
        """

        # recover messaging system information
        configuration = ConfigurationParameters()
        message = configuration.start_config()
        msg_sys_ip = configuration.global_netconf['Messaging System']['ip']
        msg_sys_port = configuration.global_netconf['Messaging System']['port']
        url = f"http://{msg_sys_ip}:{msg_sys_port}/send"
        payload = {
            "port": self.port,
            "message": message
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error sending message: {e}")
        return None

    def send_label(self, target_ip: str, target_port: int, label: [Dict]) -> Optional[Dict]:
        """
        Send a message to a target module.

        :param target_ip: The IP address of the target module.
        :param target_port: The port of the target module.
        :param label: The label to send.
        :return: The response from the target, if any.
        """

        # convert label into json
        label_dict = label.to_dictionary()

        label_json = json.dumps(label_dict)
        url = f"http://{target_ip}:{target_port}/send"
        payload = {
            "port": self.port,
            "message": label_json
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error sending message: {e}")
        return None

    def get_last_message(self) -> Optional[Dict]:
        """
       Wait for a message to be received and return it.

        :return: A dictionary containing the sender's IP, port, and the message content.
        """
        with self.message_condition:
            # Wait until a message is received
            while self.last_message is None:
                self.message_condition.wait()

            # Retrieve and clear the last message
            message = self.last_message
            self.last_message = None


            return message

    # Testing method
    def send_timestamp(self, timestamp: float, status: str) -> bool:
        """
        Send the timestamp to the Service Class.

        :param timestamp: The timestamp to send.
        :param status: The status of the timestamp
        :return: True if the timestamp was sent successfully, False otherwise.
        """

        configuration = ConfigurationParameters()
        url = f"http://{configuration.global_netconf['Service Class']['ip']}:\
                          {configuration.global_netconf['Service Class']['port']}/Timestamp"

        timestamp_message = {
            "timestamp": timestamp,
            "system_name": "Evaluation System",
            "status": status
        }

        try:
            response = requests.post(url, json=timestamp_message)
            if response.status_code == 200:
                return True
        except requests.RequestException as e:
            print(f"Error sending timestamp: {e}")
        return False
