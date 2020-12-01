class DAC(object):
    def __init__(self, tx_data, circuit_simulation, bypass, DEBUG=False):
        """Constructor of DAC."""
        
        if DEBUG:
            print('Running DAC...')
        
        

        # Data to be transmitted, after modulation.
        self.tx_data_in = tx_data

        # Flag to indicate use of circuit simulation.
        self.circuit_simulation = circuit_simulation

        # Flag to bypass the DAC entirely.
        self.bypass = False
    
        pass

    def convertsToAnalog(self):
        """Converts the digital values to analog. Can employ circuit simulation. Outputs 'dac_tx_data'."""
        pass
    

    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        return self.tx_data_in

    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        self.tx_data_in = tx_data_in

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
