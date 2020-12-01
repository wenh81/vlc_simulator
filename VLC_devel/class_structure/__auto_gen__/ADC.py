class ADC(object):
    def __init__(self, rx_data, circuit_simulation, bypass, DEBUG=False):
        """Constructor of DAC."""
        
        if DEBUG:
            print('Running ADC...')
        
        

        # Data to be transmitted, after modulation.
        self.rx_data_in = rx_data

        # Flag to indicate use of circuit simulation.
        self.circuit_simulation = circuit_simulation

        # Flag to bypass the ADC entirely.
        self.bypass = False
    
        pass

    def convertsToDigital(self):
        """Converts the analog to digital values. Can employ circuit simulation. Outputs 'dac_rx_data'."""
        pass
    

    def getRxDataIn(self):
        """Returns value of self.rx_data_in"""
        
        return self.rx_data_in

    def setRxDataIn(self, rx_data_in):
        """Set new value for self.rx_data_in"""
        
        self.rx_data_in = rx_data_in

    def getCircuitSimulation(self):
        """Returns value of self.circuit_simulation"""
        
        return self.circuit_simulation

    def setCircuitSimulation(self, circuit_simulation):
        """Set new value for self.circuit_simulation"""
        
        self.circuit_simulation = circuit_simulation

    def getBypass(self):
        """Returns value of self.bypass"""
        
        return self.bypass

    def setBypass(self, bypass):
        """Set new value for self.bypass"""
        
        self.bypass = bypass
