from flask import Flask, request, jsonify
import requests
import threading

class MessageBroker:
    """A message broker implemented using Flask for sending and receiving messages."""

    def __init__(self):
        """Initialize the Flask app and the message storage."""
        self.app = Flask(__name__)
        self.message = None  # Store the last received message

        # Define a route for receiving messages
        @self.app.route('/receive', methods=['POST'])
        def receive_message():
            """Handle receiving messages via POST requests."""
            data = request.get_json()
            sender_ip = request.remote_addr
            self.message = {
                'sender': sender_ip,
                'content': data.get('message')
            }
            return jsonify({'status': 'Message received', 'message': self.message}), 200

        # Define a route for retrieving the last received message
        @self.app.route('/receiveMessage', methods=['GET'])
        def get_message():
            """Retrieve the last received message."""
            if not self.message:
                return jsonify({'error': 'No messages received yet'}), 404
            return jsonify(self.message), 200

    def sendMessage(self, ip, port, message):
        """Send a message to a given IP and port.

        Args:
            ip (str): The recipient's IP address.
            port (int): The recipient's port number.
            message (str): The message to send.

        Returns:
            dict: The response from the recipient.
        """
        url = f'http://{ip}:{port}/receive'
        payload = {'message': message}
        response = requests.post(url, json=payload)
        return response.json()

    def receiveMessage(self, ip, port):
        """Retrieve the latest received message from another system.

        Args:
            ip (str): The sender's IP address.
            port (int): The sender's port number.

        Returns:
            dict: The message content and sender details.
        """
        url = f'http://{ip}:{port}/receiveMessage'
        response = requests.get(url)
        return response.json()

    def start_server(self, port):
        """Start the Flask server in a separate thread.

        Args:
            port (int): The port number to run the server on.
        """
        threading.Thread(target=self.app.run, kwargs={'port': port, 'debug': False}).start()

# Example usage
if __name__ == '__main__':
    # Create two message brokers for two systems
    development_system = MessageBroker()
    ingestion_system = MessageBroker()

    # Start servers on different ports
    development_system.start_server(port=5001)
    ingestion_system.start_server(port=5002)

    # Let the servers initialize (you may need to add a short delay in real cases)
    import time
    time.sleep(1)

    # Send a message from development_system to ingestion_system
    response = development_system.sendMessage('127.0.0.1', 5002, 'Hello from Development System!')
    print('Response from development system:', response)

    # Send a message from ingestion_system to development_system
    response = ingestion_system.sendMessage('127.0.0.1', 5001, 'Hello from Ingestion System!')
    print('Response from ingestion system:', response)

    # Retrieve messages on both systems
    print('Message received by development system:',
          development_system.receiveMessage('127.0.0.1', 5001))
    print('Message received by ingestion system:',
          ingestion_system.receiveMessage('127.0.0.1', 5002))
