from OFDM import OFDM

# # from OOK import OOK

import generalLibrary as lib

import numpy as np

import Global

from generalLibrary import timer_dec, sync_track

from generalLibrary import printDebug, plotDebug

from scipy import signal

from scipy.signal import correlate

class Modulator(object):
    
    def __init__(self, is_sync, bitstream_frame, modulation_config, mapping_config, mapping_pilot_config, symbol_duration, sync_obj):
        """Constructor of Modulator. It's also the demodulator."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Modulator") or self.sync_obj.getDebug("all")

        self.PLOT = self.sync_obj.getPlot("Modulator") or self.sync_obj.getPlot("all")
        
        self.sync_obj.appendToSimulationPath("Modulator")
        
        if self.DEBUG:
            print('Running Modulator...')
        
        # Bitstream info for transmission, depending on number of frames.
        self.bitstream_frame = bitstream_frame
        
        # Flag that indicates if current symbol is for sync purposes.
        self.is_sync = is_sync
        
        # Modulation config to be applied.
        self.modulation_config = modulation_config
        
        # Sample frequency, depending on the modulation type
        self.sample_frequency = None
        
        # Mapping config to be applied on data.
        self.mapping_config = mapping_config
        
        # Mapping config to be applied on pilots.
        self.mapping_pilot_config = mapping_pilot_config

        # Duration (in s) for the current symbol for tx
        self.symbol_duration = symbol_duration
        
        # Size of current frame to be transmitted.
        self.frame_size = len(bitstream_frame)
        
        # # Number of bits per symbol, before mapping.
        # self.bits_per_symbol = mapping_config[1]
        
        # # Array with all symbols converted from the input bitstream.
        # self.mapped_info = None

        # Has the shape of the input mapped info.
        self.mapped_shape = None

        # Type of modulation to be applied in mapped data.
        self.modulation_type = modulation_config["type"]
        
        # Object for OFDM modulation, if appliable.
        self.ofdm_obj = None
        
        # Object for OOK modulation, if appliable.
        self.ook_obj = None
        
        # List of data to be transmitted.
        self.tx_data_list = []
    
    @sync_track
    def createModulator(self):
        """Create modulator object, depending on type chosen."""
        
        if self.modulation_type == "OFDM":

            # Check number of pilots, if not for sync (where all carriers are for synchronization.)
            if len(self.modulation_config['pilots']) < 2 and not self.is_sync:
                raise ValueError(f"\n\n***Error --> Number of pilots < {self.modulation_config['pilots']} > should be 2 or more (unless if symbol is for sync purposes)!\n")
            
            self.ofdm_obj = OFDM(
                bitstream_frame = self.bitstream_frame,
                modulation_config = self.modulation_config,
                mapping_config = self.mapping_config,
                mapping_pilot_config = self.mapping_pilot_config,
                ofdm_duration = self.symbol_duration,
                sync_obj = self.sync_obj
            )
            
        elif self.modulation_type == "OOK":
            
            printDebug(self.bitstream_frame)
            PAUSE
            self.ook_obj = None
            
            raise ValueError(f"\n\n***Error --> OOK not supported yet: <{self.modulation_type}>!\n")
        
        else:
            raise ValueError(f"\n\n***Error --> Not supported modulation_type: <{self.modulation_type}>!\n")
            

    @sync_track
    def applyModulation(self, decoded_sequence = None, seq_idx = None):
        """Applies the modulation on the frame to send, and returns the 'tx_data_list'."""
        
        if not Global.bypass_dict['Modulator']:
        
            if self.modulation_type == "OFDM":
                
                # Before modulation, we need to setup the carrier indexes.
                self.ofdm_obj.setupOFDMCarriersIndexes()

                # Get more pre-calculated info to be used at RX side
                decoded_sequence['seq_pilot_carriers'].append(self.ofdm_obj.getPilotCarriers())
                decoded_sequence['seq_all_carriers'].append(self.ofdm_obj.getSubCarriers())
                decoded_sequence['seq_data_carriers'].append(self.ofdm_obj.getDataCarriers())
                decoded_sequence['seq_number_of_data_carriers'].append(self.ofdm_obj.getNumberOfDataCarriers())
                
                # Apply OFDM modulation
                self.ofdm_obj.applyModulation(
                    decoded_sequence = decoded_sequence,
                    seq_idx = seq_idx
                )

                # if self.modulation_config['IM_DD']:
                #     # Apply OFDM modulation for IM/DD
                #     self.ofdm_obj.applyModulationIMDD()
                # else:
                #     # Apply OFDM modulation
                #     self.ofdm_obj.applyModulation()
                    
                # Get number of packets to be sent
                temp = self.sync_obj.getMessageDict().copy()
                temp["packets"][-1] = temp["packets"][-1] + len(self.ofdm_obj.getBitstreamList())
                self.sync_obj.setMessageDict(temp)
                
                # Returns a list of OFDM symbols to be transmitted. The input stream data is
                # splitted into various symbols, depending on the throughput of the modulator.
                self.tx_data_list = self.ofdm_obj.getOFDMSymbolList()

                # make sure data is non-negative fo IM/DD
                if self.modulation_config['IM_DD']:
                    self.tx_data_list = [lib.zeroClip(tx_data) \
                            for tx_data in self.tx_data_list]

                # Set the sample frequency for this modulation.
                # self.sample_frequency = (self.ofdm_obj.getNumberOfCarriers() + self.ofdm_obj.getNumberOfPilots()) / Global.time_frame
                self.sample_frequency = self.ofdm_obj.getSampleFrequency()
                
                printDebug(self.sample_frequency/1e6)
                
            elif self.modulation_type == "OOK":
                
                # printDebug(self.bitstream_frame)
                # PAUSE
                # Set the sample frequency for this modulation.
                self.sample_frequency = None
                pass
            
            else:
                raise ValueError(f"\n\n***Error --> Not supported modulation_type: <{self.modulation_type}>!\n")
        
        else:
            # # Bypass Modulator entirely
            # self.tx_data_list = list(np.array(self.bitstream_frame))
            
            raise ValueError(f"\n\n***Error --> Bypass 'Modulator' not implemented yet!\n")
        
    

    @sync_track
    def applyDeModulation(self, decoded_sequence = None, seq_idx = None, rx_data_synced = False, delay_time = 0, delay_steps = 0):
        """Applies the de-modulation on the received info 'rx_data', and returns the symbols"""

        if self.modulation_type == "OFDM":
            
            # # Before de-modulation, we need to setup the rx_data.
            # self.ofdm_obj.setOFDMRxData(self.rx_data)
            # self.ofdm_obj.setOFDMTime(self.rx_time)
            
            
            # # Set the actual channel responses, for further comparissons with estimated ones
            # self.ofdm_obj.setListOfChannelResponses(
            #     self.list_of_channel_response
            # )
            
            # printDebug(decoded_sequence['seq_sync'])

            # Check if data is not synced yet. Then, sync it.
            if not rx_data_synced:
                if decoded_sequence['seq_sync'][seq_idx] is not None:
                    # Sync data first, before actual demodulation. Get next sequence index after that.
                    delay_time, delay_steps = self.syncRxData(
                        decoded_sequence = decoded_sequence,
                        seq_idx = seq_idx
                    )
                    # printDebug(delay_time)
                    # printDebug(delay_steps)
                    rx_data_synced = True
                else:
                    # Check if any of the subfields in the sequence are "True" for "sync". If so, raise error, that the first subfield should be the sync one.
                    # We get here, only if the first subfield is None. Also, we "allow" that there is no sync data at all. This can be used when delay is not significant, or for testing.
                    if [sync for sync in decoded_sequence['seq_sync'] if sync] != []:
                        raise ValueError(f"\n\n***Error --> Should use the first symbol as sync data: {decoded_sequence['seq_sync']}\n")
                
                # indicates that this subfield was used for data sync. So, no actual binary data returned.
                decoded_sequence['rx_data'].append('sync')

            else:
            # if decoded_sequence['seq_sync'][seq_idx] is None:

                # Shift rx data by delay value calculated in previous sequence steps
                self.rx_data = np.roll(self.rx_data, -delay_steps)

                # If not at 'sync' subfield, then get only the part of data related to currente sequence data.
                min_r = int(decoded_sequence['seq_start_time'][seq_idx] * self.sample_frequency)
                max_r = int(decoded_sequence['seq_end_time'][seq_idx] * self.sample_frequency)

                # Before de-modulation, we need to setup the rx_data, with range related to current sequence data
                self.ofdm_obj.setOFDMRxData(self.rx_data[min_r:max_r])
                self.ofdm_obj.setOFDMTime(self.rx_time[min_r:max_r])
                
                # Set the actual channel responses, for further comparissons with estimated ones
                self.ofdm_obj.setListOfChannelResponses(
                    self.list_of_channel_response
                )
                

                # # If data is already synced
                # modulation_config = decoded_sequence['seq_mod'][seq_idx]

                # Apply OFDM De-modulation
                self.ofdm_obj.applyDeModulation(
                    decoded_sequence = decoded_sequence,
                    seq_idx = seq_idx
                )

                # Get the RX reconstructed frame data
                self.rx_bitstream_frame = self.ofdm_obj.getBitstreamFrame()

                decoded_sequence['rx_data'].append(self.rx_bitstream_frame) ### TODO --- Add decoded data to decoded sequence
                
                
                # if self.modulation_config['IM_DD']:
                #     # Apply OFDM De-modulation for IM/DD
                #     self.ofdm_obj.applyDeModulationIMDD()
                # else:
                #     # Apply OFDM De-modulation
                #     self.ofdm_obj.applyDeModulation()
                
                
            
            
        elif self.modulation_type == "OOK":
            
            # self.rx_data_list
            pass
        
        else:
            raise ValueError(f"\n\n***Error --> Not supported modulation_type: <{self.modulation_type}>!\n")

        return rx_data_synced, delay_time, delay_steps
        
    @sync_track
    # @timer_dec
    def syncRxData(self, decoded_sequence = None, seq_idx = None):
        """Get tx_data info to do cross-correlation, and find actual phase delay. The tx_data is supposed here to be generated at the rx end, where we know the pattern."""

        # Get original tx_data and time for current 'seq_idx'.
        # This is the equivalent of the RX side re-creating the expected sync data for synchronization.
        tx_data = decoded_sequence['tx_wave_list'][seq_idx]
        tx_time = decoded_sequence['tx_time_list'][seq_idx]
        # Samples it as it's done at the ADC/DAC levels... b/c we need both tx and rx at the same time frames for cross-correlation
        tx_data, tx_time = lib.sampleSignal(tx_data, tx_time, self.sample_frequency)
        
        # Get positions for min and max time points for current sequence
        min_r = int(decoded_sequence['seq_start_time'][seq_idx] * self.sample_frequency)
        max_r = int(decoded_sequence['seq_end_time'][seq_idx] * self.sample_frequency)

        # Get range for ofdm rx signal for sync.
        rx_data = self.rx_data[min_r:max_r]

        # # get gradients of signals. # TODO --- Actually need gradients?
        # s0 = np.gradient(np.gradient(rx_data))
        # s1 = np.gradient(np.gradient(tx_data))
        s0 = rx_data
        s1 = tx_data
        # get max argument for cross-correlatin betwwen rx_data and tx_data
        # max_arg = np.argmax(signal.correlate(s1, s0)) + 1 ## +1 for most correct cross-correlation
        max_arg = np.argmax(signal.correlate(s1, s0)) + 0
        # max_arg = np.argmax(signal.correlate(s1, s0)) + 1

        # Get delay in steps for given rx wave
        if len(tx_data) > max_arg:
            self.phase_delay_steps = len(tx_data) - max_arg
        else:
            raise ValueError(f"\n\n***Error --> Delay is too large to be synced...\n")
            printDebug(max_arg/self.sample_frequency)
            printDebug(len(tx_data)/self.sample_frequency)
            self.phase_delay_steps = -max_arg-1 + len(tx_data)
            # self.phase_delay_steps = max_arg
        
        self.phase_delay_time = 0
        self.phase_delay_steps = 0

        # Get delay in time for given rx wave
        self.phase_delay_time = self.phase_delay_steps/self.sample_frequency
        
        if self.PLOT:
            sync_data = np.roll(rx_data, -self.phase_delay_steps)
            diff_error = sync_data - tx_data
            plotDebug(tx_data, self.rx_time[min_r:max_r], symbols='bo-.', hold=True)
            plotDebug(rx_data, self.rx_time[min_r:max_r], symbols='ro-', hold=True)
            plotDebug(sync_data, self.rx_time[min_r:max_r], symbols='mo-', hold=True)
            plotDebug(diff_error, self.rx_time[min_r:max_r], symbols='ko-', title="Synchronization of Rx data")
        
        if self.PLOT:
            plotDebug(self.rx_data, self.rx_time, symbols='ro-', hold=True)
        
        # Now, sync whole OFDM data, with given discovered phase delay.
        self.rx_data = np.roll(self.rx_data, -self.phase_delay_steps)
        
        if self.PLOT:
            plotDebug(self.rx_data, self.rx_time, symbols='bo-', title="Original (red) and synced (blue) busrt RX signal.")


        # Returns calculated delay.
        return self.phase_delay_time, self.phase_delay_steps

    @sync_track
    def getBitstreamFrame(self):
        """Returns value of self.bitstream_frame"""
        
        # self.sync_obj.appendToSimulationPath("getBitstreamFrame @ Modulator")
        
        return self.bitstream_frame

    @sync_track
    def setBitstreamFrame(self, bitstream_frame):
        """Set new value for self.bitstream_frame"""
        
        # self.sync_obj.appendToSimulationPath("setBitstreamFrame @ Modulator")
        
        self.bitstream_frame = bitstream_frame

    @sync_track
    def getRxBitstreamFrame(self):
        """Returns value of self.rx_bitstream_frame"""
        
        # self.sync_obj.appendToSimulationPath("getRxBitstreamFrame @ Modulator")
        
        return self.rx_bitstream_frame

    @sync_track
    def setRxBitstreamFrame(self, rx_bitstream_frame):
        """Set new value for self.rx_bitstream_frame"""
        
        # self.sync_obj.appendToSimulationPath("setRxBitstreamFrame @ Modulator")
        
        self.rx_bitstream_frame = rx_bitstream_frame

    @sync_track
    def getModulationConfig(self):
        """Returns value of self.modulation_config"""
        
        return self.modulation_config

    @sync_track
    def setModulationConfig(self, modulation_config):
        """Set new value for self.modulation_config"""
        
        self.modulation_config = modulation_config

    @sync_track
    def getSampleFrequency(self):
        """Returns value of self.sample_frequency"""
        
        return self.sample_frequency

    @sync_track
    def setSampleFrequency(self, sample_frequency):
        """Set new value for self.sample_frequency"""
        
        self.sample_frequency = sample_frequency

    @sync_track
    def getMappedConfig(self):
        """Returns value of self.mapping_config"""
        
        return self.mapping_config

    @sync_track
    def setMappedConfig(self, mapping_config):
        """Set new value for self.mapping_config"""
        
        self.mapping_config = mapping_config

    # @sync_track
    # def getMappedInfo(self):
    #     """Returns value of self.mapped_info"""
        
    #     return self.mapped_info

    # @sync_track
    # def setMappedInfo(self, mapped_info):
    #     """Set new value for self.mapped_info"""
        
    #     self.mapped_info = mapped_info

    @sync_track
    def getMappedShape(self):
        """Returns value of self.mapped_shape"""
        
        return self.mapped_shape

    @sync_track
    def setMappedShape(self, mapped_shape):
        """Set new value for self.mapped_shape"""
        
        self.mapped_shape = mapped_shape

    @sync_track
    def getBitsPerSymbol(self):
        """Returns value of self.bits_per_symbol"""
        
        return self.bits_per_symbol

    @sync_track
    def setBitsPerSymbol(self, bits_per_symbol):
        """Set new value for self.bits_per_symbol"""
        
        self.bits_per_symbol = bits_per_symbol

    @sync_track
    def getFrameSize(self):
        """Returns value of self.frame_size"""
        
        return self.frame_size

    @sync_track
    def setFrameSize(self, frame_size):
        """Set new value for self.frame_size"""
        
        self.frame_size = frame_size

    @sync_track
    def getModulationType(self):
        """Returns value of self.modulation_type"""
        
        return self.modulation_type

    @sync_track
    def setModulationType(self, modulation_type):
        """Set new value for self.modulation_type"""
        
        self.modulation_type = modulation_type

    @sync_track
    def getTxDataList(self):
        """Returns value of self.tx_data_list"""
        
        # self.sync_obj.appendToSimulationPath("getTxDataList @ Modulator")
        
        return self.tx_data_list

    @sync_track
    def setTxDataList(self, tx_data_list):
        """Set new value for self.tx_data_list"""
        
        # self.sync_obj.appendToSimulationPath("setTxDataList @ Modulator")
        
        self.tx_data_list = tx_data_list

    @sync_track
    def getRxData(self):
        """Returns value of self.rx_data"""
        
        return self.rx_data

    @sync_track
    def setRxData(self, rx_data):
        """Set new value for self.rx_data"""
        
        self.rx_data = rx_data
    
    @sync_track
    def getRxTime(self):
        """Returns value of self.rx_time"""
        
        return self.rx_time

    @sync_track
    def setRxTime(self, rx_time):
        """Set new value for self.rx_time"""
        
        self.rx_time = rx_time

    @sync_track
    def getListOfChannelResponses(self):
        """Returns value of self.list_of_channel_response"""
        
        # self.sync_obj.appendToSimulationPath("getListOfChannelResponses @ Modulator")
        
        return self.list_of_channel_response

    @sync_track
    def setListOfChannelResponses(self, list_of_channel_response):
        """Set new value for self.list_of_channel_response"""
        
        # self.sync_obj.appendToSimulationPath("setListOfChannelResponses @ Modulator")
        
        self.list_of_channel_response = list_of_channel_response

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj