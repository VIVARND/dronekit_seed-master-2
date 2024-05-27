from dronekit_sitl import SITL

class DroneSitl:
    def __init__(self):
        self.sitl = SITL()
        self.sitl.download('copter', '3.3', verbose=True)
        self.sitl_args = ['--model', 'quad']
        self.sitl.launch(self.sitl_args, await_ready=True)

    def connection_string(self):
        return self.sitl.connection_string()
