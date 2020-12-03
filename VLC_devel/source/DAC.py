import Global

from generalLibrary import timer_dec, sync_track

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
        
        
    @sync_track
    def convertsToAnalog(self):
        """Converts the digital values to analog. Can employ circuit simulation. Outputs 'dac_tx_data'."""
        
        
        
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
        
        
    @sync_track
    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        
        return self.tx_data_in

    @sync_track
    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        
        self.tx_data_in = tx_data_in
    
    @sync_track
    def getDacTxData(self):
        """Returns value of self.dac_tx_data"""
        
        
        return self.dac_tx_data

    @sync_track
    def setDacTxData(self, dac_tx_data):
        """Set new value for self.dac_tx_data"""
        
        
        self.dac_tx_data = dac_tx_data
        
        
    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj