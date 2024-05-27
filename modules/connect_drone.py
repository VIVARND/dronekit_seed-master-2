import logging
from dronekit import connect, APIException
from modules.my_vehicle import MyVehicle

def connect_drone(connection_string):
    try:
        logging.info(f"Connecting to vehicle on: {connection_string}")
        vehicle = connect(connection_string, wait_ready=True, baud=57600, vehicle_class=MyVehicle)
        logging.info(f"Connected to {connection_string}")
        return vehicle
    except APIException as e:
        logging.error(f"APIException: Failed to connect to {connection_string}: {e}")
    except Exception as e:
        logging.error(f"Exception: Failed to connect to {connection_string}: {e}")
    return None
