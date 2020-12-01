class Mapping(object):
    def __init__(self, bitstream_frames, mapping_type, bits_per_symbol, DEBUG=False):
        """Constructor of Mapping, that parallelizes and maps the input stream."""
        
        if DEBUG:
            print('Running Mapping...')
        
        

        # Bitstream list info for transmission, depending on number of frames.
        self.bitstream_frames = bitstream_frames

        # Number of bits per symbol, before mapping.
        self.bits_per_symbol = bits_per_symbol

        # Size of current frame to be transmitted.
        self.frame_size = 1

        # Array with all symbols converted from the input bitstream.
        self.mapped_info = np.zeros([bits_per_symbol, len(frame_size)/bits_per_symbol], dtype=complex)

        # Type of mapping to be applied in parallelized data.
        self.mapping_type = mapping_type

        # Bitstream list info after receiveing, depending on number of frames.
        self.rx_bitstream_frames = None
    
        pass

    def serialToParallel(self):
        """Converts each position of 'bitstream_frames' into 2D numpy array, as [bits_per_symbol, len(bitstream_info)/bits_per_symbol]"""
        pass
    

    def applyMapping(self):
        """Given 'bits_per_symbol' and 'mapping_type', generates the 'mapped_info'."""
        pass
    

    def applyDemapping(self):
        """Given 'mapped_output', returns the closest values for the demapping."""
        pass
    

    def ParallelToserial(self):
        """Converts each position of 'bitstream_frames' into a serial stream of data 'rx_bitstream_frames'."""
        pass
    

    def getBitstreamFrames(self):
        """Returns value of self.bitstream_frames"""
        
        return self.bitstream_frames

    def setBitstreamFrames(self, bitstream_frames):
        """Set new value for self.bitstream_frames"""
        
        self.bitstream_frames = bitstream_frames

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

    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        return self.mapped_info

    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.mapped_info = mapped_info

    def getMappingType(self):
        """Returns value of self.mapping_type"""
        
        return self.mapping_type

    def setMappingType(self, mapping_type):
        """Set new value for self.mapping_type"""
        
        self.mapping_type = mapping_type

    def getRxBitstreamFrames(self):
        """Returns value of self.rx_bitstream_frames"""
        
        return self.rx_bitstream_frames

    def setRxBitstreamFrames(self, rx_bitstream_frames):
        """Set new value for self.rx_bitstream_frames"""
        
        self.rx_bitstream_frames = rx_bitstream_frames
