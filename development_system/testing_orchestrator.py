import joblib
import pandas as pd
from sklearn.metrics import log_loss

from development_system.classifier import Classifier
from development_system.jsonIO import JsonHandler
from development_system.test_report import TestReport
from development_system.test_report_model import TestReportModel
from development_system.test_report_view import TestReportView
from utility.utils import Utils


class TestingOrchestrator:
    """Orchestrator of the testing"""

    def __init__(self):
        """ """
        self.json_handler = JsonHandler()
        self.winner_network = None
        self.test_report = None
        self.test_report_model = TestReportModel()
        self.test_report_view = TestReportView()
        self.file_manager = Utils()

    def test(self):
        """ """
        data = self.json_handler.read_json_file("intermediate_results/winner_network.json")
        classifier_index = data["index"]
        self.winner_network: Classifier = joblib.load("data/classifier" + str(classifier_index ) + ".sav")

        #print("OUTPUT CLASSIFIER NEL .SAV")
        #print("get_train_valid_error_difference:", self.winner_network.get_train_valid_error_difference())
        #print("get_valid_test_error_difference:", self.winner_network.get_valid_test_error_difference())
        #print("iterations:", self.winner_network.get_num_iterations())
        #print("layers:", self.winner_network.get_num_layers())
        #print("neurons:", self.winner_network.get_num_neurons())
        #print("training error:", self.winner_network.get_training_error())
        #print("validation error:", self.winner_network.get_validation_error())
        #print("test error:", self.winner_network.get_test_error())
        #print("loss curve:", self.winner_network.get_loss_curve())

        #print("------------------------------------")

        #network =  self.json_handler.read_winner_network("intermediate_results/winner_network.json")
        #print("OUTPUT CLASSIFIER NEL .JSON")
        #print("get_train_valid_error_difference:", network.get_train_valid_error_difference())
        #print("get_valid_test_error_difference:", network.get_valid_test_error_difference())
        #print("iterations:", network.get_num_iterations())
        #print("layers:", network.get_num_layers())
        #print("neurons:", network.get_num_neurons())
        #print("training error:", network.get_training_error())
        #print("validation error:", network.get_validation_error())
        #print("test error:", network.get_test_error())
        #print("loss curve:", network.get_loss_curve())
        #print("------------------------------------")

        test_data = self.json_handler.read_json_file("data/test_set.json")

        # Estrazione del test set
        test_set = test_data["test_set"]

        # Creazione del DataFrame da test_set
        test_data = pd.DataFrame([
            {"psd_alpha_band": record["psd_alpha_band"],
             "psd_beta_band": record["psd_beta_band"],
             "psd_theta_band": record["psd_theta_band"],
             "psd_delta_band": record["psd_delta_band"],
             # "activity": record["activity"],
             # "environment": record["environment"],
             "label": record["label"]}

            for record in test_set
        ])

        # Separazione delle caratteristiche (X) e delle etichette (y)
        #test_features = pd.DataFrame(test_data["features"].to_list())
        test_features = test_data.drop(columns=["label"])
        test_labels = test_data["label"]

        true_labels = []
        for label in test_labels:
            if label == 1.0:
                true_labels.append([1.0, 0])
            else:
                true_labels.append([0, 1.0])

        self.winner_network.set_test_error(log_loss(true_labels, self.winner_network.predict_proba(test_features)))

        # GENERATE TEST REPORT
        self.test_report = self.test_report_model.generate_test_report(self.winner_network)

        print("test report =", self.test_report)

        #remove all saved classifiers
        self.file_manager.delete_files_pattern("data/classifier*.sav")

        # save winner network (we have to save again it because, now the test_error is updated)
        joblib.dump(self.winner_network, "data/classifier.sav")

        #print("get_train_valid_error_difference:", self.winner_network.get_train_valid_error_difference())
        #print("get_valid_test_error_difference:", self.winner_network.get_valid_test_error_difference())
        #print("iterations:", self.winner_network.get_num_iterations())
        #print("layers:", self.winner_network.get_num_layers())
        #print("neurons:", self.winner_network.get_num_neurons())
        #print("training error:", self.winner_network.get_training_error())
        #print("validation error:", self.winner_network.get_validation_error())
        #print("test error:", self.winner_network.get_test_error())
        #print("loss curve:", self.winner_network.get_loss_curve())

        # CHECK TEST RESULT
        self.test_report_view.show_test_report(self.test_report)