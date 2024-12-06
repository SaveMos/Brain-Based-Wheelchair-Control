from flask import Flask, request, jsonify
from threading import Thread
import requests
from typing import Dict

class MessageBroker:
    """
    A class to facilitate message exchange between Python systems on the same network using Flask.

    Attributes:
        ip_address (str): The IP address of the local host.
        port (int): The port number for the Flask server.
    """

    def __init__(self, ip_address: str, port: int) -> None:
        """
        Initializes the MessageBroker with the given IP address and port.

        Args:
            ip_address (str): The IP address of the local host.
            port (int): The port number for the Flask server.
        """
        self.ip_address = ip_address
        self.port = port
        self.app = Flask(__name__)

        # Set up Flask route for receiving messages
        @self.app.route('/receive_message', methods=['POST'])
        def receive_message() -> Dict[str, str]:
            """
            Flask route to handle incoming messages.

            Returns:
                dict: A dictionary containing the sender's address and the received message.
            """
            data = request.json
            sender = request.remote_addr
            message = data.get("message", "")
            return jsonify({'sender': sender, 'message': message})

    def start_server(self) -> None:
        """
        Starts the Flask server in a separate thread.
        """
        server_thread = Thread(target=self.app.run, kwargs={
            'host': self.ip_address,
            'port': self.port,
            'debug': False,
            'use_reloader': False
        })
        server_thread.daemon = True
        server_thread.start()

    def send_message(self, target_ip: str, target_port: int, message: str) -> Dict[str, str]:
        """
        Sends a message to the target host via HTTP POST.

        Args:
            target_ip (str): The IP address of the recipient.
            target_port (int): The port number of the recipient.
            message (str): The message to send.

        Returns:
            dict: The response from the recipient.
        """
        url = f"http://{target_ip}:{target_port}/receive_message"
        payload = {'message': message}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            return {'error': str(error)}
