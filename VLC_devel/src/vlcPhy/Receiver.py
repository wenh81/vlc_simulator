from .common_imports import *

class Receiver(object):
    
    def __init__(self, receiver_config, roic_config, rx_data, rx_time, sample_freq, sample_phase, adc_configuration, sync_obj):
        """Constructor of receiver. Receives a array of lights."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        # Get debug and plot flags
        self.DEBUG, self.PLOT = lib.getDebugPlot("Receiver", self.sync_obj)
        
        self.sync_obj.appendToSimulationPath("Receiver")
        
        if self.DEBUG:
            print('Running Receiver...')

        # Sample frequency for the receiver
        self.sample_freq = sample_freq
        
        # Sample phase for the receiver
        self.sample_phase = sample_phase

        # Voltage references / number of bits
        self.adc_configuration = adc_configuration
        
        # Contains list of dicts with all information needed to configure the detectors on the receiver. Each position has a dict, with the type of detector, the position for each detector, and angle. Can be used to configure more than one array of detectors.
        self.receiver_config = receiver_config
        
        # Contains list of dicts with all information needed to configure the ROICs on the receiver. Each position has a dict, with the type of ROIC, associated with each corresponding detector. Can be used to configure more than one array of ROICs.
        self.roic_config = roic_config
        
        # Data to be received, after the channel
        self.rx_data = rx_data
        
        # Data time related to input data
        self.rx_time = rx_time
        
        # Flag that indicates if adc was already applied for this wave
        self.applied_offset = False
        
        # # rx data list for all photocurrents
        # self.rx_photocurrent = []
        
        # Defines the simulator to be used, if appliable.
        self.which_simulator = Global.which_simulator
        

    @sync_track
    def createDetectorArray(self):
        """Get the receiver_config (dict), and creates a detector array."""
        
        # start detector_array
        self.detector_array = []
        
        # For each detector in the detector array
        for idx in range(0, len(self.receiver_config["detector_type"])):
            
            # Create array of detectors
            self.detector_array.append(
                self.createDetector(
                    detector_type = self.receiver_config["detector_type"][idx],
                    position = self.receiver_config["position"][idx],
                    angle = self.receiver_config["angle"][idx]
                )
            )
            
            
    @sync_track
    def createDetector(self, detector_type, position, angle):
        """Create a detector array, i.e. an array of Detector objects."""
        
        
        # Create detector object
        detector_obj = Detector(
            detector_type = detector_type,
            position = position,
            angle = angle,
            sync_obj = self.sync_obj
        )
        
        return detector_obj
    
    # @sync_track
    # def assembleWaveTrain(self):
    #     """Get list of waves from TX, and concatanates on a single wave train."""

    #     shift = 0

    #     all_zeros = np.zeros((1+len(self.rx_data))*Global.number_of_points)
    #     self.rx_wave_train = all_zeros.copy()*(0+0j)
    #     for data in self.rx_data:
    #         # starts vector with all zeros plus actual data
    #         new_data = lib.sumVectosDiffSizes(all_zeros.copy()*(0+0j), data)
    #         if shift >= 0:
    #             shift += 1
    #             new_data = np.roll(new_data, (shift-1)*Global.number_of_points)

    #         self.rx_wave_train = lib.sumVectosDiffSizes(self.rx_wave_train, new_data)
        
    #     self.rx_wave_time = np.arange(0, len(self.rx_wave_train))*Global.time_step
        

    @sync_track
    def calculatesPhotocurrent(self):
        """Calculates what is the photocurrent provided for each time step, as rx_photocurrent."""
        
        # TODO --- TEMP FIX... REMOVE LISTING ON RX END... USE rx_wave_train AND SMAPLE IT
        # self.rx_data = list(self.rx_wave_train)
        # self.rx_time

        # If not bypassing the detector, calculate photocurrent based on it.
        if not Global.bypass_dict["Detector"]:
            
            # Create all configured detectors for that rx, and pass the input info to all of them.
            self.createDetectorArray()
            
            # TODO -- DO SOME CALCULATIONS BASED ON DETECTORS
            
            # Calculates photocurrent for all detectors in the array
            for detector in self.detector_array:
                
                # do conversion to photocurrent
                self.rx_photocurrent = detector.convertsToPhotocurrent(self.rx_data)

            ## TODO --- Must sum the contributions from all PDs here
            
            raise ValueError(f"\n\n***Error --> Simulation for detectors not supported yet, at bypass_dict['Detector'] = <{Global.bypass_dict['Detector']}>!\n")
        else:

            # If bypassing, just pass the rx data list
            ### TODO --- Add responsivity here for 'dummy' calc? Or inside the Detector?
            self.rx_photocurrent = self.rx_data
            
        # printDebug(len(self.rx_photocurrent[0]))
        # # plotDebug(self.rx_photocurrent[0], symbols='ro-')
        # plotDebug(self.rx_photocurrent[0], np.arange(0, len(self.rx_photocurrent[0]))*Global.time_step , symbols='ro-')
        
    @sync_track
    def createROICArray(self):
        """Get the roic_config for that rx, and creates its array of different roics."""
        
        # start roic_array
        self.roic_array = []
        
        # For a given receiver, get the dictionary definition for its roic array
        # The array here is for each PD in rx end.
        
        # For each roic in the roic array.
        for idx in range(0, len(self.roic_config["circuit_type"])):
            
            # Create array of roics
            self.roic_array.append(
                self.createROIC(
                    circuit_type = self.roic_config["circuit_type"][idx],
                    gain = self.roic_config["gain"][idx],
                    circuit_simulation = self.roic_config["circuit_simulation"][idx],
                    waves_name = self.roic_config["waves_name"][idx],
                    DR = self.roic_config["DR"][idx],
                    current_noise = self.roic_config["current_noise"][idx],
                    SNR = self.roic_config["SNR"][idx],
                    roic_setup = self.roic_config["roic_setup"][idx]
                )
            )
            
            
    @sync_track
    def createROIC(self, circuit_type, gain, circuit_simulation, waves_name, DR, current_noise, SNR, roic_setup):
        """Create a ROIC array, i.e. an array of ROIC objects."""
        
        if circuit_type == "BouncingPixel":
            
            roic_obj = BouncingPixel(
                gain = gain,
                circuit_simulation = circuit_simulation,
                waves_name = waves_name,
                DR = DR,
                current_noise = current_noise,
                SNR = SNR,
                roic_setup = roic_setup,
                sync_obj = self.sync_obj
            )

        elif circuit_type == "APS":
            
            raise ValueError(f"\n\n***Error --> APS not supported yet!\n")
            
            # roic_obj = APS(
            #     gain = self.gain,
            #     circuit_simulation = self.circuit_simulation,
            #     waves_name = self.waves_name,
            #     sync_obj = self.sync_obj
            # )
            
        else:
            raise ValueError(f"\n\n***Error --> circuit_type < {circuit_type} > is not supported!\n")
        
        return roic_obj
        
    @sync_track
    def calculatesOutVoltage(self):
        """Calculates what is the voltage associated with each photocurrent provided for each time step, as rx_voltage."""
        
        
        # If not bypassing the detector, calculate photocurrent based on it.
        if not Global.bypass_dict["ROIC"]:
            
            # Create all ROICS detectors, and pass the input info to all of them.
            self.createROICArray()
            
            # TODO -- DO SOME CALCULATIONS BASED ON ROICS
            
            # Calculates voltage for all roics in the array (# TODO --- Really need the 'array'?)
            for roic in self.roic_array:
                
                # list of all waves (voltage) -- convertsToWaves belongs to ROIC
                all_waves = roic.convertsToWaves(self.rx_photocurrent)
                
                if roic.getCircuitType() == "BouncingPixel":
                    
                    # gets voltage signals for the Bouncing Pixel
                    self.rx_voltage = roic.calculatesReconstructedVoltage(all_waves)
                    # plotDebug(self.rx_voltage)

                elif roic.getCircuitType() == "APS":
                    
                    raise ValueError(f"\n\n***Error --> APS not supported yet!\n")
                    # # gets voltage signals for the APS
                    # self.rx_voltage = roic.APS_FUNCTION(all_waves)
                    
                else:
                    raise ValueError(f"\n\n***Error --> circuit_type < {roic.getCircuitType()} > is not supported!\n")

                # plotDebug(self.rx_photocurrent[0])
                # self.rx_photocurrent = [wave/np.max(self.rx_photocurrent) \
                #     for wave in self.rx_photocurrent]
                
                # plotDebug(self.rx_photocurrent[0])
                # TODO --- CREATE THE ARRAY FOR EACH ROIC ARRAY....
                # roic_array_photocurrent.append(self.rx_voltage)
        
        else:
            # If bypassing, just pass the rx photocurrent list
            self.rx_voltage = self.rx_photocurrent

        if self.PLOT:
            printDebug(self.rx_voltage)
            plotDebug(self.rx_voltage)

    # @sync_track
    # def applyFilter(self, filter_order = 20, cuttof = 400e6, filter_type = 'low'):
    #     """Apply digital filter. Cutoff in Hz."""

    #     self.adc_rx_data_list = lib.butterFilter(self.adc_rx_data_list, cuttof = cuttof, \
    #         filter_order = filter_order, filter_type = filter_type)
    #     # return [lib.butterFilter(rx_data, cuttof = cuttof, \
    #     #     filter_order = filter_order, filter_type = filter_type)\
    #     #     for rx_data in self.adc_rx_data_list]
    
    @sync_track
    def applyADC(self, offset_value : float = 0, override_freq : float = None, IM_DD : bool = False):
        """Converts rx_voltage into adc values."""
        
        if override_freq is not None:
            self.sample_freq = override_freq

        # printDebug(offset_value)
        # plotDebug(self.rx_voltage, symbols='bo-', hold=True)
        if not self.applied_offset:
            # Remove offset, before ADC / or bypass
            self.rx_voltage -= offset_value
            self.applied_offset = True

        # plotDebug(self.rx_voltage, symbols='ro-')

        # if not bypassing adc
        if not Global.bypass_dict["ADC"]:
            
            # Creates ADC object
            self.adc_obj = ADC(
                rx_data = self.rx_voltage,
                rx_time = self.rx_time,
                sample_freq = self.sample_freq,
                adc_configuration = self.adc_configuration,
                sync_obj = self.sync_obj
            )
            
            # Converts the 'rx_data' to digital, through ADC
            self.sampled_wave, self.sampled_wave_time = self.adc_obj.convertsToDigital()
            
        else:
            # plotDebug(self.rx_voltage, self.rx_time)
            # Bypass ADC -- sample voltage given input frequency
            self.sampled_wave, self.sampled_wave_time = lib.sampleSignal(self.rx_voltage, self.rx_time, self.sample_freq)

        if IM_DD:
            # remove zero
            self.sampled_wave = lib.zeroClip(self.sampled_wave)
            
        # plotDebug(self.sampled_wave)

    @sync_track
    def getReceiverConfig(self):
        """Returns value of self.receiver_config"""
        
        return self.receiver_config

    @sync_track
    def setReceiverConfig(self, receiver_config):
        """Set new value for self.receiver_config"""
        
        self.receiver_config = receiver_config

    @sync_track
    def getRxData(self):
        """Returns value of self.rx_data"""
        
        return self.rx_data

    @sync_track
    def setRxData(self, rx_data_in_list):
        """Set new value for self.rx_data"""
        
        self.rx_data = rx_data_in_list
    
    @sync_track
    def getRxVoltage(self):
        """Returns value of self.rx_voltage"""
        
        return self.rx_voltage

    @sync_track
    def setRxVoltage(self, rx_voltage):
        """Set new value for self.rx_voltage"""
        
        self.rx_voltage = rx_voltage
        
    @sync_track
    def getRxPhotocurrent(self):
        """Returns value of self.rx_photocurrent"""
        
        return self.rx_photocurrent

    @sync_track
    def setRxPhotocurrent(self, rx_photocurrent):
        """Set new value for self.rx_photocurrent"""
        
        self.rx_photocurrent = rx_photocurrent
    
        
    @sync_track
    def getSampledWave(self):
        """Returns value of self.sampled_wave"""
        
        return self.sampled_wave

    @sync_track
    def setSampledWave(self, sampled_wave):
        """Set new value for self.sampled_wave"""
        
        self.sampled_wave = sampled_wave

    @sync_track
    def getSampledWaveTime(self):
        """Returns value of self.sampled_wave_time"""
        
        return self.sampled_wave_time

    @sync_track
    def setSampledWaveTime(self, sampled_wave_time):
        """Set new value for self.sampled_wave_time"""
        
        self.sampled_wave_time = sampled_wave_time

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj