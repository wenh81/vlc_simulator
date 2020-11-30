import numpy as np

import Global

class Channel(object):
    def __init__(self, tx_data_in, sync_obj):
        """Constructor."""
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Channel") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Channel")
        
        if self.DEBUG:
            print('Running Channel...')        
        
        # Data to be transmitted, after modulation.
        self.tx_data_in = tx_data_in

        # Flag to say if using Ray Tracing or not.
        self.raytrace = Global.use_raytrace

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

        # Convolved list of data plus noise introduced by the channel.
        self.rx_data_out = []
    
        pass

    def calculatesChannelResponse(self):
        """Calculates the channel response. Must set the channel response before, if raytrace is off."""
        
        self.sync_obj.appendToSimulationPath("calculatesChannelResponse @ Channel")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Channel")
        
        if self.raytrace:
            
            # TODO --  DO RAYTRACE CALCULATIONS
            pass
            
        elif not Global.bypass_dict["LightSource"]:
            
            # TODO --  CALCULATE CIR WITHOUT RAYTRACE FOR EACH LIGHTSOURCE
            pass
        
        else:
            raise ValueError(f"\n\n***Error --> Option not allowed, with:\n\tGlobal.use_raytrace=False\n\
                \tGlobal.bypass_dict['LightSource']=True\n\tGlobal.bypass_dict['Channel']=False\n")
        
        
        raise ValueError(f"\n\n***Error --> Calculate channel response not implemented yet!\n")
    
    
    def applyChannelResponse(self):
        """Convolves the tx_data with the channel, and get the rx_data."""
        
        self.sync_obj.appendToSimulationPath("applyChannelResponse @ Channel")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Channel")
        
        # If raytrace is on, calculates the SNR.
        if self.raytrace:
            self.calculatesReceiverSNR()
        else:
            self.setRxSNR(rx_SNR = Global.rx_SNR_dB)
        
        # For each tx_data in the list of info to be transmitted
        for tx_data in self.tx_data_in:
            
            summed_noisy_signal = 0
            counter = 0
            
            # For each CIR in the CIR list (one CIR for each lamp), apply the convolve
            for CIR in self.channel_response:
                
                # Apply convolution
                convolved = np.convolve(tx_data, CIR)
                
                # Set previous for debug
                self.sync_obj.setPrevious("Channel")
                
                # Apply noise to a signal
                noisy_signal = self.applyChannelNoise(convolved)
                
                # Set previous for debug
                self.sync_obj.setPrevious("Channel")
                
                summed_noisy_signal += noisy_signal
                counter += 1
                
            ### TODO - Sum the contribution of all convolved signals of multiple CIRs
            mean_noisy_signal = summed_noisy_signal/counter
            
            
            # Append to list of noisy signals
            self.rx_data_out.append(mean_noisy_signal)
            
            
    def calculatesReceiverSNR(self, SNR=None):
        """Calculates the SNR at the side of the receiver. If raytrace is on, it is calculated; if not, must pass the expected value."""
        
        self.sync_obj.appendToSimulationPath("calculatesReceiverSNR @ Channel")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Channel")
        
        raise ValueError(f"\n\n***Error --> Calculation of rx_SNR not implemented yet!\n")
    
    def applyChannelNoise(self, signal):
        """Apply the noise in the channel, given the rx_SNR, and outputs the final value for the rx_data_out."""
        
        self.sync_obj.appendToSimulationPath("applyChannelNoise @ Channel")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Channel")
        
        # Average power for the convolved signal
        signal_power = np.mean(abs(signal**2))
        
        # Calculate the std for given signal power, based on rx_SNR
        sigma2 = signal_power * 10**( -self.rx_SNR/10)
        
        # Generate noise given std
        noise = np.sqrt(sigma2/2) * (np.random.randn(*signal.shape)+1j*np.random.randn(*signal.shape))
        
        return noise + signal
    

    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        return self.tx_data_in

    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        self.tx_data_in = tx_data_in
        
    def getChannelResponse(self):
        """Returns value of self.channel_response"""
        
        self.sync_obj.appendToSimulationPath("getChannelResponse @ Channel")
        
        return self.channel_response

    def setChannelResponse(self, channel_response):
        """Set new value for list of self.channel_response"""
        
        self.sync_obj.appendToSimulationPath("setChannelResponse @ Channel")
        
        # Make sure passing a list of CIR for each LightSource
        assert isinstance(channel_response, list)
        
        self.channel_response = channel_response

    def getRxConvolved(self):
        """Returns value for list of self.rx_convolved"""
        
        return self.rx_convolved

    def setRxConvolved(self, rx_convolved):
        """Set new value for self.rx_convolved"""
        
        self.rx_convolved = rx_convolved

    def getRxSNR(self):
        """Returns value of self.rx_SNR"""
        
        self.sync_obj.appendToSimulationPath("getRxSNR @ Channel")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Channel")
        
        return self.rx_SNR

    def setRxSNR(self, rx_SNR):
        """Set new value for self.rx_SNR"""
        
        self.sync_obj.appendToSimulationPath("setRxSNR @ Channel")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Channel")
        
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
        
        self.sync_obj.appendToSimulationPath("getRxDataOut @ Channel")
        
        return self.rx_data_out

    def setRxDataOut(self, rx_data_out):
        """Set new value for self.rx_data_out"""
        
        self.sync_obj.appendToSimulationPath("setRxDataOut @ Channel")
        
        self.rx_data_out = rx_data_out
