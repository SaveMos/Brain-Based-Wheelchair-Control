import queue
import threading
from typing import Optional, Dict

import requests
from flask import Flask, request, jsonify

from segregation_system.segregation_system_parameters import SegregationSystemConfiguration


class SessionReceiverAndConfigurationSender:
    """
    A utility class to enable inter-module communication using Flask.

    This class supports sending and receiving messages in a blocking manner.
    """

    def __init__(self, host: str = '0.0.0.0', port: int = 5003):
        """
        Initialize the Flask communication server.

        :param host: The host address for the Flask server.
        :param port: The port number for the Flask server.
        """
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.last_message = None
        self.queue = queue.Queue()

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
                self.queue.put(self.last_message)
                # Notify any threads waiting for a message
                self.message_condition.notify_all()

            return jsonify({"status": "received"}), 200

    def start_server(self):
        """
        Start the Flask server in a separate thread.
        """
        thread = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port}, daemon=True)
        thread.start()

    def send_message(self, target_ip: str, target_port: int, message: str) -> Optional[Dict]:
        """
        Send a message to a target module.

        :param target_ip: The IP address of the target module.
        :param target_port: The port of the target module.
        :param message: The message to send (typically a JSON string).
        :return: The response from the target, if any.
        """
        url = f"http://{target_ip}:{target_port}/send"
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

    def get_last_message(self) -> Optional[Dict]:
        """
       Wait for a message to be received and return it.

        :return: A dictionary containing the sender's IP, port, and the message content.
        """
        return self.queue.get(block=True)


    def send_configuration(self) -> bool:
        """
        Send the configuration "restart" message to the Messaging System.

        :return: True if the message was sent successfully, False otherwise.
        """

        network_info = SegregationSystemConfiguration.GLOBAL_PARAMETERS["Messaging System"]

        url = f"http://{network_info.get('ip')}:\
              {network_info.get('port')}/MessagingSystem"

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

    # Testing method
    def send_timestamp(self, timestamp: float, status: str) -> bool:
        """
        Send the timestamp to the Service Class.

        :param timestamp: The timestamp to send.
        :param status: The status of the timestamp
        :return: True if the timestamp was sent successfully, False otherwise.
        """
        network_info = SegregationSystemConfiguration.GLOBAL_PARAMETERS["Service Class"]

        url = f"http://{network_info.get('ip')}:\
                      {network_info.get('port')}/Timestamp"

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
