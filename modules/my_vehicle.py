from dronekit import Vehicle, APIException
import logging

# Override the listener to handle APIException
def custom_listener(self, name, msg):
    try:
        original_listener(self, name, msg)
    except APIException as e:
        if "mode" in str(e):
            logging.warning(f"Handled unrecognized mode: {e}")
        else:
            logging.error(f"APIException occurred: {e}")
    except Exception as e:
        logging.error(f"General Exception occurred: {e}")

# Store original listener and override
original_listener = Vehicle.notify_message_listeners
Vehicle.notify_message_listeners = custom_listener

class MyVehicle(Vehicle):
    def __init__(self, *args):
        super(MyVehicle, self).__init__(*args)
        # Add custom initializations if needed
