from modules.drone_sitl import DroneSitl
from modules.my_drone import MyDrone
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

def sitl_start():
    drone_sitl = DroneSitl()
    start(drone_sitl.sitl.connection_string())

def real_start():
    '''
    see https://dronekit-python.readthedocs.io/en/latest/guide/connecting_vehicle.html

    Linux computer connected to the vehicle via Serial port (RaspberryPi example) : /dev/ttyACM0
    '''
    start("/dev/ttyACM0")

def start(connection_string):
    my_drone = MyDrone(connection_string)
    my_drone.seed_start()

if __name__ == "__main__":
    real_start()
