from development_system.configuration_parameters import ConfigurationParameters
from development_system.jsonIO import JsonHandler
from development_system.development_system_message_broker import DevelopmentSystemMessageBroker


class DevelopmentSystemOrchestrator:
    """Orchestrates the development system process."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.testing = None
        self.develop = None
        self.config_params = ConfigurationParameters() #instance of ConfigurationParameters class
        #self.dev_mess_broker = DevelopmentSystemMessageBroker()  # instance of DevelopmentSystemMessageBroker class

    def set_testing(self, value):
        """Set the minimum number of layers."""
        self.testing = value

    def get_testing(self):
        """Get the minimum number of layers."""
        return self.testing

    def develop(self):
        """Handle development logic."""
        pass  # Logic for development.

if __name__ == "__main__":
    orchestrator = DevelopmentSystemOrchestrator()

    # Load configurations directly from ConfigurationParameters
    orchestrator.config_params.load_configuration()
    # Test the access to loaded configuration parameters
    #print("Min Layers:", orchestrator.config_params.min_layers)


    # Create a MessageBroker instance and start the server
    #dev_mess_broker = DevelopmentSystemMessageBroker(host='0.0.0.0', port=5002)
    #dev_mess_broker.start_server()

    #message = dev_mess_broker.rcv_learning_set()
    #if message:
        #print("Message received:", message)

    #Simulation of the reception of the learning set, to change in future
    json_handler = JsonHandler()
    with open("dataset_split.json", 'r') as f:
        json_content = f.read()

    learning_set =  json_handler.create_learning_set_from_json(json_content)

    #Read the responses of the user for the stop and go
    user_responses = json_handler.read_user_responses("responses/user_responses.json")
    print("ItertionOK: ", user_responses["IterationOK"])