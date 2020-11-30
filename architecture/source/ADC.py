import Global

class ADC(object):
    def __init__(self, rx_data, sync_obj):
        """Constructor of ADC."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("ADC") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("ADC")
        
        if self.DEBUG:
            print('Running ADC...')
        
        # Data to be transmitted, after modulation.
        self.rx_data_in = rx_data
        
        # Flag to indicate use of circuit simulation.
        self.rounding_or_simul = Global.bypass_dict["ADC_rounding_or_simul"]
        
        
    def convertsToDigital(self):
        """Converts the analog to digital values. Can employ circuit simulation. Outputs 'dac_rx_data'."""
        
        self.sync_obj.appendToSimulationPath("convertsToDigital @ ADC")
        
        # Set previous for debug
        self.sync_obj.setPrevious("ADC")
        
        # Starts the list of DAC
        self.adc_rx_data_list = []
        
        # To choose between ronding or circuit simulation
        if self.rounding_or_simul: # if rouding
            
            # for each ofdm symbol in the list, do the rounding
            for rx_symbol in self.rx_data_in:
                
                # TODO -- Quantization for ADC
                Warning (f"\n\n***Warning --> Still not done quantization for ADC!\n")
                
                self.adc_rx_data_list.append(abs(rx_symbol))
                
            pass
        else: # if circuit simulation
            raise ValueError(f"\n\n***Error --> Circuit simulation for DAC not supported yet, at bypass_dict['DAC_rounding_or_simul'] = <{Global.bypass_dict['DAC_rounding_or_simul']}>!\n")
        
    def getAdcRxData(self):
        """Returns value of self.adc_rx_data_list"""
        
        return self.adc_rx_data_list

    def setAdcRxData(self, adc_rx_data_list):
        """Set new value for self.adc_rx_data_list"""
        
        self.adc_rx_data_list = adc_rx_data_list
    
    def getRxDataIn(self):
        """Returns value of self.rx_data_in"""
        
        return self.rx_data_in

    def setRxDataIn(self, rx_data_in):
        """Set new value for self.rx_data_in"""
        
        self.rx_data_in = rx_data_in

    def getCircuitSimulation(self):
        """Returns value of self.circuit_simulation"""
        
        return self.circuit_simulation

    def setCircuitSimulation(self, circuit_simulation):
        """Set new value for self.circuit_simulation"""
        
        self.circuit_simulation = circuit_simulation

    def getBypass(self):
        """Returns value of self.bypass"""
        
        return self.bypass

    def setBypass(self, bypass):
        """Set new value for self.bypass"""
        
        self.bypass = bypass
