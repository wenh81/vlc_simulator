class OFDM(object):
    def __init__(self, ofdm_type, mapped_info, pilot_value, n_carriers, n_pilots, n_cp, DEBUG=False):
        """Constructor of OFDM."""
        
        if DEBUG:
            print('Running OFDM...')
        
        

        # Type of OFDM modulation, such as DCO or ACO-OFDM.
        self.ofdm_type = ofdm_type

        # Array with all symbols converted from the input bitstream.
        self.mapped_info = mapped_info

        # Value for the pilot in the OFDM symbol.
        self.pilot_value = pilot_value

        # Number of OFDM subcarriers per symbol.
        self.number_of_carriers = n_carriers

        # Number of pilot carriers per OFDM symbol.
        self.number_of_pilots = n_pilots

        # Length of the cyclic prefix  per OFDM symbol.
        self.number_of_cyclic_prefix = n_cp
    
        pass

    def applyModulation(self):
        """Wrapper for all functions to apply the OFDM modulation on the mapped info."""
        pass
    

    def generateOFDMSymbol(self):
        """Generate OFDM symbols."""
        pass
    

    def applyIFFT(self):
        """Applies the IDFT on the OFDM symbols."""
        pass
    

    def applyCp(self):
        """Add the cyclic prefix to the OFDM symbol, and creates the 'ofdm_symbol_tx'"""
        pass
    

    def removeCp(self, ofdm_symbol_rx):
        """Removes the cyclic prefix from 'ofdm_symbol_rx'."""
        pass
    

    def applyIFFT(self):
        """Applies the DFT on input info, to generate the OFDM symbols."""
        pass
    

    def estimateChannel(self):
        """Analyze pilots to get the channel estimation."""
        pass
    

    def equalize(self):
        """Equalize, given OFDM symbols from DFT operation, and the channel estimate."""
        pass
    

    def getConstellation(self):
        """Given equalized data, return the 'mapped_output'."""
        pass
    

    def getOfdmType(self):
        """Returns value of self.ofdm_type"""
        
        return self.ofdm_type

    def setOfdmType(self, ofdm_type):
        """Set new value for self.ofdm_type"""
        
        self.ofdm_type = ofdm_type

    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        return self.mapped_info

    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.mapped_info = mapped_info

    def getPilotValue(self):
        """Returns value of self.pilot_value"""
        
        return self.pilot_value

    def setPilotValue(self, pilot_value):
        """Set new value for self.pilot_value"""
        
        self.pilot_value = pilot_value

    def getNumberOfCarriers(self):
        """Returns value of self.number_of_carriers"""
        
        return self.number_of_carriers

    def setNumberOfCarriers(self, number_of_carriers):
        """Set new value for self.number_of_carriers"""
        
        self.number_of_carriers = number_of_carriers

    def getNumberOfPilots(self):
        """Returns value of self.number_of_pilots"""
        
        return self.number_of_pilots

    def setNumberOfPilots(self, number_of_pilots):
        """Set new value for self.number_of_pilots"""
        
        self.number_of_pilots = number_of_pilots

    def getNumberOfCyclicPrefix(self):
        """Returns value of self.number_of_cyclic_prefix"""
        
        return self.number_of_cyclic_prefix

    def setNumberOfCyclicPrefix(self, number_of_cyclic_prefix):
        """Set new value for self.number_of_cyclic_prefix"""
        
        self.number_of_cyclic_prefix = number_of_cyclic_prefix
