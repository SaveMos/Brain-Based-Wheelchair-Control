"""
Author: Giovanni Ligato
"""
from traceback import print_tb

from service_class.ServiceClassParameters import ServiceClassParameters
from service_class.ServiceReceiver import ServiceReceiver
from service_class.RecordSender import RecordSender

class ServiceClassOrchestrator:
    """
    Service Class Orchestrator module responsible for managing the Service Class.
    """


    def __init__(self, basedir: str = "."):
        """
        Initialize the Service Class Orchestrator.

        :param basedir: The base directory for the Service Class Orchestrator.
        """

        self.basedir = basedir

        # Load the parameters of the Service Class
        ServiceClassParameters.loadParameters(self.basedir)

        self.serviceReceiver = ServiceReceiver(basedir=self.basedir)

        self.recordSender = RecordSender(basedir=self.basedir)


    def start(self):
        """
        Start the Service Class Orchestrator.
        """

        print("Service Class started.")

        # Start the Service Receiver server
        self.serviceReceiver.start_server()

        if ServiceClassParameters.DEVELOPMENT_PHASE:
            # Send development sessions
            for _ in range(ServiceClassParameters.DEVELOPMENT_SESSIONS):
                self.recordSender.send_session()
        else:
            # Send production amd evaluation sessions
            for _ in range(ServiceClassParameters.PRODUCTION_SESSIONS):
                self.recordSender.send_session()
            for _ in range(ServiceClassParameters.EVALUATION_SESSIONS):
                self.recordSender.send_session()


        print("Sessions sent.")

        # Keeping the main thread alive until the user wants to exit
        # In this way the Service Receiver server will keep running
        input("Press 'q' and Enter to exit...\n")

        print("Service Class stopped.")


if __name__ == "__main__":

    service_class_orchestrator = ServiceClassOrchestrator()

    # Start the Service Class Orchestrator
    service_class_orchestrator.start()