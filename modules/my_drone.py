import logging
from dronekit import connect, APIException
from modules.my_vehicle import MyVehicle
from modules.lands import Land, CoordinateSystem
from modules.servo_motor import ServoMotor
from modules import land_dao
import time

# Constants
NOT_CONTAIN_ANGLE = 0
OUT_OF_LANDS = -1

# Logging configuration
logging.basicConfig(level=logging.INFO)

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

class MyDrone:
    def __init__(self, connection_string):
        self.lands = land_dao.load_lands()
        self.current_land_index = OUT_OF_LANDS
        self.connection_string = connection_string
        self.servo_motor = ServoMotor()
        self.vehicle = None

    def seed_start(self):
        self.connect_drone()
        while True:
            new_current_index = self.__find_current_land_index()
            if new_current_index != self.current_land_index:
                logging.info("구역을 이동했으므로 서보모터 각도를 변경합니다")
                self.current_land_index = new_current_index
                angle = self.lands[new_current_index].sub_motor_angle if new_current_index != OUT_OF_LANDS else 0
                self.servo_motor.change_angle(angle)
            time.sleep(1)  # 1초 대기 후 다음 반복

    def connect_drone(self):
        self.vehicle = connect_drone(self.connection_string)
        if self.vehicle:
            # Disable SERIAL5_PROTOCOL
            self.vehicle.parameters['SERIAL5_PROTOCOL'] = 0  # None
            logging.info("SERIAL5_PROTOCOL disabled.")
        else:
            logging.error("Failed to connect to the drone.")

    def __find_current_land_index(self):
        global_location = self.__get_global_location()
        if global_location is None or global_location.lat == 0.0 or global_location.lon == 0.0:
            logging.error("Invalid GPS location")
            return OUT_OF_LANDS
        drone_coordinate_system = CoordinateSystem(global_location.lat, global_location.lon)
        logging.info(f"Drone coordinates: {drone_coordinate_system}")

        for index, land in enumerate(self.lands):
            if land.contain(drone_coordinate_system):
                return index
        return OUT_OF_LANDS

    def __get_global_location(self):
        try:
            global_frame = self.vehicle.location.global_frame
            logging.info("Location obtained")
            logging.info(f"Latitude: {global_frame.lat}, Longitude: {global_frame.lon}")
            return global_frame
        except AttributeError as e:
            logging.error(f"Error getting global location: {e}")
            return None

# Usage
if __name__ == "__main__":
    drone = MyDrone('/dev/ttyACM0')
    drone.seed_start()
