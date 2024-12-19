from production_system.configuration_parameters import ConfigurationParameters
from flask import Flask, request, jsonify
import threading
import requests
from typing import Optional, Dict


class ProductionSystemIO:
    """

        this class manage all sended/received json file
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
        with self.message_condition:
            # Wait until a message is received
            while self.last_message is None:
                self.message_condition.wait()

            # Retrieve and clear the last message
            message = self.last_message
            self.last_message = None

            sender_ip = message['ip']
            # if the sender is the Develop system then I have received the classifier
            if sender_ip == ConfigurationParameters.DEVELOP_SYSTEM_IP:
                sender = "Develop"

            # if the sender is the Preparation system then I have received the classifier
            elif sender_ip == ConfigurationParameters.PREPARATION_SYSTEM_IP:
                sender = "Preparation"

            return sender, message



