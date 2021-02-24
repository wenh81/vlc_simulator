from generalLibrary import timer_dec, sync_track

from Detector import Detector

from ROIC import ROIC

from ADC import ADC

from BouncingPixel import BouncingPixel

# from APS import APS

import numpy as np

import Global

from generalLibrary import printDebug, plotDebug

class Receiver(object):
    
    def __init__(self, receiver_config, roic_config, rx_data_list, sync_obj):
        """Constructor of receiver. Receives a array of lights."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Receiver") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Receiver")
        
        if self.DEBUG:
            print('Running Receiver...')
        
        # Contains list of dicts with all information needed to configure the detectors on the receiver. Each position has a dict, with the type of detector, the position for each detector, and angle. Can be used to configure more than one array of detectors.
        self.receiver_config = receiver_config
        
        # Contains list of dicts with all information needed to configure the ROICs on the receiver. Each position has a dict, with the type of ROIC, associated with each corresponding detector. Can be used to configure more than one array of ROICs.
        self.roic_config = roic_config
        
        # Data must to be received, after the channel.
        self.rx_data_in_list = rx_data_list
        
        # rx data list for all photocurrents
        self.rx_photocurrent_list = []
        
        # Defines the simulator to be used, if appliable.
        self.which_simulator = Global.which_simulator
        

    @sync_track
    def createAllDetectors(self):
        """Get the receiver_config, and for each position (each dict), create a different detector array."""
        
        
        
        # start all_detector_array
        self.all_detector_arrays = []
        
        # For each detector array, get its dictionary
        for detector_array_dict in self.receiver_config:
            
            # start detector_array
            detector_array = []
            
            # For each detector in the detector array
            for idx in range(0, len(detector_array_dict["detector_type"])):
                
                
                # Create array of detectors
                detector_array.append(
                    self.createDetector(
                        detector_type = detector_array_dict["detector_type"][idx],
                        position = detector_array_dict["position"][idx],
                        angle = detector_array_dict["angle"][idx]
                    )
                )
                
            # List of all detector arrays
            self.all_detector_arrays.append(detector_array)
            
            
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
    
    @sync_track
    def calculatesPhotocurrent(self):
        """Calculates what is the photocurrent provided for each time step, as rx_photocurrent_list."""
        
        
        
        # If not bypassing the detector, calculate photocurrent based on it.
        if not Global.bypass_dict["Detector"]:
            
            # Create all configured detectors, and pass the input info to all of them.
            self.createAllDetectors()
            
            # TODO -- DO SOME CALCULATIONS BASED ON DETECTORS
            
            # Calculates photocurrent for all detectors
            for detector_arrays in self.all_detector_arrays:
                for detector in detector_arrays:
                    
                    
                    # do conversion to photocurrent
                    self.rx_photocurrent_list = detector.convertsToPhotocurrent(self.rx_data_in_list)
            
            raise ValueError(f"\n\n***Error --> Simulation for detectors not supported yet, at bypass_dict['Detector'] = <{Global.bypass_dict['Detector']}>!\n")
        else:
            # If bypassing, just pass the rx data list
            self.rx_photocurrent_list = self.rx_data_in_list
        
    @sync_track
    def createAllROIC(self):
        """Get the roic_config, and for each position create a different roic array."""
        
        # start all_roic_array
        self.all_roic_arrays = []
        
        # For each roic array, get its dictionary
        for roic_array_dict in self.roic_config:
            
            # start roic_array
            roic_array = []
            
            # For each roic in the roic array
            for idx in range(0, len(roic_array_dict["circuit_type"])):
                
                # Create array of roics
                roic_array.append(
                    self.createROIC(
                        circuit_type = roic_array_dict["circuit_type"][idx],
                        gain = roic_array_dict["gain"][idx],
                        circuit_simulation = roic_array_dict["circuit_simulation"][idx],
                        waves_name = roic_array_dict["waves_name"][idx],
                        DR = roic_array_dict["DR"][idx],
                        current_noise = roic_array_dict["current_noise"][idx],
                        SNR = roic_array_dict["SNR"][idx],
                        roic_setup = roic_array_dict["roic_setup"][idx]
                    )
                )
            
            # List of all roic arrays
            self.all_roic_arrays.append(roic_array)
            
            
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
            self.createAllROIC()
            
            # TODO -- DO SOME CALCULATIONS BASED ON ROICS
            
            # Calculates voltage for all roics
            for roic_arrays in self.all_roic_arrays:
                for roic in roic_arrays:
                    
                    # list of lists for all waves (voltage) -- convertsToWaves belongs to ROIC
                    all_waves = roic.convertsToWaves(self.rx_photocurrent_list)
                    
                    if roic.getCircuitType() == "BouncingPixel":
                        
                        # gets the list of voltage signals for the Bouncing Pixel
                        self.rx_voltage_list = roic.calculatesReconstructedVoltage(all_waves)

                    elif roic.getCircuitType() == "APS":
                        
                        raise ValueError(f"\n\n***Error --> APS not supported yet!\n")
                        # # gets the list of voltage signals for the APS
                        # self.rx_voltage_list = roic.APS_FUNTION(all_waves)
                        
                    else:
                        raise ValueError(f"\n\n***Error --> circuit_type < {roic.getCircuitType()} > is not supported!\n")

                    # plotDebug(self.rx_photocurrent_list[0])
                    # self.rx_photocurrent_list = [wave/np.max(self.rx_photocurrent_list) \
                    #     for wave in self.rx_photocurrent_list]
                    
                    # plotDebug(self.rx_photocurrent_list[0])
                    # TODO --- CREATE THE ARRAY FOR EACH ROIC ARRAY....
                    # roic_array_photocurrent.append(self.rx_voltage_list)
            
            # raise ValueError(f"\n\n***Error --> Simulation for ROICs not supported yet, at bypass_dict['ROIC'] = <{Global.bypass_dict['ROIC']}>!\n")
        
        else:
            # If bypassing, just pass the rx photocurrent list
            self.rx_voltage_list = self.rx_photocurrent_list
    

    @sync_track
    def applyADC(self):
        """Converts rx_voltage into adc values, given input rx_voltage."""        
        
        # if not bypassing adc
        if not Global.bypass_dict["ADC"]:
            
            # Creates ADC object
            self.adc_obj = ADC(
                rx_data = self.rx_voltage_list,
                sync_obj = self.sync_obj
            )
            
            
            # Converts the 'rx_data' list into 'dac_rx_data' list
            self.adc_obj.convertsToDigital()
            
            
            # Get the list of dac rx_data
            self.adc_rx_data_list = self.adc_obj.getAdcRxData()
            
        else:
            # Bypass DAC
            self.adc_rx_data_list = self.rx_voltage_list
            
            

    @sync_track
    def getReceiverConfig(self):
        """Returns value of self.receiver_config"""
        
        return self.receiver_config

    @sync_track
    def setReceiverConfig(self, receiver_config):
        """Set new value for self.receiver_config"""
        
        self.receiver_config = receiver_config

    @sync_track
    def getRxDataInList(self):
        """Returns value of self.rx_data_in_list"""
        
        return self.rx_data_in_list

    @sync_track
    def setRxDataInList(self, rx_data_in_list):
        """Set new value for self.rx_data_in_list"""
        
        self.rx_data_in_list = rx_data_in_list
    
    @sync_track
    def getRxPhotocurrentList(self):
        """Returns value of self.rx_photocurrent_list"""
        
        return self.rx_photocurrent_list

    @sync_track
    def setRxPhotocurrentList(self, rx_photocurrent_list):
        """Set new value for self.rx_photocurrent_list"""
        
        self.rx_photocurrent_list = rx_photocurrent_list
    
    @sync_track
    def getAdcRxDataList(self):
        """Returns value of self.adc_rx_data_list"""
        
        return self.adc_rx_data_list

    @sync_track
    def setAdcRxDataList(self, adc_rx_data_list):
        """Set new value for self.adc_rx_data_list"""
        
        self.adc_rx_data_list = adc_rx_data_list

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj