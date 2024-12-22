from flask import Flask, request, jsonify
import threading
import requests
from typing import Optional, Dict

class DevelopmentSystemMessageBroker:
    """The messaging broker of the development system"""

    """
       A utility class to enable inter-module communication using Flask.

       This class supports sending and receiving messages in a blocking manner.
       """

    def __init__(self, host: str = '0.0.0.0', port: int = 5000):
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

            return jsonify("Development System: learning set received"), 200

    def start_server(self):
        """
        Start the Flask server in a separate thread.
        """
        thread = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port}, daemon=True)
        thread.start()

    def send_classifier(self, target_ip: str, target_port: int, classifier_file: str) -> Optional[Dict]:
        """
        Send the winner classifier to the target module production system.

        :param target_ip: The IP address of the target module.
        :param target_port: The port of the target module.
        :param classifier_file: The message to send (typically a JSON string).
        :return: The response from the target, if any.
        """

        with open(classifier_file, "rb") as f:
            file_content = f.read()
            message = file_content.decode('latin1')  # Encode binary content to a string format

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
        except (UnicodeDecodeError, IOError) as e:
            print(f"Error processing file: {e}")
        return None

    def send_configuration(self, target_ip: str, target_port: int) -> Optional[Dict]:
        """
        Send the configuration to the target module messaging system.

        :param target_ip: The IP address of the target module.
        :param target_port: The port of the target module.
        :return: The response from the target, if any.
        """

        restart_config = {"action": "restart"}

        url = f"http://{target_ip}:{target_port}/send"

        payload = {
            "port": self.port,
            "message": restart_config
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error sending message: {e}")

        return None

    def rcv_learning_set(self) -> Optional[Dict]:
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