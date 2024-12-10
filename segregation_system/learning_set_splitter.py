from typing import List
import random

from segregation_system.learning_set import LearningSet
from segregation_system.prepared_session import PreparedSession
from segregation_system.segregation_system_configuration import SegregationSystemConfiguration


class LearningSetSplitter:
    """
    Handles the splitting of prepared sessions into training, validation, and test sets.

    Attributes:
        None
    """

    def __init__(self):
        """
        Initializes the LearningSetSplitter object.
        """
        print("LearningSetSplitter initialized.")

    def generateLearningSets(self, prepared_sessions: List[PreparedSession] , config : SegregationSystemConfiguration) -> LearningSet:
        """
        Divides the given prepared sessions into training, validation, and test sets
        based on the percentages specified in the configuration file.

        Args:
            prepared_sessions (List[PreparedSession]): The list of prepared sessions to split.
            config (SegregationSystemConfiguration): The segregation system configuration.

        Returns:
            LearningSet: An object containing the training, validation, and test sets.

        Raises:
            ValueError: If the sum of the percentages in the configuration is not 100%.
        """
        training_percentage = config.training_set_percentage
        validation_percentage = config.validation_set_percentage
        test_percentage = 1 - (training_percentage + validation_percentage)

        if training_percentage + validation_percentage + test_percentage != 1:
            raise ValueError("The percentages for training, validation, and test sets must sum to 100%.")

        # Shuffle the prepared sessions to ensure random distribution
        random.shuffle(prepared_sessions)

        # Calculate the number of sessions for each set
        total_sessions = len(prepared_sessions)
        training_count = int(total_sessions * training_percentage)
        validation_count = int(total_sessions * validation_percentage)
        test_count = total_sessions - training_count - validation_count

        # Split the sessions
        training_set = prepared_sessions[:training_count]
        validation_set = prepared_sessions[training_count:training_count + validation_count]
        test_set = prepared_sessions[training_count + validation_count:]

        print(f"Generated learning sets: {len(training_set)} training, {len(validation_set)} validation, {len(test_set)} test.")

        # Return the LearningSet object
        return LearningSet(training_set, validation_set, test_set)
