from development_system.trainer import Trainer


class TrainingOrchestrator:
    """Orchestrator of the training"""

    def __init__(self):
        """ """
        self.trainer = Trainer()

    def train_classifier(self, set_average_hyperparams):
        """ """
        if set_average_hyperparams:
            self.trainer.set_average_hyperparameters()