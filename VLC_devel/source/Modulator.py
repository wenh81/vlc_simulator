from OFDM import OFDM

# # from OOK import OOK

import numpy as np

import Global

from generalLibrary import timer_dec, sync_track

class Modulator(object):
    
    def __init__(self, bitstream_frame, modulation_config, mapping_config, sync_obj):
        """Constructor of Modulator. It's also the demodulator."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Modulator") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Modulator")
        
        if self.DEBUG:
            print('Running Modulator...')
        
        # Bitstream info for transmission, depending on number of frames.
        self.bitstream_frame = bitstream_frame
        
        # Modulation config to be applied.
        self.modulation_config = modulation_config
        
        # Mapping config to be applied.
        self.mapping_config = mapping_config
        
        # Size of current frame to be transmitted.
        self.frame_size = len(bitstream_frame)
        
        # Number of bits per symbol, before mapping.
        self.bits_per_symbol = mapping_config[1]
        
        # Array with all symbols converted from the input bitstream.
        self.mapped_info = None

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
        
        # self.sync_obj.appendToSimulationPath("createModulator @ Modulator")
        
            
        if self.modulation_type == "OFDM":
            
            self.ofdm_obj = OFDM(
                bitstream_frame = self.bitstream_frame,
                modulation_config = self.modulation_config,
                mapping_config = self.mapping_config,
                mapped_info = self.mapped_info,
                sync_obj = self.sync_obj
            )
            
        elif self.modulation_type == "OOK":
            
            pass
        
        else:
            raise ValueError(f"\n\n***Error --> Not supported modulation_type: <{self.modulation_type}>!\n")
            

    @sync_track
    def applyModulation(self):
        """Applies the modulation on the frame to send, and returns the 'tx_data_list'."""
        
        # self.sync_obj.appendToSimulationPath("applyModulation @ Modulator")
        
        if not Global.bypass_dict['Modulator']:
        
            if self.modulation_type == "OFDM":
                
                # Before modulation, we need to setup the carrier inexes.
                self.ofdm_obj.setupOFDMCarriersIndexes()
                
                if Global.IM_DD:
                    # Apply OFDM modulation for IM/DD
                    self.ofdm_obj.applyModulationIMDD()
                else:
                    # Apply OFDM modulation
                    self.ofdm_obj.applyModulation()
                    
                # Get number of packets to be sent
                temp = self.sync_obj.getMessageDict().copy()
                temp["packets"][-1] = temp["packets"][-1] + len(self.ofdm_obj.getBitstreamList())
                self.sync_obj.setMessageDict(temp)
                
                
                # Returns a list of OFDM symbols to be transmitted. The input stream data is
                # splitted into various symbols, depending on the throughput of the modulator.
                self.tx_data_list = self.ofdm_obj.getOFDMSymbolList()
                
            elif self.modulation_type == "OOK":
                
                pass
            
            else:
                raise ValueError(f"\n\n***Error --> Not supported modulation_type: <{self.modulation_type}>!\n")
        
        else:
            # # Bypass Modulator entirely
            # self.tx_data_list = list(np.array(self.bitstream_frame))
            
            raise ValueError(f"\n\n***Error --> Bypass 'Modulator' not implemented yet!\n")
        
    

    @sync_track
    def applyDeModulation(self):
        """Applies the de-modulation on the received info 'rx_data_list', and returns the symbols"""
        
        # self.sync_obj.appendToSimulationPath("applyDeModulation @ Modulator")
        
        
        if self.modulation_type == "OFDM":
            
            # Before de-modulation, we need to setup the rx_data_list.
            self.ofdm_obj.setOFDMRxDataList(self.rx_data_list)
            
            
            # Set the actual channel responses, for further comparissons with estimated ones
            self.ofdm_obj.setListOfChannelResponses(
                self.list_of_channel_response
            )
            
            
            # Apply OFDM De-modulation
            self.ofdm_obj.applyDeModulation()
            
            
            # Get the RX reconstructed frame data
            self.rx_bitstream_frame = self.ofdm_obj.getBitstreamFrame()
            
            
        elif self.modulation_type == "OOK":
            
            pass
        
        else:
            raise ValueError(f"\n\n***Error --> Not supported modulation_type: <{self.modulation_type}>!\n")
        
        
        

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
    def getMappedConfig(self):
        """Returns value of self.mapping_config"""
        
        return self.mapping_config

    @sync_track
    def setMappedConfig(self, mapping_config):
        """Set new value for self.mapping_config"""
        
        self.mapping_config = mapping_config

    @sync_track
    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        return self.mapped_info

    @sync_track
    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.mapped_info = mapped_info

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
    def getRxDataList(self):
        """Returns value of self.rx_data_list"""
        
        # self.sync_obj.appendToSimulationPath("getRxDataList @ Modulator")
        
        return self.rx_data_list

    @sync_track
    def setRxDataList(self, rx_data_list):
        """Set new value for self.rx_data_list"""
        
        # self.sync_obj.appendToSimulationPath("setRxDataList @ Modulator")
        
        self.rx_data_list = rx_data_list

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