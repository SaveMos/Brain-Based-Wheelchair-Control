from segregation_system.SegregationSystemJsonHandler import SegregationSystemJsonHandler
from segregation_system.learning_set_splitter import LearningSetSplitter
from segregation_system.segregation_system_parameters import SegregationSystemConfiguration
from segregation_system.session_receiver_and_configuration_sender import SessionReceiverAndConfigurationSender
from segregation_system.test.test_utility_lib import generate_random_prepared_sessions_object_list

# Example to test the class
if __name__ == "__main__":
    SegregationSystemConfiguration.configure_parameters()
    Sessions = generate_random_prepared_sessions_object_list(100)

    LearningSetSplitter = LearningSetSplitter()
    Set = LearningSetSplitter.generateLearningSets(Sessions)

    message_broker = SessionReceiverAndConfigurationSender()

    network_info = SegregationSystemConfiguration.GLOBAL_PARAMETERS["Development System"]

    message_broker.send_message(network_info['ip'], network_info['port'], SegregationSystemJsonHandler.dict_to_string(Set.to_dict()))




