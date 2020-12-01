from generalLibrary import timer_dec, sync_track

import numpy as np

from scipy import interpolate

from matplotlib import pyplot as plt

from Mapping import Mapping

import Global

import generalLibrary as lib

import pyfftw

import reikna


class OFDM(object):
    
    def __init__(self, bitstream_frame, modulation_config, mapping_config, mapped_info, sync_obj):
        """Constructor of OFDM."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("OFDM") or self.sync_obj.getDebug("all")
        
        self.PLOT = self.sync_obj.getPlot("OFDM") or self.sync_obj.getPlot("all")
        
        self.sync_obj.appendToSimulationPath("OFDM")
        
        if self.DEBUG:
            print('Running OFDM...')
            
        # Flag to use pyfft (wrapper for FFTW, that is faster), istead of numpy fft
        self.use_pyfft = Global.use_pyfft
        
        # Bitstream info for transmission, depending on number of frames.
        self.bitstream_frame = bitstream_frame
        
        # flag to remove padded zeros before analysis
        self.remove_padded_zeros = Global.remove_padded_zeros
        
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
    
    @sync_track
    @timer_dec
    def applyModulation(self):
        """Wrapper for all functions to apply the OFDM modulation on the mapped info."""
        
        
        
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
            
    
    @sync_track
    def setupOFDMCarriersIndexes(self):
        """Setup carriers indexes for ofdm calculation."""
        
        
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
        
    @sync_track
    def setupBitstreamList(self):
        """Generate list of data to be converted into OFDM symbols."""
        
        
        # Converts bitstream to numpy array
        self.bitstream_frame = np.array([bit for bit in self.bitstream_frame], dtype=int)
        
        # get frame_size and bits_per_symbol
        frame_size = len(self.bitstream_frame)
        bits_per_symbol = int(np.log2(self.mapping_config[1]))
        
        # number of symbols per OFDM symbol
        number_of_symbols_per_ofdm_symbol = frame_size//bits_per_symbol
        
        # number of OFDM symbols for transmission
        n_ofdm_symbols = number_of_symbols_per_ofdm_symbol//self.number_of_data_carriers
        
        # number of bits for each ofdm symbol
        self.bits_per_ofdm_symbol = bits_per_symbol*self.number_of_data_carriers
        
        # Pad whole info frame with zeros if necessary
        if frame_size > n_ofdm_symbols*self.bits_per_ofdm_symbol:
            # number of zeros to pad
            self.zeros_to_pad = (n_ofdm_symbols + 1)*self.bits_per_ofdm_symbol - frame_size
            self.bitstream_frame = np.array([0]*self.zeros_to_pad + list(self.bitstream_frame), dtype=int)
            
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
    
    @sync_track
    def generateOFDMSymbol(self):
        """Generate OFDM symbols, adding pilots and data carriers."""
        
        
        # Initialize the the ofdm data as zeros
        self.ofdm_symbol_data = np.zeros(self.number_of_carriers, dtype=complex)
        
        # Introduce the pilots in the subcarrier ofdm symbol
        self.ofdm_symbol_data[self.pilot_subcarriers] = self.pilot_value
        
        # Introduce the actual mapped data in the ofdm symbol
        self.ofdm_symbol_data[self.data_subcarriers] = self.mapped_info
        
    @sync_track
    def applyIFFT(self):
        """Applies the IDFT on the OFDM symbols."""
        
        
        if self.use_pyfft:
            self.digital_ofdm = pyfftw.interfaces.numpy_fft.ifft(self.ofdm_symbol_data)
        else:
            self.digital_ofdm = np.fft.ifft(self.ofdm_symbol_data)
    
    @sync_track
    def applyCp(self):
        """Add the cyclic prefix to the OFDM symbol, and creates the 'ofdm_symbol_tx'"""
        
        
        # Get end of cyclic prefix
        self.ofdm_symbol_tx = self.digital_ofdm[-self.number_of_cyclic_prefix:]
        
        # And pass to the beginning of te vector
        self.ofdm_symbol_tx = np.hstack([self.ofdm_symbol_tx, self.digital_ofdm])
        
    
    @sync_track
    @timer_dec
    def applyDeModulation(self):
        """Wrapper for all functions to apply the OFDM de-modulation on the rx_data."""
        
        
        self.sync_obj.setPrevious("OFDM")
        
        # when de-mapping, the ouput starts as an empty list (temp_list)
        temp_list = []
        
        # for each chunk of information to become an OFDM symbol, to the Mapping
        for idx_data, rx_ofdm_symbol in enumerate(self.ofdm_rx_data_list):
            
            # Set the current RX OFDM symbol
            self.setOFDMSymbolRx(rx_ofdm_symbol)
            
            self.sync_obj.setPrevious("OFDM")
            
            # Remove the cyclic prefix in the OFDM symbol
            self.removeCp()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Applies the FFT
            self.applyFFT()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Estimates the channel response
            self.estimateChannel()
            
            self.sync_obj.setPrevious("OFDM")
            
            if self.PLOT:
                
                ### TODO - Get contribution of multiple CIRs... not sure how to do that yet
                
                # For each CIR in the CIR list (one CIR for each lamp, if appliable)
                for idx_cir, CIR in enumerate(self.list_of_channel_response):
                    
                    # show = idx_cir == len(self.list_of_channel_response) - 1
                    show = True
                    self.compareOFDMChannelResponse(
                        CIR,
                        show = show
                    )
            
            self.sync_obj.setPrevious("OFDM")
            
            # Applies equalization, given the channel response
            self.applyEqualization()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Get the mapped ouput signal, with its associated constellation
            self.getConstellation()
            
            self.sync_obj.setPrevious("OFDM")
            
            # Creates the de-mapping object.
            self.de_mapping_obj = Mapping(
                bitstream_frame = None,
                mapping_config = self.mapping_config,
                mapped_info = self.mapped_output,
                sync_obj = self.sync_obj
            )
            
            self.sync_obj.setPrevious("OFDM")
            
            # Set demapping from mapped_output
            self.de_mapping_obj.applyDemapping()
            
            self.sync_obj.setPrevious("OFDM")
            
            if self.PLOT:
                # Given de-mapping, plot found constelattions from mapped_output
                # show = idx_data == len(self.ofdm_rx_data_list) - 1
                show = True
                self.showFoundConstellation(
                    self.de_mapping_obj.getFoundConstellation(),
                    show = show
                )
            
            self.sync_obj.setPrevious("OFDM")
            
            # Get seriallized data of interest
            temp_list.append(self.de_mapping_obj.getRxBitstreamFrame())
            
            self.sync_obj.setPrevious("OFDM")
            
        self.bitstream_frame = []
        
        for bitstream in temp_list:
            self.bitstream_frame = self.bitstream_frame + list(bitstream)
        
        zero_pad_counter = 0
        temp_frame = ''
        for bit in list(self.bitstream_frame):
            # print(bit)
            if self.remove_padded_zeros:
                if zero_pad_counter >= self.zeros_to_pad:
                    temp_frame += str(bit)
            else:
                temp_frame += str(bit)
            zero_pad_counter += 1
        self.bitstream_frame = temp_frame
        del temp_list
        del temp_frame
        
        # # converts to numpy array
        # self.bitstream_frame = np.array(self.bitstream_frame)
    
    @sync_track
    def removeCp(self):
        """Removes the cyclic prefix from 'ofdm_symbol_rx'."""
        
        
        self.ofdm_symbol_rx = self.ofdm_symbol_rx[self.number_of_cyclic_prefix:(self.number_of_cyclic_prefix + self.number_of_carriers)]
        
    @sync_track
    def applyFFT(self):
        """Applies the DFT on the OFDM symbols."""
        
        
        if self.use_pyfft:
            self.ofdm_symbol_rx = pyfftw.interfaces.numpy_fft.fft(self.ofdm_symbol_rx)
        else:
            self.ofdm_symbol_rx = np.fft.fft(self.ofdm_symbol_rx)
            
    @sync_track
    def estimateChannel(self):
        """Analyze pilots to get the channel estimation."""
        
        
        # Get the channel response by dividing the pilot subcarriers by the known pilot value.
        self.estimated_pilots_response = self.ofdm_symbol_rx[self.pilot_subcarriers] / self.pilot_value
        
        # interpolates the estimated response, to get the actual modulus and angle for estimated channel response
        channel_response_modulus = interpolate.interp1d(self.pilot_subcarriers, abs(self.estimated_pilots_response), kind='linear')(self.all_subcarriers)
        channel_response_angle = interpolate.interp1d(self.pilot_subcarriers, np.angle(self.estimated_pilots_response), kind='linear')(self.all_subcarriers)
        
        # join modulus and phase to create the estimated channel response
        self.estimated_channel_response = channel_response_modulus * np.exp(1j*channel_response_angle)
        
    @sync_track
    def applyEqualization(self):
        """Equalize, given OFDM symbols from DFT operation, and the channel estimate."""
        
        
        self.ofdm_symbol_rx = self.ofdm_symbol_rx / self.estimated_channel_response

    @sync_track
    def getConstellation(self):
        """Given equalized data, return the 'mapped_output'."""
        
        
        self.mapped_output = self.ofdm_symbol_rx[self.data_subcarriers]
    
    @sync_track
    def compareOFDMChannelResponse(self, current_channel, show = False):
        """Compares the OFDM channel response with estimated. Must first set all channel responses."""
        
        
        # Calculates the actual CIR
        CIR = np.fft.fft(current_channel, self.number_of_carriers)
        
        plt.plot(self.all_subcarriers, abs(CIR), label='Actual channel response')
        plt.stem(self.pilot_subcarriers, abs(self.estimated_pilots_response), label='Estimated pilots')
        plt.plot(self.all_subcarriers, abs(self.estimated_channel_response), label='Interpolated estimated channel')
        plt.grid(True)
        plt.title('Channel response estimations')
        plt.xlabel('Subcarrier indexes')
        plt.ylabel('$|H(f)|$')
        plt.legend(fontsize=10)
        plt.ylim(0, 1.5)
        plt.show(show)
        
        
    @sync_track
    def showFoundConstellation(self, found_constellation, show = False):
        """Plots the found constellation."""
        
        
        # plot all the estimated constellations
        for qam, estimated in zip(self.mapped_output, found_constellation):
            plt.plot([qam.real, estimated.real], [qam.imag, estimated.imag], 'b-o')
            plt.plot(found_constellation.real, found_constellation.imag, 'ro')
        
        
        plt.grid(True)
        plt.title('Estimated constellation')
        plt.xlabel('Real')
        plt.ylabel('Imagingary')
        plt.legend(fontsize=10)
        plt.show(show)
        

    @sync_track    
    def getOfdmType(self):
        """Returns value of self.ofdm_type"""
        
        return self.ofdm_type

    @sync_track
    def setOfdmType(self, ofdm_type):
        """Set new value for self.ofdm_type"""
        
        self.ofdm_type = ofdm_type

    @sync_track
    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        return self.mapped_info

    @sync_track
    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.mapped_info = mapped_info

    @sync_track
    def getPilotValue(self):
        """Returns value of self.pilot_value"""
        
        return self.pilot_value

    @sync_track
    def setPilotValue(self, pilot_value):
        """Set new value for self.pilot_value"""
        
        self.pilot_value = pilot_value
    
    @sync_track
    def getNumberOfCarriers(self):
        """Returns value of self.number_of_carriers"""
        
        
        return self.number_of_carriers
    
    @sync_track
    def setNumberOfCarriers(self, number_of_carriers):
        """Set new value for self.number_of_carriers"""
        
        
        self.number_of_carriers = number_of_carriers
    
    @sync_track
    def getNumberOfPilots(self):
        """Returns value of self.number_of_pilots"""
        
        return self.number_of_pilots
    
    @sync_track
    def setNumberOfPilots(self, number_of_pilots):
        """Set new value for self.number_of_pilots"""
        
        self.number_of_pilots = number_of_pilots
    
    @sync_track
    def getNumberOfCyclicPrefix(self):
        """Returns value of self.number_of_cyclic_prefix"""
        
        return self.number_of_cyclic_prefix
    
    @sync_track
    def setNumberOfCyclicPrefix(self, number_of_cyclic_prefix):
        """Set new value for self.number_of_cyclic_prefix"""
        
        self.number_of_cyclic_prefix = number_of_cyclic_prefix
    
    @sync_track
    def getBitstreamFrame(self):
        """Returns value of self.bitstream_frame"""
        
        
        return self.bitstream_frame
    
    @sync_track
    def setBitstreamFrame(self, bitstream_frame):
        """Set new value for self.bitstream_frame"""
        
        
        self.bitstream_frame = bitstream_frame
    
    @sync_track
    def getBitstreamList(self):
        """Returns value of self.bitstream_list"""
        
        return self.bitstream_list
    
    @sync_track
    def setBitstreamList(self, bitstream_list):
        """Set new value for self.bitstream_list"""
        
        self.bitstream_list = bitstream_list
        
    @sync_track
    def getOFDMSymbolList(self):
        """Returns value of self.ofdm_symbol_list"""
        
        
        return self.ofdm_symbol_list
    
    @sync_track
    def setOFDMSymbolList(self, ofdm_symbol_list):
        """Set new value for self.ofdm_symbol_list"""
        
        
        self.ofdm_symbol_list = ofdm_symbol_list
    
    
    @sync_track
    def getOFDMRxDataList(self):
        """Returns value of self.ofdm_rx_data_list"""
        
        
        return self.ofdm_rx_data_list
    
    @sync_track
    def setOFDMRxDataList(self, ofdm_rx_data_list):
        """Set new value for self.ofdm_rx_data_list"""
        
        
        self.ofdm_rx_data_list = ofdm_rx_data_list
    
    @sync_track
    def getOFDMSymbolRx(self):
        """Returns value of self.ofdm_symbol_rx"""
        
        
        return self.ofdm_symbol_rx
    
    @sync_track
    def setOFDMSymbolRx(self, ofdm_symbol_rx):
        """Set new value for self.ofdm_symbol_rx"""
        
        
        self.ofdm_symbol_rx = ofdm_symbol_rx
    
    @sync_track
    def getSubCarriers(self):
        """Returns value of self.all_subcarriers"""
        
        
        return self.all_subcarriers
    
    @sync_track
    def setSubCarriers(self, all_subcarriers):
        """Set new value for self.all_subcarriers"""
        
        
        self.all_subcarriers = all_subcarriers
    
    @sync_track
    def getPilotCarriers(self):
        """Returns value of self.pilot_subcarriers"""
        
        
        return self.pilot_subcarriers
    
    @sync_track
    def setPilotCarriers(self, pilot_subcarriers):
        """Set new value for self.pilot_subcarriers"""
        
        
        self.pilot_subcarriers = pilot_subcarriers
    
    @sync_track
    def getEstimatedChannel(self):
        """Returns value of self.estimated_channel_response"""
        
        
        return self.estimated_channel_response
    
    @sync_track
    def setEstimatedChannel(self, estimated_channel_response):
        """Set new value for self.estimated_channel_response"""
        
        
        self.estimated_channel_response = estimated_channel_response
    
    @sync_track
    def getListOfChannelResponses(self):
        """Returns value of self.list_of_channel_response"""
        
        
        return self.list_of_channel_response
    
    @sync_track
    def setListOfChannelResponses(self, list_of_channel_response):
        """Set new value for self.list_of_channel_response"""
        
        
        self.list_of_channel_response = list_of_channel_response
        
    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj