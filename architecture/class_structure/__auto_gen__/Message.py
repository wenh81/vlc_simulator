class Message(object):
    def __init__(self, input_info, n_frames, DEBUG=False):
        """Constructor of Message."""
        
        if DEBUG:
            print('Running Message...')
        
        

        # Contains a dict with all the information to be sent, for example, as {"type": "image", "data": [image1, image2]}
        self.input_info = input_info

        # List of bitstream info for transmission. Each position is of type 'bitstream.BitStream'.
        self.bitstream_frames = None

        # Number of frames to be transmitted sequentially.
        self.number_of_frames = n_frames

        # Bitstream list info after receiveing, depending on number of frames.
        self.rx_bitstream_frames = None

        # dict with all recovered received information.
        self.output_info = None
    
        pass

    def convertsToBitstream(self):
        """Converts 'input_info' into a list of bistream (bitstream_frames) for transmission, depending on the number of frames to divide the input info."""
        pass
    

    def BitstreamToMessage(self, rx_bitstream_frames):
        """Converts back the received bistream list (rx_bitstream_frames) after receiving, depending on the number of frames."""
        pass
    

    def compareMessages(self):
        """Compares the input and received output info."""
        pass
    

    def getInputInfo(self):
        """Returns value of self.input_info"""
        
        return self.input_info

    def setInputInfo(self, input_info):
        """Set new value for self.input_info"""
        
        self.input_info = input_info

    def getBitstreamFrames(self):
        """Returns value of self.bitstream_frames"""
        
        return self.bitstream_frames

    def setBitstreamFrames(self, bitstream_frames):
        """Set new value for self.bitstream_frames"""
        
        self.bitstream_frames = bitstream_frames

    def getNumberOfFrames(self):
        """Returns value of self.number_of_frames"""
        
        return self.number_of_frames

    def setNumberOfFrames(self, number_of_frames):
        """Set new value for self.number_of_frames"""
        
        self.number_of_frames = number_of_frames

    def getRxBitstreamFrames(self):
        """Returns value of self.rx_bitstream_frames"""
        
        return self.rx_bitstream_frames

    def setRxBitstreamFrames(self, rx_bitstream_frames):
        """Set new value for self.rx_bitstream_frames"""
        
        self.rx_bitstream_frames = rx_bitstream_frames

    def getOutputInfo(self):
        """Returns value of self.output_info"""
        
        return self.output_info

    def setOutputInfo(self, output_info):
        """Set new value for self.output_info"""
        
        self.output_info = output_info
