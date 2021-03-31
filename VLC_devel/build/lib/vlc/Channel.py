import numpy as np

import Global

from generalLibrary import timer_dec, sync_track

import generalLibrary as lib

from generalLibrary import printDebug, plotDebug

from scipy import signal

class Channel(object):
    
    def __init__(self, tx_data, tx_data_time, time_step, IM_DD, channel_SNR, sync_obj):
        """Constructor."""
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Channel") or self.sync_obj.getDebug("all")

        self.PLOT = self.sync_obj.getPlot("Channel") or self.sync_obj.getPlot("all")
        
        self.sync_obj.appendToSimulationPath("Channel")
        
        if self.DEBUG:
            print('Running Channel...')        
        
        # Data to be transmitted, after modulation.
        self.tx_data = tx_data
        
        # Time of data to be transmitted
        self.tx_data_time = tx_data_time
        
        # Get minimum time step for simulation (s)
        self.time_step = time_step

        # Indicates if using IM/DD or not
        self.IM_DD = IM_DD

        # Get channel SNR (dB)
        self.channel_SNR = channel_SNR

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
    def definesChannelResponse(self, channel_list = None, time_duration = None):
        """Defines a new channel response. Get from imput definition."""
        
        if channel_list is None:
            raise ValueError(f"\n\n***Error --> channel_list should not be <None>!\n")
        if time_duration is None:
            raise ValueError(f"\n\n***Error --> time_duration should not be <None>!\n")
        elif not isinstance(channel_list, list):
            raise ValueError(f"\n\n***Error --> channel_list should be of type <list>!\n")

        # starts list of channel responses
        self.channel_response = []
        
        # Get dictionary describing the channels
        for get_channel in channel_list:
            if not isinstance(get_channel, dict):
                raise ValueError(f"\n\n***Error --> {get_channel} should be of type <dict>!\n")

            # Get channel dict key for ID.
            channel_id = next(iter(get_channel.keys()))
            
            # Check channel ID to correclty build its model. 
            if channel_id == "impulse" or channel_id == "butter":
                delay_list = []
                gain_list = []
                
                # get all gains and delays for givne input channel
                for (gain, delay) in get_channel[channel_id]:
                    delay_list.append(delay)
                    gain_list.append(gain)
                
                # Sum all gains for latter weighted sum
                max_delay = np.max(delay_list)
                if max_delay > time_duration:
                    raise ValueError(f"\n\n***Error --> Channel < {channel_id} > maximum delay < {max_delay} (s) > should not be larger than < {time_duration} (s) >!\n")

                # Sum all gains for latter weighted sum
                gain_sum = np.sum(gain_list)
                
                # start weighted sum
                CIR = 0
                for (gain, delay) in get_channel[channel_id]:
                    ### delay_position = int(np.round(delay/Global.time_step))
                    # tx_data_time has the same interval betwee two points. Get the time step interval.
                    # delay_position = int(np.round(delay/(self.tx_data_time[1] - self.tx_data_time[0])))
                    
                    # get delay position relative to size of channel time 
                    delay_position = int(np.round(delay/self.time_step))
                    
                    # apply weight do each impulse
                    CIR += (gain)*signal.unit_impulse(int(time_duration/self.time_step), delay_position)
                    # CIR += (gain)*signal.unit_impulse(int(len(self.tx_data_time)), delay_position)
                    # CIR += (gain)*signal.unit_impulse(Global.number_of_points, delay_position)

                # divide by sum of gains, to do weigthed sum (to normalize)
                CIR /= gain_sum

                # then, multiply by max gain
                CIR *= np.max(gain_list)

            else:
                raise ValueError(f"\n\n***Error --> <{channel_id}> not supported yet!\n")
            
            # if butterworth...
            if channel_id == "butter":
                b, a = signal.butter(1, 0.2)
                CIR = signal.lfilter(b, a, CIR)
            
            # get channel time vector
            channel_time = np.arange(0, len(CIR))*self.time_step
            
            if self.PLOT:
                plotDebug(CIR, channel_time, symbols='ro-')
            
            self.channel_response.append([CIR, channel_time])
    
    
    @sync_track
    # @timer_dec
    def applyChannelResponse(self, do_convolution = True, ):
        """Convolves the tx_data with the channel, and get the rx_data."""
        
        # If raytrace is on, calculates the SNR. Overrides previous value
        if self.raytrace:
            self.calculatesReceiverSNR()
        else:
            # SNR already passed in
            pass
        
        # For input tx_data wave
        summed_noisy_signal = 0
        counter = 0
        
        # For each CIR in the CIR list (one CIR for each lamp), apply the convolve
        for CIR, channel_time in self.channel_response:
            
            ## TODO --- DEBUG WHY THE 'ACTUAL' CHANNEL RESPONSE IS NOT MATCHING THE PILOTS ESTIMATES??
            ## TODO --- LOOKS LIKE THE 'ABS' HELPS, SINCE THE OFDM FOR LIFI USES ONLY 'REAL' DATA.
            ## TODO --- IS THERE AN ISSUE WITH THE CONVOLUTION FOR THIS OFDM?
            ## MAIN ISSUE WAS THE INTERPOLATION... kind of filter. Zero-hold order (ZHO) was best interpolation.

            if self.PLOT:
                plotDebug(CIR, channel_time, symbols='b-')
                plotDebug(self.tx_data, self.tx_data_time, symbols='r-')

            if do_convolution:
                # Apply convolution
                convolved = np.convolve(self.tx_data, CIR)
                from scipy import signal
                convolved = signal.convolve(self.tx_data, CIR)

                # Get convolved time vector
                convolved_time = np.arange(0, len(convolved))*self.time_step

                if self.PLOT:
                    plotDebug(convolved, convolved_time)
            else:
                plot_type = 'angle' ## for debugging only
                plot_type = 'abs' ## for debugging only
                plot_type = 'complex'
                
                # number of points in tx data to get frequency, for plot
                n_points = len(self.tx_data_time)
                if self.PLOT:
                    frequencies = np.arange(n_points)/np.max(self.tx_data_time)
                    # Apply roll if plotting the frequency responses
                    roll_value = int(n_points/2) ## centralize spectrum -- for debugging/plot only
                else:
                    roll_value = 0

                if plot_type == 'complex':
                    CIR_FFT = np.roll(np.fft.fft(CIR, n_points), roll_value)
                    tx_data_FFT = np.roll(np.fft.fft(self.tx_data, n_points), roll_value)
                elif plot_type == 'abs':
                    CIR_FFT = np.abs(np.roll(np.fft.fft(CIR, n_points), roll_value))
                    tx_data_FFT = np.abs(np.roll(np.fft.fft(self.tx_data, n_points), roll_value))
                elif plot_type == 'angle':
                    CIR_FFT = np.angle(np.roll(np.fft.fft(CIR, n_points), roll_value))
                    tx_data_FFT = np.angle(np.roll(np.fft.fft(self.tx_data, n_points), roll_value))
                
                # Multiply in frequency domain (equivalent to time domain convolution)
                convolved = CIR_FFT*tx_data_FFT
                
                # Apply IFFT to get time domain signal again
                convolved = np.fft.ifft(np.roll(convolved , -roll_value))

                # Get convolved time vector
                convolved_time = np.arange(0, len(convolved))*self.time_step

                if self.PLOT:
                    plotDebug(CIR_FFT, frequencies)
                    plotDebug(tx_data_FFT, frequencies)
                    plotDebug(convolved, convolved_time)
            
            # search for zeros introduced by convolution, and apply tx_voltage_bias again.
            # This ensure that there are no "steps" when moving into the wave burst symbols
            if self.IM_DD:
                all_zeros = [np.abs(convolved) < Global.zero_slack]
                convolved[all_zeros] += Global.tx_voltage_bias

            # Get convolved time vector
            convolved_time = np.arange(0, len(convolved))*self.time_step

            # Apply noise to a signal
            noisy_signal = self.applyChannelNoise(convolved)
            
            # TODO --  IS THAT CORRECT? APPLY CIR AND THEN ABS (or clip to zero)
            if self.IM_DD and False:
                noisy_signal = lib.zeroClip(noisy_signal)
                printDebug("DEBUG @ Channel")
                plotDebug(noisy_signal, convolved_time)
                noisy_signal = np.abs(noisy_signal)
                plotDebug(noisy_signal, convolved_time)
                printDebug()
                
            
            summed_noisy_signal += noisy_signal
            counter += 1

            ### TODO - Sum the contribution of all convolved signals of multiple CIRs
            ### TODO - Must go to each adequate LED 
            ### TODO - Here the best is to apply a matrix approach Y[pd] = M[pd,led]*X[led];
            # where X[led] are the inputs of tx_data for each "led";
            # Y[pd] is the output rx_data for each "pd"; 
            # M[pd,led] is the matrix of channel responses for each combination of "pd" x "led".
            # If all 'led' and 'pd' are part of the same link, then should summ the response from each "pd"; BUT NOT HERE (after roic)!
            mean_noisy_signal = summed_noisy_signal/counter
            if self.PLOT:
                printDebug(np.max(mean_noisy_signal))
                printDebug(np.max(convolved))
                printDebug(np.max(self.tx_data))
                plotDebug(mean_noisy_signal, convolved_time)
            
            # store the time for after the conbolution. Should be the same for all convolved signals, so no need for a list here.
            self.rx_time = convolved_time
            # Append to list of noisy signals, for each channel link
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
    def getChannelSNR(self):
        """Returns value of self.channel_SNR"""

        return self.channel_SNR

    @sync_track
    def setChannelSNR(self, channel_SNR):
        """Set new value for self.channel_SNR"""
        
        self.channel_SNR = channel_SNR

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
    def getRxTime(self):
        """Returns value of self.rx_time"""
        return self.rx_time

    @sync_track
    def setRxTime(self, rx_time):
        """Set new value for self.rx_time"""
        self.rx_time = rx_time

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