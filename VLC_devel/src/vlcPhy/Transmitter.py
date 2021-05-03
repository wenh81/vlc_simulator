from .common_imports import *


class Transmitter(object):
    
    def __init__(self, transmitter_config, tx_data_list, sync_obj):
        """Constructor of transmitter. Receives a array of lights."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        # Get debug and plot flags
        self.DEBUG, self.PLOT = lib.getDebugPlot("Transmitter", self.sync_obj)
        
        self.sync_obj.appendToSimulationPath("Transmitter")
        
        if self.DEBUG:
            print('Running Transmitter...')
        
        # Contains list of dicts with all information needed to configure the lights on the Transmitter. Each position has a dict, with the type of light, the position for each lamp, and angle. Can be used to configure more than one array of lamps.
        self.transmitter_config = transmitter_config

        # List of data to be transmitted, after modulation.
        self.tx_data_list_in = tx_data_list

        # # Flag to bypass the creation of light sources ????????????????
        # self.bypass = Global.bypass_dict["Transmitter"]
        
        pass
    
    @sync_track
    def createAllLamps(self):
        """Get the transmitter_config, and for each position (each dict), create a different lamp."""
        
        # start all_lamp_array
        self.all_lamp_arrays = []
        
        # For each lamp array, get its dictionary
        for lamp_array_dict in self.transmitter_config:
            
            # start lamp_array
            lamp_array = []
            
            # For each lamp in the lamp array
            for idx in range(0, len(lamp_array_dict["light_type"])):
                
                
                # Create array of lamps
                lamp_array.append(
                    self.createLamp(
                        light_type = lamp_array_dict["light_type"][idx],
                        position = lamp_array_dict["position"][idx],
                        angle = lamp_array_dict["angle"][idx]
                    )
                )
                
            # List of all lamp arrays
            self.all_lamp_arrays.append(lamp_array)
    
    @sync_track
    def createLamp(self, light_type, position, angle):
        """Create a lamp, which is an array of LightSource objects."""
        
        
            
        # Create light source object
        light_obj = LightSource(
            light_type = light_type,
            position = position,
            angle = angle,
            sync_obj = self.sync_obj
        )
        
        return light_obj
    
    
    @sync_track
    def applyFilter(self, filter_order = 20, cuttof = 400e6, filter_type = 'low'):
        """Apply digital filter. Cutoff in Hz."""        
        
        # sig = tx_data
        
        # lib.butterFilter(tx_data, cuttof=100e6)
        # lib.butterFilter(tx_data, cuttof=1e3, filter_type = 'hp')

        # return [lib.butterFilter(tx_data, cuttof=10e6)\
        self.tx_data_list_in = [lib.butterFilter(tx_data, cuttof = cuttof, \
            filter_order = filter_order, filter_type = filter_type)\
            for tx_data in self.tx_data_list_in]
        # return [lib.butterFilter(tx_data, cuttof = cuttof, \
        #     filter_order = filter_order, filter_type = filter_type)\
        #     for tx_data in self.tx_data_list_in]
        
        # for tx_data in self.tx_data_list_in:
            
            # plotDebug(tx_data)
            # output_signal = signal.filtfilt(b, a, tx_data)
            # plotDebug(output_signal)
        

    @sync_track
    def applyDAC(self, offset_value = 0, IM_DD = True, time_interval = None):
        """Converts tx_data into dac values."""
        
        
        # if not bypassing dac
        if not Global.bypass_dict["DAC"]:
            
            # Creates DAC object
            self.dac_obj = DAC(
                tx_data = self.tx_data_list_in,
                time_interval = time_interval,
                sync_obj = self.sync_obj
            )
            # plotDebug(self.tx_data_list_in[0])
            # Converts the 'tx_data' list into 'dac_tx_data' list
            self.dac_obj.convertsToAnalog(offset_value = offset_value)
            
            # Get the list of dac tx_data
            self.dac_tx_data_list = self.dac_obj.getDacTxData()
            
            # plotDebug(self.dac_tx_data_list[0])
        else:
            #### Bypass DAC
            # self.dac_tx_data_list = self.tx_data_list_in
            # plotDebug(self.tx_data_list_in[0])
            max_tx = np.max([np.max(tx_symbol) for tx_symbol in self.tx_data_list_in])
            min_tx = np.min([np.min(tx_symbol) for tx_symbol in self.tx_data_list_in])
            
            # number of points in current time interval
            number_of_points = int(time_interval/Global.time_step)

            # Do interpolation (convertion to analog). Zero-hold order.
            self.dac_tx_data_list = [lib.interpolateData(np.arange(0, len(dac_tx))*time_interval/len(dac_tx), dac_tx, number_of_points) \
                for dac_tx in self.dac_tx_data_list]
            
            # TODO --- Remove offset from here
            
            self.dac_tx_data_list = [lib.adjustRange(tx_symbol,\
                Global.VDD_tx, Global.VSS_rx,\
                    max_tx, min_tx,\
                        offset_value) \
                            for tx_symbol in self.tx_data_list_in]
        
        # TODO --- Remove zero clipping?
        
        # Applies zero clipping (by default, for IM_DD)
        if IM_DD:
            self.dac_tx_data_list = [lib.zeroClip(dac_tx) \
                    for dac_tx in self.dac_tx_data_list]
        
    
    @sync_track
    def calculatesOpticalPower(self):
        """Calculates what is the optical power provided for each time step, as tx_optical (given input dac_values)."""
        
        
        
        # If not bypassing the light source, calculate optical power based on it.
        if not Global.bypass_dict["LightSource"]:
            
            # Create all configured lamps, and pass the input info to all of them.
            # Next, should sum up their impact.
            self.createAllLamps()

            raise ValueError(f"\n\n***Error --> Simulation for light sources not supported yet, at bypass_dict['LightSource'] = <{Global.bypass_dict['LightSource']}>!\n")

            for lamp in self.all_lamp_arrays:

                self.tx_optical_out_list = lamp.convertToOpticalPower(self.dac_tx_data_list)
                
            
            # TODO -- DO SOME CALCULATIONS BASED ON INPUT LIGHT
            ## votlage --> current -[non-linear]-> optical
            # self.tx_optical_out_list = self.dac_tx_data_list
            
        else:

            ## TODO -- Apply gain here for voltage to optical?
            # If bypassing, just pass the dac value forward
            self.tx_optical_out_list = self.dac_tx_data_list
            
            
            
    @sync_track
    def getTransmitterConfig(self):
        """Returns value of self.transmitter_config"""
        
        return self.transmitter_config

    @sync_track
    def setTransmitterConfig(self, transmitter_config):
        """Set new value for self.transmitter_config"""
        
        self.transmitter_config = transmitter_config

    @sync_track
    def getTxDataListIn(self):
        """Returns value of self.tx_data_list_in"""
        
        return self.tx_data_list_in

    @sync_track
    def setTxDataListIn(self, tx_data_list_in):
        """Set new value for self.tx_data_list_in"""
        
        self.tx_data_list_in = tx_data_list_in

    @sync_track
    def getDacTxDataList(self):
        """Returns value of self.dac_tx_data_list"""
        
        return self.dac_tx_data_list

    @sync_track
    def setDacTxDataList(self, dac_tx_data_list):
        """Set new value for self.dac_tx_data_list"""
        
        self.dac_tx_data_list = dac_tx_data_list
    
    @sync_track
    def getTxOpticalOutList(self):
        """Returns value of self.tx_optical_out_list"""
        
        
        return self.tx_optical_out_list

    @sync_track
    def setTxOpticalOutList(self, tx_optical_out_list):
        """Set new value for self.tx_optical_out_list"""
        
        
        self.tx_optical_out_list = tx_optical_out_list
        
    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj