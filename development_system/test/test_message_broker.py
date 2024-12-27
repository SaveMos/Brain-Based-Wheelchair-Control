import threading
import requests
from flask import Flask, request, jsonify
from typing import Optional, Dict

from development_system.development_system_message_broker import DevelopmentSystemMessageBroker


def test_send_classifier():
    """Test the send_classifier method."""
    broker = DevelopmentSystemMessageBroker()
    broker.start_server()

    # Create a mock classifier file
    classifier_file = "mock_classifier.json"
    with open(classifier_file, "w") as file:
        file.write("{\"classifier\": \"MockClassifier\"}")

    # Simulate sending the classifier to the broker
    response = broker.send_classifier("127.0.0.1", broker.port, classifier_file)

    assert response == "Development System: learning set received", "send_classifier test failed."
    print("send_classifier test passed.")

def test_send_configuration():
    """Test the send_configuration method."""
    broker = DevelopmentSystemMessageBroker()
    broker.start_server()

    # Simulate sending a configuration
    response = broker.send_configuration("127.0.0.1", broker.port)

    assert response == "Development System: learning set received", "send_configuration test failed."
    print("send_configuration test passed.")

def test_rcv_learning_set():
    """Test the rcv_learning_set method."""
    broker = DevelopmentSystemMessageBroker()
    broker.start_server()

    # Simulate a client sending a message
    def simulate_client():
        url = f"http://127.0.0.1:{broker.port}/send"
        payload = {"port": 12345, "message": "Mock Learning Set"}
        requests.post(url, json=payload)

    threading.Thread(target=simulate_client, daemon=True).start()

    # Receive the message using the broker
    message = broker.rcv_learning_set()

    assert message == {
        "ip": "127.0.0.1",
        "port": 12345,
        "message": "Mock Learning Set"
    }, "rcv_learning_set test failed."
    print("rcv_learning_set test passed.")

# Run tests
if __name__ == "__main__":
    test_send_classifier()
    test_send_configuration()
    test_rcv_learning_set()
