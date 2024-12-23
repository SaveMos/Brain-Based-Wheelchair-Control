import random
import time
from evaluation_system.EvaluationSystemParameters import EvaluationSystemParameters
from evaluation_system.LabelsBuffer import LabelsBuffer
from evaluation_system.LabelReceiver_and_ConfigurationSender import LabelReceiver_and_ConfigurationSender
import json
import jsonschema
from evaluation_system.EvaluationReportView import EvaluationReportView
import os

class EvaluationSystemOrchestrator:
    """
    This class is responsible for orchestrating the Evaluation System.
    """

    def __init__(self, basedir: str = "."):
        """
        Initialize the Evaluation System Orchestrator.

        :param basedir: Base directory of the Evaluation System.
        """

        self.basedir = basedir

        EvaluationSystemParameters.loadParameters(self.basedir)
        self.testing = EvaluationSystemParameters.TESTING

        self.labels_buffer = LabelsBuffer()
        self.labelReceiver_and_configurationSender = LabelReceiver_and_ConfigurationSender(basedir=self.basedir)
        self.evaluation_report_view = EvaluationReportView(self.basedir)



    def _get_classifier_evaluation(self) -> (bool, dict or None):
        """
        Retrieve the classifier evaluation given by the Human Operator.

        :return: False + None if the file containing the classifier evaluation does not exist yet.
                 True + dict otherwise.
        """

        try:
            with open(f"{self.basedir}/human_operator_workspace/classifier_evaluation.json", "r") as f:
                # The file exists. Now we need to check the content.
                data = json.load(f)

                # Validating the JSON content
                with open(f"{self.basedir}/classifier_evaluation_schema.json", "r") as schema_file:
                    schema = json.load(schema_file)
                    jsonschema.validate(data, schema)

                return True, data
        except:
            return False, None



    def Evaluate(self):
        """
        Main method of the Evaluation System Orchestrator.
        """

        print("Evaluation System Orchestrator started.")

        self.labelReceiver_and_configurationSender.start_server()

        while True:
            classifier_evaluation_exists, classifier_evaluation = self._get_classifier_evaluation()

            print(f"Classifier evaluation exists: {classifier_evaluation_exists}")

            if not classifier_evaluation_exists:
                # Evaluation Report has not been created yet.

                while True:
                    label = self.labelReceiver_and_configurationSender.get_label()
                    if self.testing:
                        self.labelReceiver_and_configurationSender.send_timestamp(time.time(), "start")

                    self.labels_buffer.save_label(label)
                    print(f"Label saved: {label.to_dict()}")

                    if self.labels_buffer.get_num_classifier_labels() >= EvaluationSystemParameters.MINIMUM_NUMBER_LABELS and \
                       self.labels_buffer.get_num_expert_labels() >= EvaluationSystemParameters.MINIMUM_NUMBER_LABELS:

                        print("Sufficient number of labels.")
                        break
                    elif self.testing:
                        self.labelReceiver_and_configurationSender.send_timestamp(time.time(), "end")

                # Get all the stored labels
                classifier_labels = self.labels_buffer.get_classifier_labels(EvaluationSystemParameters.MINIMUM_NUMBER_LABELS)
                expert_labels = self.labels_buffer.get_expert_labels(EvaluationSystemParameters.MINIMUM_NUMBER_LABELS)

                # Create the evaluation report
                self.evaluation_report_view.create_evaluation_report(classifier_labels, expert_labels,
                                                                     EvaluationSystemParameters.TOTAL_ERRORS,
                                                                     EvaluationSystemParameters.MAX_CONSECUTIVE_ERRORS)

                # Remove the labels
                self.labels_buffer.delete_labels(EvaluationSystemParameters.MINIMUM_NUMBER_LABELS)
                print("Labels removed.")

                if not self.testing:
                    return

                print("Testing mode, classifier evaluation automatically generated.")

                # Testing mode, evaluation automatically generated
                random_evaluation = int(random.random() <= 0.3) # 30% chance of being good
                if random_evaluation == 1:
                    # Good classifier
                    print("Good classifier.")
                    self.labelReceiver_and_configurationSender.send_timestamp(time.time(), "end")
                else:
                    # Bad classifier
                    print("Bad classifier.")
                    self.labelReceiver_and_configurationSender.send_timestamp(time.time(), "end")
                    self.labelReceiver_and_configurationSender.send_configuration()
                    print("Configuration sent.")

                return

            else:
                # Evaluation Report has been created.
                # Check if the classifier has been evaluated by the Human Operator.
                if classifier_evaluation["classifier_evaluation"] == "waiting_for_evaluation":
                    # Human Operator has not evaluated the classifier yet.
                    print("Human Operator has not evaluated the classifier yet.")
                    return

                if classifier_evaluation["classifier_evaluation"] == "good":
                    # Human Operator evaluated the classifier as good.
                    print("Human Operator evaluated the classifier as good.")
                    if self.testing:
                        self.labelReceiver_and_configurationSender.send_timestamp(time.time(), "end")
                elif classifier_evaluation["classifier_evaluation"] == "bad":
                    # Human Operator evaluated the classifier as bad.
                    print("Human Operator evaluated the classifier as bad.")
                    if self.testing:
                        self.labelReceiver_and_configurationSender.send_timestamp(time.time(), "end")
                    self.labelReceiver_and_configurationSender.send_configuration()
                    print("Configuration sent.")

                # Remove the classifier_evaluation.json file to start a new evaluation
                os.remove(f"{self.basedir}/human_operator_workspace/classifier_evaluation.json")

                return