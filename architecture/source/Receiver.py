from Detector import Detector

from ROIC import ROIC

from BouncingPixel import BouncingPixel

# from APS import APS

import Global

class Receiver(object):
    def __init__(self, receiver_config, roic_config, rx_data_list, sync_obj):
        """Constructor of receiver. Receives a array of lights."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug()
        
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
        

    def createAllDetectors(self):
        """Get the receiver_config, and for each position (each dict), create a different detector array."""
        
        self.sync_obj.appendToSimulationPath("createAllDetectors @ Receiver")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Receiver")
        
        # start all_detector_array
        self.all_detector_arrays = []
        
        # For each detector array, get its dictionary
        for detector_array_dict in self.receiver_config:
            
            # start detector_array
            detector_array = []
            
            # For each detector in the detector array
            for idx in range(0, len(detector_array_dict["detector_type"])):
                
                # Set previous for debug
                self.sync_obj.setPrevious("Receiver")
                
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
            
            
    def createDetector(self, detector_type, position, angle):
        """Create a detector array, i.e. an array of Detector objects."""
        
        self.sync_obj.appendToSimulationPath("createDetector @ Receiver")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Receiver")
            
        # Create detector object
        detector_obj = Detector(
            detector_type = detector_type,
            position = position,
            angle = angle,
            sync_obj = self.sync_obj
        )
        
        return detector_obj
    
    def calculatesPhotocurrent(self):
        """Calculates what is the photocurrent provided for each time step, as rx_photocurrent_list."""
        
        self.sync_obj.appendToSimulationPath("calculatesPhotocurrent @ Receiver")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Receiver")
        
        # If not bypassing the detector, calculate photocurrent based on it.
        if not Global.bypass_dict["Detector"]:
            
            # Create all configured detectors, and pass the input info to all of them.
            self.createAllDetectors()
            
            # TODO -- DO SOME CALCULATIONS BASED ON DETECTORS
            
            # Calculates photocurrent for all detectors
            for detector_arrays in self.all_detector_arrays:
                for detector in detector_arrays:
                    
                    # Set previous for debug
                    self.sync_obj.setPrevious("Receiver")
                    
                    # do conversion to photocurrent
                    self.rx_photocurrent_list = detector.convertsToPhotocurrent(self.rx_data_in_list)
            
            raise ValueError(f"\n\n***Error --> Simulation for detectors not supported yet, at bypass_dict['Detector'] = <{Global.bypass_dict['Detector']}>!\n")
        else:
            # If bypassing, just pass the rx data list
            self.rx_photocurrent_list = self.rx_data_in_list
        
    def createAllROIC(self):
        """Get the roic_config, and for each position create a different roic array."""
        
        self.sync_obj.appendToSimulationPath("createAllROIC @ Receiver")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Receiver")
        
        # start all_roic_array
        self.all_roic_arrays = []
        
        # For each roic array, get its dictionary
        for roic_array_dict in self.roic_config:
            
            # start roic_array
            roic_array = []
            
            # For each roic in the roic array
            for idx in range(0, len(roic_array_dict["circuit_type"])):
                
                # Set previous for debug
                self.sync_obj.setPrevious("Receiver")
                
                # Create array of roics
                roic_array.append(
                    self.createROIC(
                        circuit_type = roic_array_dict["circuit_type"][idx]
                    )
                )
                
            # List of all roic arrays
            self.all_roic_arrays.append(roic_array)
            
            
    def createROIC(self, circuit_type):
        """Create a ROIC array, i.e. an array of ROIC objects."""
        
        self.sync_obj.appendToSimulationPath("createROIC @ Receiver")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Receiver")
        
        if circuit_type == "BouncingPixel":
        
            roic_obj = BouncingPixel(
                sync_obj = self.sync_obj
            )

        elif circuit_type == "APS":
            
            raise ValueError(f"\n\n***Error --> APS not supported yet!\n")
            
        else:
            raise ValueError(f"\n\n***Error --> circuit_type < {circuit_type} > is not supported!\n")
        
        return roic_obj
        
    def calculatesOutVoltage(self):
        """Calculates what is the voltage associated with each photocurrent provided for each time step, as rx_voltage."""
        
        self.sync_obj.appendToSimulationPath("calculatesOutVoltage @ Receiver")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Receiver")
        
        # If not bypassing the detector, calculate photocurrent based on it.
        if not Global.bypass_dict["ROIC"]:
            
            # Create all ROICS detectors, and pass the input info to all of them.
            self.createAllROIC()
            
            # TODO -- DO SOME CALCULATIONS BASED ON ROICS
            
            # Calculates voltage for all roics
            for roic_arrays in self.all_roic_arrays:
                for roic in roic_arrays:
                    
                    # Set previous for debug
                    self.sync_obj.setPrevious("Receiver")
                    
                    # list of lists for all waves
                    all_waves = roic.convertsToWaves(self.rx_photocurrent_list)
                    
                    # Set previous for debug
                    self.sync_obj.setPrevious("Receiver")
                    
                    if roic.getCircuitType() == "BouncingPixel":
                        
                        # gets the list of voltage signals for the Bouncing Pixel
                        self.rx_voltage_list = roic.calculatesReconstructedVoltage(all_waves)

                    elif roic.getCircuitType() == "APS":
                        
                        raise ValueError(f"\n\n***Error --> APS not supported yet!\n")
                        # # gets the list of voltage signals for the APS
                        # self.rx_voltage_list = roic.APS_FUNTION(all_waves)
                        
                    else:
                        raise ValueError(f"\n\n***Error --> circuit_type < {roic.getCircuitType()} > is not supported!\n")
            
            raise ValueError(f"\n\n***Error --> Simulation for ROICs not supported yet, at bypass_dict['ROIC'] = <{Global.bypass_dict['ROIC']}>!\n")
        
        else:
            # If bypassing, just pass the rx photocurrent list
            self.rx_voltage_list = self.rx_photocurrent_list
    

    def applyADC(self):
        """Converts rx_voltage into adc values, given input rx_voltage."""
        
        self.sync_obj.appendToSimulationPath("applyADC @ Receiver")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Receiver")
        
        # if not bypassing adc
        if not Global.bypass_dict["ADC"]:
            
            # Creates ADC object
            self.adc_obj = ADC
            (
                rx_data = self.rx_voltage_list,
                sync_obj = self.sync_obj
            )
            
            # Set previous for debug
            self.sync_obj.setPrevious("Receiver")
            
            # Converts the 'rx_data' list into 'dac_rx_data' list
            self.adc_obj.convertsToDigital()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Receiver")
            
            # Get the list of dac rx_data
            self.adc_rx_data_list = self.adc_obj.getAdcRxData()
            
        else:
            # Bypass DAC
            self.adc_rx_data_list = self.rx_voltage_list
            
            

    def getReceiverConfig(self):
        """Returns value of self.receiver_config"""
        
        return self.receiver_config

    def setReceiverConfig(self, receiver_config):
        """Set new value for self.receiver_config"""
        
        self.receiver_config = receiver_config

    def getRxDataInList(self):
        """Returns value of self.rx_data_in_list"""
        
        return self.rx_data_in_list

    def setRxDataInList(self, rx_data_in_list):
        """Set new value for self.rx_data_in_list"""
        
        self.rx_data_in_list = rx_data_in_list
    
    def getRxPhotocurrentList(self):
        """Returns value of self.rx_photocurrent_list"""
        
        return self.rx_photocurrent_list

    def setRxPhotocurrentList(self, rx_photocurrent_list):
        """Set new value for self.rx_photocurrent_list"""
        
        self.rx_photocurrent_list = rx_photocurrent_list
    
    def getAdcRxDataList(self):
        """Returns value of self.adc_rx_data_list"""
        
        return self.adc_rx_data_list

    def setAdcRxDataList(self, adc_rx_data_list):
        """Set new value for self.adc_rx_data_list"""
        
        self.adc_rx_data_list = adc_rx_data_list
