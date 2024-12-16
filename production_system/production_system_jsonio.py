import queue
from production_system.prepared_session import PreparedSession
from utility.json_handler.json_handler import JsonHandler
from flask import Flask, request, jsonify
import threading
import requests
from typing import Optional, Dict


class ProductionSystemJSONIO:
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

        # Queue to store received labels
        self.ps_queue = queue.Queue()

        # Lock and condition for blocking behavior
        self.message_condition = threading.Condition()

        # Define a route to receive messages
        @self.app.route('/ProductionSystem', methods=['POST'])
        def receive_prepared_session():
            prep_sess_json = request.get_json()

            prepared_session = PreparedSession(uuid= prep_sess_json['uuid'], features=prep_sess_json['features'])

            self.ps_queue.put(prepared_session)
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
            return message



    def send_label(self, label, destinatario):
        """
            method to send label to
        """








    def send_configuration(self, config):
        """

        """

    def receive_classifier(self):
        """
        Receive a classifier from Development System

        Returns:
            the received classifier

        """