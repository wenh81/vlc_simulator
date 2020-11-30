from OFDM import OFDM

# # from OOK import OOK

import numpy as np

import Global

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
    
        pass

    def createModulator(self):
        """Create modulator object, depending on type chosen."""
        
        self.sync_obj.appendToSimulationPath("createModulator @ Modulator")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Modulator")
            
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
            
    

    def applyModulation(self):
        """Applies the modulation on the frame to send, and returns the 'tx_data_list'."""
        
        self.sync_obj.appendToSimulationPath("applyModulation @ Modulator")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Modulator")
        
        if not Global.bypass_dict['Modulator']:
        
            if self.modulation_type == "OFDM":
                
                # Before modulation, we need to setup the carrier inexes.
                self.ofdm_obj.setupOFDMCarriersIndexes()
                
                # Set previous for debug
                self.sync_obj.setPrevious("Modulator")
                
                # Apply OFDM modulation
                self.ofdm_obj.applyModulation()
                
                # Set previous for debug
                self.sync_obj.setPrevious("Modulator")
                
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
        
    

    def applyDeModulation(self):
        """Applies the de-modulation on the received info 'rx_data_list', and returns the symbols"""
        
        self.sync_obj.appendToSimulationPath("applyDeModulation @ Modulator")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Modulator")
        
        if self.modulation_type == "OFDM":
            
            # Before de-modulation, we need to setup the rx_data_list.
            self.ofdm_obj.setOFDMRxDataList(self.rx_data_list)
            
            # Set previous for debug
            self.sync_obj.setPrevious("Modulator")
            
            # Set the actual channel responses, for further comparissons with estimated ones
            self.ofdm_obj.setListOfChannelResponses(
                self.list_of_channel_response
            )
            
            # Set previous for debug
            self.sync_obj.setPrevious("Modulator")
            
            # Apply OFDM De-modulation
            self.ofdm_obj.applyDeModulation()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Modulator")
            
            # Get the RX reconstructed frame data
            self.rx_bitstream_frame = self.ofdm_obj.getBitstreamFrame()
            
            self.sync_obj.setPrevious("Modulator")
            
        elif self.modulation_type == "OOK":
            
            pass
        
        else:
            raise ValueError(f"\n\n***Error --> Not supported modulation_type: <{self.modulation_type}>!\n")
        
        
        
        
    def getBitstreamFrame(self):
        """Returns value of self.bitstream_frame"""
        
        self.sync_obj.appendToSimulationPath("getBitstreamFrame @ Modulator")
        
        return self.bitstream_frame

    def setBitstreamFrame(self, bitstream_frame):
        """Set new value for self.bitstream_frame"""
        
        self.sync_obj.appendToSimulationPath("setBitstreamFrame @ Modulator")
        
        self.bitstream_frame = bitstream_frame
    
    def getRxBitstreamFrame(self):
        """Returns value of self.rx_bitstream_frame"""
        
        self.sync_obj.appendToSimulationPath("getRxBitstreamFrame @ Modulator")
        
        return self.rx_bitstream_frame

    def setRxBitstreamFrame(self, rx_bitstream_frame):
        """Set new value for self.rx_bitstream_frame"""
        
        self.sync_obj.appendToSimulationPath("setRxBitstreamFrame @ Modulator")
        
        self.rx_bitstream_frame = rx_bitstream_frame

    def getModulationConfig(self):
        """Returns value of self.modulation_config"""
        
        return self.modulation_config

    def setModulationConfig(self, modulation_config):
        """Set new value for self.modulation_config"""
        
        self.modulation_config = modulation_config
        
    def getMappedConfig(self):
        """Returns value of self.mapping_config"""
        
        return self.mapping_config

    def setMappedConfig(self, mapping_config):
        """Set new value for self.mapping_config"""
        
        self.mapping_config = mapping_config
        
    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        return self.mapped_info

    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.mapped_info = mapped_info

    def getMappedShape(self):
        """Returns value of self.mapped_shape"""
        
        return self.mapped_shape

    def setMappedShape(self, mapped_shape):
        """Set new value for self.mapped_shape"""
        
        self.mapped_shape = mapped_shape

    def getBitsPerSymbol(self):
        """Returns value of self.bits_per_symbol"""
        
        return self.bits_per_symbol

    def setBitsPerSymbol(self, bits_per_symbol):
        """Set new value for self.bits_per_symbol"""
        
        self.bits_per_symbol = bits_per_symbol

    def getFrameSize(self):
        """Returns value of self.frame_size"""
        
        return self.frame_size

    def setFrameSize(self, frame_size):
        """Set new value for self.frame_size"""
        
        self.frame_size = frame_size

    def getModulationType(self):
        """Returns value of self.modulation_type"""
        
        return self.modulation_type

    def setModulationType(self, modulation_type):
        """Set new value for self.modulation_type"""
        
        self.modulation_type = modulation_type
    
    def getTxDataList(self):
        """Returns value of self.tx_data_list"""
        
        self.sync_obj.appendToSimulationPath("getTxDataList @ Modulator")
        
        return self.tx_data_list

    def setTxDataList(self, tx_data_list):
        """Set new value for self.tx_data_list"""
        
        self.sync_obj.appendToSimulationPath("setTxDataList @ Modulator")
        
        self.tx_data_list = tx_data_list
    
    def getRxDataList(self):
        """Returns value of self.rx_data_list"""
        
        self.sync_obj.appendToSimulationPath("getRxDataList @ Modulator")
        
        return self.rx_data_list

    def setRxDataList(self, rx_data_list):
        """Set new value for self.rx_data_list"""
        
        self.sync_obj.appendToSimulationPath("setRxDataList @ Modulator")
        
        self.rx_data_list = rx_data_list
    
    def getListOfChannelResponses(self):
        """Returns value of self.list_of_channel_response"""
        
        self.sync_obj.appendToSimulationPath("getListOfChannelResponses @ Modulator")
        
        return self.list_of_channel_response

    def setListOfChannelResponses(self, list_of_channel_response):
        """Set new value for self.list_of_channel_response"""
        
        self.sync_obj.appendToSimulationPath("setListOfChannelResponses @ Modulator")
        
        self.list_of_channel_response = list_of_channel_response
