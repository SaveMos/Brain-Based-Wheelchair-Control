import random
import time
from EvaluationSystemParameters import EvaluationSystemParameters
from LabelsBuffer import LabelsBuffer
from LabelReceiver_and_ConfigurationSender import LabelReceiver_and_ConfigurationSender
import json
import jsonschema
from Label import Label
from EvaluationReportView import EvaluationReportView

class EvaluationSystemOrchestrator:
    """
    This class is responsible for orchestrating the Evaluation System.
    """

    def __init__(self):
        """
        Initialize the Evaluation System Orchestrator.
        """

        EvaluationSystemParameters.loadParameters()
        self.testing = EvaluationSystemParameters.TESTING



        self.labels_buffer = LabelsBuffer()
        self.labelReceiver_and_configurationSender = LabelReceiver_and_ConfigurationSender()
        self.evaluation_report_view = EvaluationReportView()



    def _get_classifier_evaluation(self) -> (bool, dict or None):
        """
        Retrieve the classifier evaluation given by the Human Operator.

        :return: False + None if the file containing the classifier evaluation does not exist yet.
                 True + dict otherwise.
        """

        try:
            with open("human_operator_workspace/classifier_evaluation.json", "r") as f:
                # The file exists. Now we need to check the content.
                data = json.load(f)

                # Validating the JSON content
                with open("schemas/classifier_evaluation_schema.json", "r") as schema_file:
                    schema = json.load(schema_file)
                    jsonschema.validate(data, schema)

                return True, data
        except:
            return False, None



    def Evaluate(self):
        """
        Main method of the Evaluation System Orchestrator.
        """

        self.labelReceiver_and_configurationSender.start_server()

        classifier_evaluation_exists, classifier_evaluation = self._get_classifier_evaluation()

        while True:
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

                # Testing mode, evaluation automatically generated
                random_evaluation = int(random.random() <= 0.3)
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
                    return

            #







        # OLD CODE
        while True:
            if stop_and_go is None or stop_and_go["step"] == "before_evaluation":
                while True:
                    # wait until we have a sufficient number of labels
                    label = self.eval_sys_io.recv_label()
                    if self._service_flag:
                        self.eval_sys_io.send_timestamp(time.time(), "start")
                        # store the received label in a db
                    self.label_storage_controller.store_label(label)
                    print("label stored: " + str(label.to_dict()))
                    # increments the received label counter (depending on the label_type)
                    self._inc_num_labels(label)
                    # if the number of label if sufficient let's generate the evaluation report
                    if self._check_num_labels():
                        print("sufficient labels")
                        break
                    elif self._service_flag:
                        self.eval_sys_io.send_timestamp(time.time(), "end")

                # get all the labels previously stored
                classifier_labels, expert_labels = self.label_storage_controller.get_stored_labels(
                    2 * ConfigurationParameters.MIN_LABELS)

                # generate the evaluation report
                self.eval_report_view.generate_evaluation_report(classifier_labels, expert_labels)

                # remove stored labels
                self.label_storage_controller.remove_label(classifier_labels)
                self.label_storage_controller.remove_label(expert_labels)
                # decrease the label counters a value equal to the label used to generate the report
                self._num_labels_expert = (self._num_labels_expert
                                           - ConfigurationParameters.MIN_LABELS)
                self._num_labels_classifier = (self._num_labels_classifier
                                               - ConfigurationParameters.MIN_LABELS)
                print("labels removed")
                if not self._service_flag:
                    return
            # service flag is true, the decision is generated statistically
            if stop_and_go is None:
                index = int(random.random() <= 0.14)
                if index == 1:  # 14%
                    # classifier is good (both thresholds are satisfied)
                    print("Good classifier")
                    if self._service_flag:
                        self.eval_sys_io.send_timestamp(time.time(), "end")
                    continue
                else:  # 86%
                    # classifier is not good (one of the two threshold is not satisfied)
                    print("Bad classifier")
                    if self._service_flag:
                        self.eval_sys_io.send_timestamp(time.time(), "end")
                    self.eval_sys_io.send_restart_configuration()
                    print("restart configuration sent")
            elif stop_and_go["step"] == "classifier_evaluated":
                # human task: evaluate classifier
                decision = self.eval_sys_io.get_classifier_decision()
                if decision == "bad":
                    # the human decided the classifier is bad
                    print("Bad classifier")
                    # let the system wait for new labels when it restarts
                    stop_and_go["step"] = "before_evaluation"
                    with open("data/stop&go.json", 'w', encoding='utf_8') as stop_and_go_file:
                        json.dump({"step": "before_evaluation"}, stop_and_go_file)
                    if self._service_flag:
                        self.eval_sys_io.send_timestamp(time.time(), "end")
                    self.eval_sys_io.send_restart_configuration()
                    print("restart configuration sent")
                    continue
                elif decision == "good":
                    # the human decided the classifier is good
                    print("Good classifier")
                    # let the system wait for new labels when it restarts
                    stop_and_go["step"] = "before_evaluation"
                    with open("data/stop&go.json", 'w', encoding='utf_8') as stop_and_go_file:
                        json.dump({"step": "before_evaluation"}, stop_and_go_file)
                    continue
                if self._service_flag:
                    self.eval_sys_io.send_timestamp(time.time(), "end")

