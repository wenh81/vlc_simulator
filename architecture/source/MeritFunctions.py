class MeritFunctions(object):
    def __init__(self, DEBUG=False):
        """Constructor of MeritFunctions."""
        
        if DEBUG:
            print('Running MeritFunctions...')
        
        

        # List of Bit-Error Rates, for each frame.
        self.BER = None

        # Overall system Signal-To-Noise Ratio
        self.SNR = None

        # Average datarate for the whole process.
        self.DataRate = None
    
        pass

    def calculateBER(self):
        """Calculates the BER, for each frame."""
        pass
    

    def calculateSNR(self):
        """Calculates the overall SNR."""
        pass
    

    def calculateDataRate(self):
        """Calculates the overall Data Rate."""
        pass
    

    def getBER(self):
        """Returns value of self.BER"""
        
        return self.BER

    def setBER(self, BER):
        """Set new value for self.BER"""
        
        self.BER = BER

    def getSNR(self):
        """Returns value of self.SNR"""
        
        return self.SNR

    def setSNR(self, SNR):
        """Set new value for self.SNR"""
        
        self.SNR = SNR

    def getDataRate(self):
        """Returns value of self.DataRate"""
        
        return self.DataRate

    def setDataRate(self, DataRate):
        """Set new value for self.DataRate"""
        
        self.DataRate = DataRate
