class Modulator(object):
    def __init__(self, mapped_info, modulation_type, DEBUG=False):
        """Constructor of Modulator. It's also the demodulator."""
        
        if DEBUG:
            print('Running Modulator...')
        
        

        # Array with all symbols converted from the input bitstream.
        self.mapped_info = mapped_info

        # Has the shape of the input mapped info.
        self.mapped_shape = mapped_info.shape

        # Number of bits per symbol, before mapping.
        self.bits_per_symbol = mapped_shape[1]

        # Size of frame to be transmitted, from the original info.
        self.frame_size = mapped_shape[0]

        # Type of modulation to be applied in mapped data.
        self.modulation_type = modulation_type
    
        pass

    def createModulator(self):
        """Create modulator object, depending on type chosen."""
        pass
    

    def applyModulation(self):
        """Applies the modulation on the mapped info, and returns the 'tx_data'."""
        pass
    

    def applyDemodulation(self):
        """Applies the de-modulation on the received info, and returns ??????"""
        pass
    

    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        return self.mapped_info

    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.mapped_info = mapped_info

    def getMappedShape(self):
        """Returns value of self.mapped_shape"""
        
        return self.mapped_shape

    def setMappedShape(self, mapped_shape):
        """Set new value for self.mapped_shape"""
        
        self.mapped_shape = mapped_shape

    def getBitsPerSymbol(self):
        """Returns value of self.bits_per_symbol"""
        
        return self.bits_per_symbol

    def setBitsPerSymbol(self, bits_per_symbol):
        """Set new value for self.bits_per_symbol"""
        
        self.bits_per_symbol = bits_per_symbol

    def getFrameSize(self):
        """Returns value of self.frame_size"""
        
        return self.frame_size

    def setFrameSize(self, frame_size):
        """Set new value for self.frame_size"""
        
        self.frame_size = frame_size

    def getModulationType(self):
        """Returns value of self.modulation_type"""
        
        return self.modulation_type

    def setModulationType(self, modulation_type):
        """Set new value for self.modulation_type"""
        
        self.modulation_type = modulation_type
