"""
Module: record_buffer_controller
This module handles the buffering of records in the ingestion system.
"""

class RecordBufferController:
    """
    Controller for managing the record buffer.
    Provides methods to store, retrieve, and remove records from the buffer.
    """

    # Static buffer to store records
    _records_buffer = []

    @staticmethod
    def store_record(record):
        """
        Store a record in the buffer.

        Args:
            record (dict): A dictionary representing the record to store.
        """
        RecordBufferController._records_buffer.append(record)

    @staticmethod
    def get_records():
        """
        Retrieve all records from the buffer.

        Returns:
            list: List of all records in the buffer.
        """
        return RecordBufferController._records_buffer

    @staticmethod
    def remove_records():
        """
        Remove all records from the buffer.
        """
        RecordBufferController._records_buffer.clear()
