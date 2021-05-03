from .common_imports import *


class ADC(object):
    
    def __init__(self, rx_data, rx_time, sample_freq, adc_configuration, sync_obj):
        """Constructor of ADC."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        # Get debug and plot flags
        self.DEBUG, self.PLOT = lib.getDebugPlot("ADC", self.sync_obj)
        
        self.sync_obj.appendToSimulationPath("ADC")
        
        if self.DEBUG:
            print('Running ADC...')
        
        # Data to be received, before demodulation.
        self.rx_data_in = rx_data
        
        # Time of data to be received, before demodulation.
        self.rx_time = rx_time
        
        # Sample frequency for the receiver
        self.sample_freq = sample_freq
        
        # Flag to indicate use of circuit simulation.
        self.rounding_or_simul = Global.bypass_dict["ADC_rounding_or_simul"]

        # Voltage references / number of bits
        self.vref_plus = adc_configuration['vref_plus']
        self.vref_minus = adc_configuration['vref_minus']
        self.n_bits = adc_configuration['n_bits']
        
        
    @sync_track
    def convertsToDigital(self):
        """Converts the analog to digital values. Can employ circuit simulation."""
        
        # To choose between ronding or circuit simulation
        if self.rounding_or_simul: # if rouding
            
            # TODO -- Quantization for ADC
            Warning (f"\n\n***Warning --> Quantization not ready yet for ADC!\n")

            # # Remove negative values
            # self.rx_data_in[self.rx_data_in <= 0] = 0

            # Voltage range
            vcm = (self.vref_plus - self.vref_minus)/(2**(self.n_bits-1))
            # plotDebug(self.rx_data_in, symbols='ro-', hold = True)
            self.rx_data_in = np.round(self.rx_data_in/vcm) * vcm + self.vref_minus
            # self.rx_data_in = np.ceil(self.rx_data_in/vcm) * vcm + self.vref_minus
            printDebug(self.rx_data_in)
            # plotDebug(self.rx_data_in, symbols='bo-')

            # # Differential Nonlinearity (DNL) Error
            # DNL = ?
            # # Integral Nonlinearity (INL) Error
            # INL = ?
            # ADC gain Error
            ADC_gain_error = 1
            # ADC offset Error
            ADC_gain_offset = 0
            self.rx_data_in = ADC_gain_error*self.rx_data_in + ADC_gain_offset
            
            # TODO --- for now, bypassing
            self.adc_rx_data, self.rx_time = lib.sampleSignal(self.rx_data_in, self.rx_time, self.sample_freq)
            
            # # remove zero
            # self.sampled_wave = lib.zeroClip(self.sampled_wave)

        else: # if circuit simulation
            raise ValueError(f"\n\n***Error --> Circuit simulation for DAC not supported yet, at bypass_dict['DAC_rounding_or_simul'] = <{Global.bypass_dict['DAC_rounding_or_simul']}>!\n")
            self.adc_rx_data = self.rx_data_in
            self.rx_time = self.rx_time

        return self.adc_rx_data, self.rx_time
        
    @sync_track
    def getAdcRxData(self):
        """Returns value of self.adc_rx_data"""
        
        return self.adc_rx_data

    @sync_track
    def setAdcRxData(self, adc_rx_data):
        """Set new value for self.adc_rx_data"""
        
        self.adc_rx_data = adc_rx_data
    
    @sync_track
    def getRxDataIn(self):
        """Returns value of self.rx_data_in"""
        
        return self.rx_data_in

    @sync_track
    def setRxDataIn(self, rx_data_in):
        """Set new value for self.rx_data_in"""
        
        self.rx_data_in = rx_data_in

    @sync_track
    def getCircuitSimulation(self):
        """Returns value of self.circuit_simulation"""
        
        return self.circuit_simulation

    @sync_track
    def setCircuitSimulation(self, circuit_simulation):
        """Set new value for self.circuit_simulation"""
        
        self.circuit_simulation = circuit_simulation

    @sync_track
    def getBypass(self):
        """Returns value of self.bypass"""
        
        return self.bypass

    @sync_track
    def setBypass(self, bypass):
        """Set new value for self.bypass"""
        
        self.bypass = bypass
        
    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj