from .common_imports import *


class DAC(object):
    
    def __init__(self, tx_data, time_interval, sync_obj):
        """Constructor of DAC."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        # Get debug and plot flags
        self.DEBUG, self.PLOT = lib.getDebugPlot("DAC", self.sync_obj)
        
        self.sync_obj.appendToSimulationPath("DAC")
        
        if self.DEBUG:
            print('Running DAC...')
        
        # Data to be transmitted, after modulation.
        self.tx_data_in = tx_data
        
        # Time interval for current conversion
        self.time_interval = time_interval

        # Flag to indicate use of circuit simulation.
        self.rounding_or_simul = Global.bypass_dict["DAC_rounding_or_simul"]
        
        
    @sync_track
    def convertsToAnalog(self, offset_value = 0):
        """Converts the digital values to analog. Can employ circuit simulation. Outputs 'dac_tx_data'."""
        
        
        # Starts the list of DAC
        self.dac_tx_data = []
        
        # To choose between ronding or circuit simulation
        if self.rounding_or_simul: # if rouding
            
            max_tx = np.max([np.max(tx_symbol) for tx_symbol in self.tx_data_in])
            min_tx = np.min([np.min(tx_symbol) for tx_symbol in self.tx_data_in])
            # for each ofdm symbol in the list, do the rounding
            for tx_symbol in self.tx_data_in:
                
                # TODO -- Quantization for DAC
                Warning (f"\n\n***Warning --> Still not done quantization for DAC!\n")

                # # Differential Nonlinearity (DNL) Error
                # DNL = ?
                # # Integral Nonlinearity (INL) Error
                # INL = ?
                # DAC gain Error
                DAC_gain_error = 1
                # DAC offset Error
                DAC_gain_offset = 0
                tx_symbol = DAC_gain_error*tx_symbol + DAC_gain_offset

                # number of points in current time interval
                number_of_points = int(self.time_interval/Global.time_step)

                # plotDebug(tx_symbol)
                # Do interpolation (convertion to analog). Zero-hold order.
                tx_symbol = lib.interpolateData(np.arange(0, len(tx_symbol))*self.time_interval/len(tx_symbol), tx_symbol, number_of_points)
                # printDebug(offset_value)
                # printDebug(max_tx)
                # printDebug(min_tx)
                # plotDebug(tx_symbol)

                
                # x = tx_symbol
                # y = voltage
                # y = a*x + b
                # x=min(tx_data) -> vss = a*min + b -> b = vss - a*min
                # x=max(tx_data) -> vdd = a*max + b = a*max + vss - a*min \
                #     -> vdd = a*(max - min) + vss -> a = (vdd - vss)/(max - min)
                # y = a*x + vss - a*min = a*(x - min) + vss -> \
                #     y = (vdd - vss)/(max - min)*(x - min) + vss
                tx_symbol = lib.adjustRange(tx_symbol, \
                    Global.VDD_tx, Global.VSS_tx,\
                        max_tx, min_tx,\
                            offset_value)
                # plotDebug(tx_symbol)
                
                # TODO -- Apply Noise.
                
                # self.dac_tx_data.append(abs(tx_symbol))
                self.dac_tx_data.append(tx_symbol)
                
            pass
        else: # if circuit simulation
            raise ValueError(f"\n\n***Error --> Circuit simulation for DAC not supported yet, at bypass_dict['DAC_rounding_or_simul'] = <{Global.bypass_dict['DAC_rounding_or_simul']}>!\n")
        
        
    @sync_track
    def getTxDataIn(self):
        """Returns value of self.tx_data_in"""
        
        
        return self.tx_data_in

    @sync_track
    def setTxDataIn(self, tx_data_in):
        """Set new value for self.tx_data_in"""
        
        
        self.tx_data_in = tx_data_in
    
    @sync_track
    def getDacTxData(self):
        """Returns value of self.dac_tx_data"""
        
        return self.dac_tx_data

    @sync_track
    def setDacTxData(self, dac_tx_data):
        """Set new value for self.dac_tx_data"""
        
        
        self.dac_tx_data = dac_tx_data
        
        
    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj