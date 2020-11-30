import Global

class DAC(object):
    def __init__(self, tx_data, sync_obj):
        """Constructor of DAC."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("DAC") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("DAC")
        
        if self.DEBUG:
            print('Running DAC...')
        
        # Data to be transmitted, after modulation.
        self.tx_data_in = tx_data

        # Flag to indicate use of circuit simulation.
        self.rounding_or_simul = Global.bypass_dict["DAC_rounding_or_simul"]
        
        
    def convertsToAnalog(self):
        """Converts the digital values to analog. Can employ circuit simulation. Outputs 'dac_tx_data'."""
        
        self.sync_obj.appendToSimulationPath("convertsToAnalog @ DAC")
        
        # Set previous for debug
        self.sync_obj.setPrevious("DAC")
        
        # Starts the list of DAC
        self.dac_tx_data = []
        
        # To choose between ronding or circuit simulation
        if self.rounding_or_simul: # if rouding
            
            # for each ofdm symbol in the list, do the rounding
            for tx_symbol in self.tx_data_in:
                
                # TODO -- Quantization for DAC
                Warning (f"\n\n***Warning --> Still not done quantization for DAC!\n")
                
                self.dac_tx_data.append(abs(tx_symbol))
                
            pass
        else: # if circuit simulation
            raise ValueError(f"\n\n***Error --> Circuit simulation for DAC not supported yet, at bypass_dict['DAC_rounding_or_simul'] = <{Global.bypass_dict['DAC_rounding_or_simul']}>!\n")
        
        
    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        self.sync_obj.appendToSimulationPath("getTxDataIn @ DAC")
        
        return self.tx_data_in

    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        self.sync_obj.appendToSimulationPath("setTxDataIn @ DAC")
        
        self.tx_data_in = tx_data_in
    
    def getDacTxData(self):
        """Returns value of self.dac_tx_data"""
        
        self.sync_obj.appendToSimulationPath("getDacTxData @ DAC")
        
        return self.dac_tx_data

    def setDacTxData(self, dac_tx_data):
        """Set new value for self.dac_tx_data"""
        
        self.sync_obj.appendToSimulationPath("setDacTxData @ DAC")
        
        self.dac_tx_data = dac_tx_data