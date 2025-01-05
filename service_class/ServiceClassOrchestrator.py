"""
Author: Giovanni Ligato
"""

import time

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


        if ServiceClassParameters.LOCAL_PARAMETERS["phase"] == "all_phases":
            print("All phases will be tested.")
            print("For each phase, the following sessions will be sent:")
            print(" Development: " + str(ServiceClassParameters.LOCAL_PARAMETERS["development_sessions"]))
            print(" Production: " + str(ServiceClassParameters.LOCAL_PARAMETERS["production_sessions"]))
            print(" Evaluation: " + str(ServiceClassParameters.LOCAL_PARAMETERS["evaluation_sessions"]))

            # Writing headers to the CSV file
            with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "w") as f:
                f.write("phase,timestamp,status\n")

            # Dictionary to store the phases and a boolean value to indicate if the labels should be sent
            phases_and_labels = {
                "development": True,
                "production": False,
                "evaluation": True
            }

            for phase, include_labels in phases_and_labels.items():
                # Preparing the bucket for the phase
                bucket = self.recordSender.prepare_bucket(ServiceClassParameters.LOCAL_PARAMETERS[f"{phase}_sessions"], include_labels)

                # Updating CSV file with the phase
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{phase}," + str(time.time()) + ",start\n")

                # Sending the bucket
                self.recordSender.send_bucket(bucket)

                # Updating CSV file
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{phase}," + str(time.time()) + ",records_sent\n")

                if phase == "development":
                    # Waiting for the production configuration message
                    configuration = self.serviceReceiver.get_configuration()

                    # Updating CSV file
                    with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                        f.write(f"{phase}," + str(time.time()) + f",{configuration['configuration']}\n")

                    if configuration["configuration"] == "restart":
                        # Restart the development phase
                        print("Restart configuration received.")
                        return

                else:
                    # Waiting for the labels
                    for _ in range(ServiceClassParameters.LOCAL_PARAMETERS[f"{phase}_sessions"]):
                        label = self.serviceReceiver.get_label()

                    # Updating CSV file
                    with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                        f.write(f"{phase}," + str(time.time()) + ",labels_received\n")


                print(f"{phase.capitalize()} phase completed.")

            print("All phases completed.")

        elif ServiceClassParameters.LOCAL_PARAMETERS["phase"] == "development":
            print("Development phase will be tested, by developing " + str(ServiceClassParameters.LOCAL_PARAMETERS["classifiers_to_develop"]) + " classifiers.")

            # Writing headers to the CSV file
            with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "w") as f:
                f.write("developed_classifier,timestamp,status\n")

            for i in range(1, ServiceClassParameters.LOCAL_PARAMETERS["classifiers_to_develop"]+1):

                # Preparing the bucket for the development
                bucket = self.recordSender.prepare_bucket(ServiceClassParameters.LOCAL_PARAMETERS["development_sessions"], include_labels=True)

                # Updating CSV file with the classifier
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{i}," + str(time.time()) + ",start\n")

                # Sending the bucket
                self.recordSender.send_bucket(bucket)

                # Updating CSV file
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{i}," + str(time.time()) + ",records_sent\n")

                # Waiting for the production configuration message
                configuration = self.serviceReceiver.get_configuration()

                # Updating CSV file
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{i}," + str(time.time()) + f",{configuration['configuration']}\n")

                if configuration["configuration"] == "restart":
                    # Restart the development phase
                    print("Restart configuration received.")
                    return

        elif ServiceClassParameters.LOCAL_PARAMETERS["phase"] == "production":
            print("Production phase will be tested, by considering " + str(ServiceClassParameters.LOCAL_PARAMETERS["production_sessions"]) + " sessions.")

            # Writing headers to the CSV file
            with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "w") as f:
                f.write("sessions,timestamp,status\n")

            for i in range(1, ServiceClassParameters.LOCAL_PARAMETERS["production_sessions"]+1):

                # Preparing the bucket for the production
                bucket = self.recordSender.prepare_bucket(i, include_labels=False)

                # Updating CSV file with the session
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{i}," + str(time.time()) + ",start\n")

                # Sending the bucket
                self.recordSender.send_bucket(bucket)

                # Updating CSV file
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{i}," + str(time.time()) + ",records_sent\n")


                for _ in range(i):
                    label = self.serviceReceiver.get_label()

                # Updating CSV file
                with open(f"{self.basedir}/log/{ServiceClassParameters.LOCAL_PARAMETERS["phase"]}_log.csv", "a") as f:
                    f.write(f"{i}," + str(time.time()) + ",labels_received\n")

                print(f"Production phase {i} completed.")

            print("Production phase completed.")

        else:
            print("Invalid value for the phase parameter.")
            print("Please, choose between 'all_phases', 'development' or 'production'.")
            return

        print("Service Class stopped.")


if __name__ == "__main__":

    service_class_orchestrator = ServiceClassOrchestrator()

    # Start the Service Class Orchestrator
    service_class_orchestrator.start()