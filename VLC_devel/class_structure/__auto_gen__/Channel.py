class Channel(object):
    def __init__(self, tx_data_in, raytrace, DEBUG=False):
        """Constructor."""
        
        if DEBUG:
            print('Running Channel...')
        
        

        # Data to be transmitted, after modulation.
        self.tx_data_in = tx_data

        # Flag to say if using Ray Tracing or not.
        self.raytrace = False

        # Stores the channel response, for each lamp.
        self.channel_response = []

        # Convolved data, after modulation.
        self.rx_convolved = None

        # Signal to noise-ratio at the receiver (in dB)
        self.rx_SNR = None

        # Average power of the optical rx_data, after the channel response.
        self.rx_optical_power = None

        # Standard deviation of the rx data, given the rx_SNR
        self.rx_std = None

        # Noise added by the channel, given the rx_SNR.
        self.rx_noise = None

        # Convolved data plus noise introduced by the channel.
        self.rx_data_out = None
    
        pass

    def calculatesChannelResponse(self):
        """Calculates the channel response. Must set the channel response before, if raytrace is off."""
        pass
    

    def applyChannelResponse(self):
        """Convolves the tx_data with the channel, and get the rx_data."""
        pass
    

    def calculatesReceiverSNR(self, SNR=None):
        """Calculates the SNR at the side of the receiver. If raytrace is on, it is calculated; if not, must pass the expected value."""
        pass
    

    def applyChannelNoise(self):
        """Apply the noise in the channel, given the rx_SNR, and outputs the final value for the rx_data_out."""
        pass
    

    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        return self.tx_data_in

    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        self.tx_data_in = tx_data_in

    def getRaytrace(self):
        """Returns value of self.raytrace"""
        
        return self.raytrace

    def setRaytrace(self, raytrace):
        """Set new value for self.raytrace"""
        
        self.raytrace = raytrace

    def getChannelResponse(self):
        """Returns value of self.channel_response"""
        
        return self.channel_response

    def setChannelResponse(self, channel_response):
        """Set new value for self.channel_response"""
        
        self.channel_response = channel_response

    def getRxConvolved(self):
        """Returns value of self.rx_convolved"""
        
        return self.rx_convolved

    def setRxConvolved(self, rx_convolved):
        """Set new value for self.rx_convolved"""
        
        self.rx_convolved = rx_convolved

    def getRxSNR(self):
        """Returns value of self.rx_SNR"""
        
        return self.rx_SNR

    def setRxSNR(self, rx_SNR):
        """Set new value for self.rx_SNR"""
        
        self.rx_SNR = rx_SNR

    def getRxOpticalPower(self):
        """Returns value of self.rx_optical_power"""
        
        return self.rx_optical_power

    def setRxOpticalPower(self, rx_optical_power):
        """Set new value for self.rx_optical_power"""
        
        self.rx_optical_power = rx_optical_power

    def getRxStd(self):
        """Returns value of self.rx_std"""
        
        return self.rx_std

    def setRxStd(self, rx_std):
        """Set new value for self.rx_std"""
        
        self.rx_std = rx_std

    def getRxNoise(self):
        """Returns value of self.rx_noise"""
        
        return self.rx_noise

    def setRxNoise(self, rx_noise):
        """Set new value for self.rx_noise"""
        
        self.rx_noise = rx_noise

    def getRxDataOut(self):
        """Returns value of self.rx_data_out"""
        
        return self.rx_data_out

    def setRxDataOut(self, rx_data_out):
        """Set new value for self.rx_data_out"""
        
        self.rx_data_out = rx_data_out
