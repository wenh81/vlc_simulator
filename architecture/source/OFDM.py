import numpy as np

from Mapping import Mapping

import Global

class OFDM(object):
    def __init__(self, bitstream_frame, modulation_config, mapping_config, mapped_info, sync_obj):
        """Constructor of OFDM."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug()
        
        self.sync_obj.appendToSimulationPath("OFDM")
        
        if self.DEBUG:
            print('Running OFDM...')

        # Bitstream info for transmission, depending on number of frames.
        self.bitstream_frame = bitstream_frame
        
        # Mapping config to be applied.
        self.mapping_config = mapping_config
        
        # Type of OFDM modulation, such as DCO or ACO-OFDM.
        self.ofdm_type = modulation_config["ofdm_type"]

        # Array with all symbols converted from the input bitstream.
        self.mapped_info = mapped_info

        # Value for the pilot in the OFDM symbol.
        self.pilot_value = modulation_config["pilot_value"]

        # Number of OFDM subcarriers per OFDM symbol.
        self.number_of_carriers = modulation_config["n_carriers"]

        # Number of pilot carriers per OFDM symbol.
        self.number_of_pilots = modulation_config["n_pilots"]

        # Length of the cyclic prefix  per OFDM symbol.
        self.number_of_cyclic_prefix = modulation_config["n_cp"]
        
        # List of all input info to be transmitted. Will be converted into ofdm_symbol_list.
        # It depends on the frame_size, bits_per_symbol and number_of_carriers
        self.bitstream_list = []
        
        # OFDM symbol list
        self.ofdm_symbol_list = []
    
        pass

    def applyModulation(self):
        """Wrapper for all functions to apply the OFDM modulation on the mapped info."""
        
        self.sync_obj.appendToSimulationPath("applyModulation @ OFDM")
        
        
        self.sync_obj.setPrevious("OFDM")
        
        # Before mapping, we need to setup the data for each OFDM symbol.
        self.setupBitstreamList()
        
        self.sync_obj.setPrevious("OFDM")
        
        # for each chunk of information to become an OFDM symbol, to the Mapping
        for bitstream_ofdm_frame in self.bitstream_list:
        
            # Starts by creating the mapping object.
            self.mapping_obj = Mapping(
                bitstream_frame = bitstream_ofdm_frame,
                mapping_config = self.mapping_config,
                mapped_info = self.mapped_info,
                sync_obj = self.sync_obj
            )
            
            self.sync_obj.setPrevious("OFDM")
            
            # Set number of data carriers, before applying the mapping
            self.mapping_obj.setNumberOfDataCarriers(self.number_of_data_carriers)
            
            self.sync_obj.setPrevious("OFDM")
            
            # Apply the mapping for such information frame (bitstream_ofdm_frame)
            self.mapping_obj.applyMapping()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Get the mapped info
            self.mapped_info = self.mapping_obj.getMappedInfo()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Create the OFDM symbol data adding pilots and mapped data
            self.generateOFDMSymbol()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Do the IDFT on the OFDM symbol data
            self.applyIFFT()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Add the cyclic prefix in the OFDM symbol
            self.applyCp()
            
            self.sync_obj.setPrevious("OFDM")
            
            self.ofdm_symbol_list.append(self.ofdm_symbol_tx)
            
    

    def setupOFDMCarriersIndexes(self):
        """Setup carriers indexes for ofdm calculation."""
        
        self.sync_obj.appendToSimulationPath("setupOFDMCarriersIndexes @ OFDM")
        
        # Indexes for all carriers (data carriers + pilot carriers)
        self.all_subcarriers = np.arange(self.number_of_carriers)
        
        # set indexes for pilot subcarriers
        self.pilot_subcarriers = self.all_subcarriers[::self.number_of_carriers//self.number_of_pilots]
        
        # make last subcarrier also as a pilot (and increment number of pilots)
        self.pilot_subcarriers = np.hstack([self.pilot_subcarriers, np.array([self.all_subcarriers[-1]])])
        self.number_of_pilots += 1
        
        # set the indexes for the data subcarriers
        self.data_subcarriers = np.delete(self.all_subcarriers, self.pilot_subcarriers)
        
        # set number of actual data carriers (through FFT)
        self.number_of_data_carriers = len(self.data_subcarriers)
        
        
    def setupBitstreamList(self):
        """Generate list of data to be converted into OFDM symbols."""
        
        self.sync_obj.appendToSimulationPath("setupBitstreamList @ OFDM")
        
        # Converts bitstream to numpy array
        self.bitstream_frame = np.array([bit for bit in self.bitstream_frame], dtype=int)
        
        # get frame_size and bits_per_symbol
        frame_size = len(self.bitstream_frame)
        bits_per_symbol = self.mapping_config[1]
        
        # number of symbols per OFDM symbol
        number_of_symbols_per_ofdm_symbol = frame_size//bits_per_symbol
        
        # number of OFDM symbols for transmission
        n_ofdm_symbols = number_of_symbols_per_ofdm_symbol//self.number_of_data_carriers
        
        # number of bits for each ofdm symbol
        self.bits_per_ofdm_symbol = bits_per_symbol*self.number_of_data_carriers
        
        # Pad whole info frame with zeros if necessary
        if frame_size > n_ofdm_symbols*self.bits_per_ofdm_symbol:
            # number of zeros to pad
            zeros_to_pad = (n_ofdm_symbols + 1)*self.bits_per_ofdm_symbol - frame_size
            self.bitstream_frame = np.array([0]*zeros_to_pad + list(self.bitstream_frame), dtype=int)
            
        temp_bitstream = []
        self.bitstream_list = []
        counter = 0
        # recalculate frame size after padding
        frame_size = len(self.bitstream_frame)
        for index in range(0, frame_size):
            # while counter < number of bits per OFDM symbol
            if index == frame_size - 1:
                temp_bitstream.append(self.bitstream_frame[index])
                self.bitstream_list.append(np.array(temp_bitstream))
            elif counter < self.bits_per_ofdm_symbol:
                temp_bitstream.append(self.bitstream_frame[index])
                counter += 1
            else:
                self.bitstream_list.append(np.array(temp_bitstream))
                temp_bitstream = []
                temp_bitstream.append(self.bitstream_frame[index])
                counter = 1
        
    def generateOFDMSymbol(self):
        """Generate OFDM symbols, adding pilots and data carriers."""
        
        self.sync_obj.appendToSimulationPath("generateOFDMSymbol @ OFDM")
        
        # Initialize the the ofdm data as zeros
        self.ofdm_symbol_data = np.zeros(self.number_of_carriers, dtype=complex)
        
        # Introduce the pilots in the subcarrier ofdm symbol
        self.ofdm_symbol_data[self.pilot_subcarriers] = self.pilot_value
        
        # Introduce the actual mapped data in the ofdm symbol
        self.ofdm_symbol_data[self.data_subcarriers] = self.mapped_info
        
        
    def applyIFFT(self):
        """Applies the IDFT on the OFDM symbols."""
        
        self.sync_obj.appendToSimulationPath("applyIFFT @ OFDM")
        
        self.digital_ofdm = np.fft.ifft(self.ofdm_symbol_data)
    
    def applyCp(self):
        """Add the cyclic prefix to the OFDM symbol, and creates the 'ofdm_symbol_tx'"""
        
        self.sync_obj.appendToSimulationPath("applyCp @ OFDM")
        
        # Get end of cyclic prefix
        self.ofdm_symbol_tx = self.digital_ofdm[-self.number_of_cyclic_prefix:]
        
        # And pass to the beginning of te vector
        self.ofdm_symbol_tx = np.hstack([self.ofdm_symbol_tx, self.digital_ofdm])
        
        
    def applyDeModulation(self):
        """Wrapper for all functions to apply the OFDM de-modulation on the rx_data."""
        
        self.sync_obj.appendToSimulationPath("applyDeModulation @ OFDM")
        
        self.sync_obj.setPrevious("OFDM")
        
        # # Before mapping, we need to setup the data for each OFDM symbol.
        # self.setupBitstreamList()
        
        # self.sync_obj.setPrevious("OFDM")
        
        # for each chunk of information to become an OFDM symbol, to the Mapping
        for rx_ofdm_symbol in self.ofdm_rx_data_list:
            
            # Set the current RX OFDM symbol
            self.setOFDMSymbolRx(rx_ofdm_symbol)
            
            self.sync_obj.setPrevious("OFDM")
            
            # Remove the cyclic prefix in the OFDM symbol
            self.removeCp()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Applies the FFT
            self.applyFFT()
            
            self.sync_obj.setPrevious("OFDM")
            
            self.estimateChannel() #### STOPPED HERE
            STOPPED HERE
            
            self.sync_obj.setPrevious("OFDM")
        
            # # Starts by creating the mapping object.
            # self.mapping_obj = Mapping(
            #     bitstream_frame = rx_ofdm_list,
            #     mapping_config = self.mapping_config,
            #     mapped_info = self.mapped_info,
            #     sync_obj = self.sync_obj
            # )
            
            self.sync_obj.setPrevious("OFDM")
            
            # Set number of data carriers, before applying the mapping
            self.mapping_obj.setNumberOfDataCarriers(self.number_of_data_carriers)
        
    def removeCp(self):
        """Removes the cyclic prefix from 'ofdm_symbol_rx'."""
        
        self.sync_obj.appendToSimulationPath("removeCp @ OFDM")
        
        self.ofdm_symbol_rx = self.ofdm_symbol_rx[self.number_of_cyclic_prefix:(self.number_of_cyclic_prefix + self.number_of_carriers)]
        
    def applyFFT(self):
        """Applies the DFT on the OFDM symbols."""
        
        self.sync_obj.appendToSimulationPath("applyIFFT @ OFDM")
        
        self.ofdm_symbol_rx = np.fft.fft(self.ofdm_symbol_rx)
    
    def estimateChannel(self):
        """Analyze pilots to get the channel estimation."""
        
        self.sync_obj.appendToSimulationPath("estimateChannel @ OFDM")
    

    def equalize(self):
        """Equalize, given OFDM symbols from DFT operation, and the channel estimate."""
        
        self.sync_obj.appendToSimulationPath("equalize @ OFDM")
    

    def getConstellation(self):
        """Given equalized data, return the 'mapped_output'."""
        
        self.sync_obj.appendToSimulationPath("getConstellation @ OFDM")
    

    def getOfdmType(self):
        """Returns value of self.ofdm_type"""
        
        return self.ofdm_type

    def setOfdmType(self, ofdm_type):
        """Set new value for self.ofdm_type"""
        
        self.ofdm_type = ofdm_type

    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        return self.mapped_info

    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.mapped_info = mapped_info

    def getPilotValue(self):
        """Returns value of self.pilot_value"""
        
        return self.pilot_value

    def setPilotValue(self, pilot_value):
        """Set new value for self.pilot_value"""
        
        self.pilot_value = pilot_value

    def getNumberOfCarriers(self):
        """Returns value of self.number_of_carriers"""
        
        return self.number_of_carriers

    def setNumberOfCarriers(self, number_of_carriers):
        """Set new value for self.number_of_carriers"""
        
        self.number_of_carriers = number_of_carriers

    def getNumberOfPilots(self):
        """Returns value of self.number_of_pilots"""
        
        return self.number_of_pilots

    def setNumberOfPilots(self, number_of_pilots):
        """Set new value for self.number_of_pilots"""
        
        self.number_of_pilots = number_of_pilots

    def getNumberOfCyclicPrefix(self):
        """Returns value of self.number_of_cyclic_prefix"""
        
        return self.number_of_cyclic_prefix

    def setNumberOfCyclicPrefix(self, number_of_cyclic_prefix):
        """Set new value for self.number_of_cyclic_prefix"""
        
        self.number_of_cyclic_prefix = number_of_cyclic_prefix
    
    def getBitstreamFrame(self):
        """Returns value of self.bitstream_frame"""
        
        return self.bitstream_frame

    def setBitstreamFrame(self, bitstream_frame):
        """Set new value for self.bitstream_frame"""
        
        self.bitstream_frame = bitstream_frame
    
    def getBitstreamList(self):
        """Returns value of self.bitstream_list"""
        
        return self.bitstream_list

    def setBitstreamList(self, bitstream_list):
        """Set new value for self.bitstream_list"""
        
        self.bitstream_list = bitstream_list
        
    def getOFDMSymbolList(self):
        """Returns value of self.ofdm_symbol_list"""
        
        self.sync_obj.appendToSimulationPath("getOFDMSymbolList @ OFDM")
        
        return self.ofdm_symbol_list

    def setOFDMSymbolList(self, ofdm_symbol_list):
        """Set new value for self.ofdm_symbol_list"""
        
        self.sync_obj.appendToSimulationPath("setOFDMSymbolList @ OFDM")
        
        self.ofdm_symbol_list = ofdm_symbol_list
    
    
    def getOFDMRxDataList(self):
        """Returns value of self.ofdm_rx_data_list"""
        
        self.sync_obj.appendToSimulationPath("getOFDMRxDataList @ OFDM")
        
        return self.ofdm_rx_data_list

    def setOFDMRxDataList(self, ofdm_rx_data_list):
        """Set new value for self.ofdm_rx_data_list"""
        
        self.sync_obj.appendToSimulationPath("setOFDMRxDataList @ OFDM")
        
        self.ofdm_rx_data_list = ofdm_rx_data_list
    
    def getOFDMSymbolRx(self):
        """Returns value of self.ofdm_symbol_rx"""
        
        self.sync_obj.appendToSimulationPath("getOFDMSymbolRx @ OFDM")
        
        return self.ofdm_symbol_rx

    def setOFDMSymbolRx(self, ofdm_symbol_rx):
        """Set new value for self.ofdm_symbol_rx"""
        
        self.sync_obj.appendToSimulationPath("setOFDMSymbolRx @ OFDM")
        
        self.ofdm_symbol_rx = ofdm_symbol_rx
