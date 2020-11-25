class Transmitter(object):
    def __init__(self, transmitter_config, tx_data, bypass, DEBUG=False):
        """Constructor of transmitter. Receives a array of lights."""
        
        if DEBUG:
            print('Running Transmitter...')
        
        

        # Contains list of dicts with all information needed to configure the lights on the Transmitter. Each position has a dict, with the type of light, the position for each lamp, and angle. Can be used to configure more than one array of lamps.
        self.transmitter_config = [{"light_type": [], "position": [], "angle": []}]

        # Data to be transmitted, after modulation.
        self.tx_data_in = tx_data

        # Flag to bypass the creation of light sources.
        self.bypass = False
    
        pass

    def createAllLamps(self):
        """Get the transmitter_config, and for each position (each dict), create a different lamp."""
        pass
    

    def createLamp(self):
        """Create a lamp, which is an array of LightSource objects."""
        pass
    

    def applyDAC(self):
        """Converts tx_data into dac values."""
        pass
    

    def calculatesOpticalPower(self):
        """Calculates what is the optical power provided for each time step, as tx_optical (given input dac_values)."""
        pass
    

    def getTransmitterConfig(self):
        """Returns value of self.transmitter_config"""
        
        return self.transmitter_config

    def setTransmitterConfig(self, transmitter_config):
        """Set new value for self.transmitter_config"""
        
        self.transmitter_config = transmitter_config

    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        return self.tx_data_in

    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        self.tx_data_in = tx_data_in

    def getBypass(self):
        """Returns value of self.bypass"""
        
        return self.bypass

    def setBypass(self, bypass):
        """Set new value for self.bypass"""
        
        self.bypass = bypass
