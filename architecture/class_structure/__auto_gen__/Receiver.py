class Receiver(object):
    def __init__(self, receiver_config, rx_data, bypass, DEBUG=False):
        """Constructor of receiver. Receives a array of lights."""
        
        if DEBUG:
            print('Running Receiver...')
        
        

        # Contains list of dicts with all information needed to configure the detectors on the receiver. Each position has a dict, with the type of detector, the position for each detector, and angle. Can be used to configure more than one array of detectors.
        self.receiver_config = [{"detector_type": [], "position": [], "angle": []}]

        # Data to be received, after the channel.
        self.rx_data_in = rx_data

        # Flag to bypass the creation of light sources.
        self.bypass = False
    
        pass

    def createAllDetectors(self):
        """Get the receiver_config, and for each position (each dict), create a different detector array."""
        pass
    

    def createDetector(self):
        """Create a detector array, i.e. na array of Detector objects."""
        pass
    

    def calculatesPhotocurrent(self):
        """Calculates what is the photocurrent provided for each time step, as rx_photocurrent."""
        pass
    

    def calculatesOutVoltage(self):
        """Calculates what is the voltage associated with each photocurrent provided for each time step, as rx_voltage."""
        pass
    

    def applyADC(self):
        """Converts rx_voltage into adc values, given input rx_voltage."""
        pass
    

    def getReceiverConfig(self):
        """Returns value of self.receiver_config"""
        
        return self.receiver_config

    def setReceiverConfig(self, receiver_config):
        """Set new value for self.receiver_config"""
        
        self.receiver_config = receiver_config

    def getRxDataIn(self):
        """Returns value of self.rx_data_in"""
        
        return self.rx_data_in

    def setRxDataIn(self, rx_data_in):
        """Set new value for self.rx_data_in"""
        
        self.rx_data_in = rx_data_in

    def getBypass(self):
        """Returns value of self.bypass"""
        
        return self.bypass

    def setBypass(self, bypass):
        """Set new value for self.bypass"""
        
        self.bypass = bypass
