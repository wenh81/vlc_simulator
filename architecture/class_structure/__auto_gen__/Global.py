class Global(object):
    def __init__(self, DEBUG=False):
        """Config file with all parameters."""
        
        if DEBUG:
            print('Running Global...')
        
        

        # Contains list of dicts with all information needed to configure the lights on the Transmitter. Each position has a dict, with the type of light, the position for each lamp, and angle. Can be used to configure more than one array of lamps.
        self.transmitter_config = [{"light_type": [], "position": [], "angle": []}]

        # Contains list of dicts with all information needed to configure the detectors on the receiver. Each position has a dict, with the type of detector, the position for each detector, and angle. Can be used to configure more than one array of detectors.
        self.receiver_config = [{"detector_type": [], "position": [], "angle": []}]

        # List of all wavelengths to be considered during simulation, in nm.
        self.wavelenghts = [550]

        # Temperature in Kelvin.
        self.temperature = 273

        # Defines the simulator to be used, if appliable.
        self.which_simulator = simulator
    
        pass

    def getTransmitterConfig(self):
        """Returns value of self.transmitter_config"""
        
        return self.transmitter_config

    def setTransmitterConfig(self, transmitter_config):
        """Set new value for self.transmitter_config"""
        
        self.transmitter_config = transmitter_config

    def getReceiverConfig(self):
        """Returns value of self.receiver_config"""
        
        return self.receiver_config

    def setReceiverConfig(self, receiver_config):
        """Set new value for self.receiver_config"""
        
        self.receiver_config = receiver_config

    def getWavelenghts(self):
        """Returns value of self.wavelenghts"""
        
        return self.wavelenghts

    def setWavelenghts(self, wavelenghts):
        """Set new value for self.wavelenghts"""
        
        self.wavelenghts = wavelenghts

    def getTemperature(self):
        """Returns value of self.temperature"""
        
        return self.temperature

    def setTemperature(self, temperature):
        """Set new value for self.temperature"""
        
        self.temperature = temperature

    def getWhichSimulator(self):
        """Returns value of self.which_simulator"""
        
        return self.which_simulator

    def setWhichSimulator(self, which_simulator):
        """Set new value for self.which_simulator"""
        
        self.which_simulator = which_simulator
