from .client import ClientSideOrchestrator

if __name__ == "__main__":
    Csv_data_path = "../data" #path where to find csv data
    client_controller = ClientSideOrchestrator(Csv_data_path)
    client_controller.run(5) #5 is batch max size
