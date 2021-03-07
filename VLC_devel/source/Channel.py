import numpy as np

import Global

from generalLibrary import timer_dec, sync_track

import generalLibrary as lib

from generalLibrary import printDebug, plotDebug

from scipy import signal

class Channel(object):
    
    def __init__(self, tx_data_in, sync_obj):
        """Constructor."""
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Channel") or self.sync_obj.getDebug("all")

        self.PLOT = self.sync_obj.getPlot("Channel") or self.sync_obj.getPlot("all")
        
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

    @sync_track
    def calculatesChannelResponse(self):
        """Calculates the channel response. Must set the channel response before, if raytrace is off."""
        
        
        
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
    
    @sync_track
    def definesChannelResponse(self):
        """Defines a new channel response. Get from imput definition."""
        
        # starts list of channel responses
        self.channel_response = []
        
        # get_channel = Global.list_of_channel_response
        for get_channel in Global.list_of_channel_response:
            channel_type = next(iter(get_channel.keys()))
            if channel_type == "impulse" or channel_type == "butter":
                delay_list = []
                gain_list = []
                for (gain, delay) in get_channel[channel_type]:
                    delay_list.append(delay)
                    gain_list.append(gain)
                # get max delay from input delays
                max_delay = np.max(delay_list)
                gain_sum = np.sum(gain_list)

                # # max delay times 10%
                # max_position = int((max_delay/Global.time_step)*1.5)
                
                CIR = 0
                for (gain, delay) in get_channel[channel_type]:
                    delay_position = int(np.round(delay/Global.time_step))
                    # CIR += gain*signal.unit_impulse(int(Global.number_of_points), delay_position)
                    # CIR_number_of_points = 
                    # CIR += gain*signal.unit_impulse(max_position, delay_position)
                    # CIR += gain*signal.unit_impulse(int(Global.number_of_points), int(Global.number_of_points*0.1))
                    # asdsa
                    # apply weight do each impulse
                    CIR += (gain)*signal.unit_impulse(Global.number_of_points, delay_position)
                
                # divide CIR by number of impulses
                # CIR /= len(get_channel[channel_type])

                # divide by sum of gains, to do wigthed sum (to normalize)
                CIR /= gain_sum

                # then, multiply by max gain
                CIR *= np.max(gain_list)

            else:
                raise ValueError(f"\n\n***Error --> <{channel_type}> not supported yet!\n")
            
            # if butterworth...
            if channel_type == "butter":
                b, a = signal.butter(1, 0.2)
                CIR = signal.lfilter(b, a, CIR)
            
            if self.PLOT:
                plotDebug(CIR, symbols='ro-')
            
            self.channel_response.append(CIR)
    
    
    @sync_track
    # @timer_dec
    def applyChannelResponse(self):
        """Convolves the tx_data with the channel, and get the rx_data."""
        
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
                
                ## TODO --- DEBUG WHY THE 'ACTUAL' CHANNEL RESPONSE IS NOT MATCHING THE PILOTS ESTIMATES??
                ## TODO --- LOOKS LIKE THE 'ABS' HELPS, SINCE THE OFDM FOR LIFI USES ONLY 'REAL' DATA.
                ## TODO --- IS THERE AN ISSUE WITH THE CONVOLUTION FOR THIS OFDM?

                # if Global.IM_DD:
                #     CIR = np.abs(CIR)

                printDebug(CIR.shape)
                printDebug(tx_data.shape)

                printDebug(CIR)
                # plotDebug(tx_data, Global.base_time_vector)
                if self.PLOT:
                    plotDebug(CIR, Global.base_time_vector)
                    plotDebug(tx_data, Global.base_time_vector, symbols='ro-')
                # plotDebug(CIR)

                # Apply convolution
                convolved = np.convolve(tx_data, CIR)
                from scipy import signal
                # convolved = signal.convolve(tx_data, CIR, mode='same')
                # convolved = signal.convolve(tx_data, CIR, mode='valid')
                convolved = signal.convolve(tx_data, CIR)
                # plotDebug(convolved, Global.base_time_vector)
                printDebug(convolved)
                printDebug(len(convolved))
                # plotDebug(convolved)
                printDebug(len(CIR))
                printDebug(len(tx_data))
                if self.PLOT:
                    plotDebug(convolved)

                ### TODO --- NEED TO DEFINE THE OFDM TIME DELTA, AND CORRELATE IT TO THE FFT NUMBER, SAMPLING, ETC.
                ### TODO --- HOW TO DESCRIBE THE CHANNEL MATCHEMATICALLY?
                
                # Apply noise to a signal
                noisy_signal = self.applyChannelNoise(convolved)
                
                # TODO --  IS THAT CORRECT? APPLY CIR AND THEN ABS (or clip to zero)
                if Global.IM_DD:
                    noisy_signal = lib.zeroClip(noisy_signal)
                    print(noisy_signal)
                    noisy_signal = np.abs(noisy_signal)
                    print(noisy_signal)
                    
                
                summed_noisy_signal += noisy_signal
                counter += 1
                
            ### TODO - Sum the contribution of all convolved signals of multiple CIRs
            ### TODO - Must go to each adequate LED 
            mean_noisy_signal = summed_noisy_signal/counter
            if self.PLOT:
                plotDebug(mean_noisy_signal)
                printDebug(np.max(mean_noisy_signal))
                printDebug(np.max(convolved))
                printDebug(np.max(tx_data))
            
            # Append to list of noisy signals
            self.rx_data_out.append(mean_noisy_signal)
            
            
    @sync_track
    def calculatesReceiverSNR(self, SNR=None):
        """Calculates the SNR at the side of the receiver. If raytrace is on, it is calculated; if not, must pass the expected value."""
        
        raise ValueError(f"\n\n***Error --> Calculation of rx_SNR not implemented yet!\n")
    
    @sync_track
    def applyChannelNoise(self, signal):
        """Apply the noise in the channel, given the rx_SNR, and outputs the final value for the rx_data_out."""
        
        # If noise not applieable
        if self.rx_SNR == None:
            return signal
        
        # Average power for the convolved signal
        signal_power = np.mean(abs(signal**2))
        
        # Calculate the std for given signal power, based on rx_SNR
        sigma2 = signal_power * 10**( -self.rx_SNR/10)
        
        # Generate noise given std
        noise = np.sqrt(sigma2/2) * (np.random.randn(*signal.shape)+1j*np.random.randn(*signal.shape))
        
        # TODO --  IS THAT CORRECT? APPLY CIR AND THEN ABS
        if Global.IM_DD:
            noise = np.abs(noise)
        
        return noise + signal
    

    @sync_track
    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        return self.tx_data_in

    @sync_track
    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        self.tx_data_in = tx_data_in
        
    @sync_track
    def getChannelResponse(self):
        """Returns value of self.channel_response"""
        
        
        return self.channel_response

    @sync_track
    def setChannelResponse(self, channel_response):
        """Set new value for list of self.channel_response"""
        
        
        # Make sure passing a list of CIR for each LightSource
        assert isinstance(channel_response, list)
        
        self.channel_response = channel_response

    @sync_track
    def getRxConvolved(self):
        """Returns value for list of self.rx_convolved"""
        
        return self.rx_convolved

    @sync_track
    def setRxConvolved(self, rx_convolved):
        """Set new value for self.rx_convolved"""
        
        self.rx_convolved = rx_convolved

    @sync_track
    def getRxSNR(self):
        """Returns value of self.rx_SNR"""
        
        
        
        return self.rx_SNR

    @sync_track
    def setRxSNR(self, rx_SNR):
        """Set new value for self.rx_SNR"""
        
        self.rx_SNR = rx_SNR

    @sync_track
    def getRxOpticalPower(self):
        """Returns value of self.rx_optical_power"""
        
        return self.rx_optical_power

    @sync_track
    def setRxOpticalPower(self, rx_optical_power):
        """Set new value for self.rx_optical_power"""
        
        self.rx_optical_power = rx_optical_power

    @sync_track
    def getRxStd(self):
        """Returns value of self.rx_std"""
        
        return self.rx_std

    @sync_track
    def setRxStd(self, rx_std):
        """Set new value for self.rx_std"""
        
        self.rx_std = rx_std

    @sync_track
    def getRxNoise(self):
        """Returns value of self.rx_noise"""
        
        return self.rx_noise

    @sync_track
    def setRxNoise(self, rx_noise):
        """Set new value for self.rx_noise"""
        
        self.rx_noise = rx_noise

    @sync_track
    def getRxDataOut(self):
        """Returns value of self.rx_data_out"""
        
        
        return self.rx_data_out

    @sync_track
    def setRxDataOut(self, rx_data_out):
        """Set new value for self.rx_data_out"""
        
        
        self.rx_data_out = rx_data_out

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj