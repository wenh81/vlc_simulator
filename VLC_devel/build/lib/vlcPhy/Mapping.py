from .common_imports import *


class Mapping(object):
    
    def __init__(self, bitstream_frame, mapping_config, sync_obj):
        """Constructor of Mapping, that parallelizes and maps the input stream."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Mapping") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Mapping")
        
        if self.DEBUG:
            print('Running Mapping...')

        
        # Mapping config to be applied.
        self.mapping_config = mapping_config

        # Bitstream info for transmission, depending on number of frames.
        self.bitstream_frame = bitstream_frame

        # Number of bits per symbol, before mapping.
        self.bits_per_symbol = int(np.log2(mapping_config[1]))

        # Size of current frame to be transmitted.
        if self.bitstream_frame is not None:
            self.frame_size = len(bitstream_frame)

            # Array with all parallelized symbols from the input bitstream.
            self.parallelized_info = np.zeros([self.frame_size//self.bits_per_symbol, self.bits_per_symbol], dtype=np.uint8)
            
        else:
            
            self.frame_size = None
            
            self.parallelized_info = None
            
            
        # Type of mapping to be applied in parallelized data.
        self.mapping_type = mapping_config[0]

        # self.parallelized_info = np.zeros([self.frame_size//self.bits_per_symbol, self.bits_per_symbol], dtype=np.bool_)
        
        # Bitstream info after receiveing, depending on number of frames.
        self.rx_bitstream_frame = None
        
        # Array with all symbols converted from the input bitstream, when mapping
        # Or the output mapped, when demapping
        self.mapped_info = None
        
        # Has the shape of the input mapped info.
        self.mapped_shape = None
        
        # Stores the number of data carriers, i.e., the number of quadrature symbols for each transmission
        self.number_of_data_carriers = None
    
        pass

    @sync_track
    def setupMappingTable(self):
        """Setup mapping table, depending on the choosen mapping scheme."""
        
        # Get number of levels for mapping
        M = self.mapping_config[1]
        
        if self.mapping_type == "QAM":
            
            # QAM object
            self.m_qam_obj = QAMModem(M)
            
            # List of binary representations for M-QAM
            list_of_binary = [','.join(str(np.binary_repr(number, width = int(np.log2(M))))) for number in range(0, M)]
            
            # Creates the mapping table
            self.mapping_table = {eval(f"({binary})") : self.m_qam_obj.modulate(eval(binary))[0] for binary in list_of_binary}
        
        elif self.mapping_type == "PSK":
            
            # BPSK = 2-PSK
            if M == 2:
                self.mapping_table = {
                        (1,) : +1+0j,
                        (0,) : -1+0j
                    }
            else:
                
                # PSK object
                self.m_psk_obj = PSKModem(M)
                
                # List of binary representations for M-PSK
                list_of_binary = [','.join(str(np.binary_repr(number, width = int(np.log2(M))))) for number in range(0, M)]
                
                # Creates the mapping table
                self.mapping_table = {eval(f"({binary})") : self.m_psk_obj.modulate(eval(binary))[0] for binary in list_of_binary}
        
        # Also, setup the demapping table
        self.demapping_table = {v : k for k, v in self.mapping_table.items()}
        
    @sync_track
    def serialToParallel(self):
        """Converts each 'bitstream_frame' into 2D numpy array, as [bits_per_symbol, len(bitstream_info)/bits_per_symbol]"""
        
        
        if self.number_of_data_carriers is not None:
            self.parallelized_info = self.bitstream_frame.reshape((self.number_of_data_carriers, self.bits_per_symbol))
        else:
            raise ValueError(f"\n\n***Error --> Please first setup the number of data carriers 'number_of_data_carriers'.\nUse setNumberOfDataCarriers(value)\n")
        
        pass
    
    @sync_track
    def createPilotTable(self):
        """Create the mapping table for given pilot config."""
        
        # Supported modulation
        if self.mapping_type in ["QAM", "PSK"]:
            
            self.setupMappingTable()

            max_imag = None
            max_real = None
            for key in self.mapping_table.keys():
                if max_imag is None:
                    max_imag = self.mapping_table[key].imag
                elif max_imag < self.mapping_table[key].imag:
                    max_imag = self.mapping_table[key].imag
                
                if max_real is None:
                    max_real = self.mapping_table[key].real
                elif max_real < self.mapping_table[key].real:
                    max_real = self.mapping_table[key].real
            
            # get pilot value
            self.pilot_value = max_real + 1j*max_imag
            
            return self.pilot_value
        
        else:
            raise ValueError(f"\n\n***Error --> Not supported mapping_type: <{self.mapping_type}>!\n")

    @sync_track
    def applyMapping(self):
        """Given 'bits_per_symbol' and 'mapping_type', generates the 'mapped_info'."""
        
        # Supported modulation
        if self.mapping_type in ["QAM", "PSK"]:
            
            self.setupMappingTable()
            
            self.serialToParallel()
            
            # calculate the mapped info, depending on the modulations scheme
            self.mapped_info = np.array([self.mapping_table[tuple(symbol)] for symbol in self.parallelized_info])
            
        else:
            raise ValueError(f"\n\n***Error --> Not supported mapping_type: <{self.mapping_type}>!\n")
    
    @sync_track
    def applyDemapping(self, mapped_output):
        """Given 'mapped_output', returns the closest values for the demapping."""
        

        printDebug(self.mapping_type)
        if self.mapping_type != "QA":
            
            self.setupMappingTable()
            
            # Given the demapping table, get all possible constellation points
            self.constellation = np.array([x for x in self.demapping_table.keys()])

            # calculates what is the distance between each received data, and each constellation point
            euclidean_dist = abs(mapped_output.reshape((-1,1)) - self.constellation.reshape((1,-1)))
            
            # Get the minimum distance index
            min_distance = euclidean_dist.argmin(axis=1)
            
            # get back the real constellation point
            self.found_constellation = self.constellation[min_distance]
            
            # Do the de-mapping transofrmation, back to bit list values
            self.rx_bitstream_frame = np.vstack([self.demapping_table[C] for C in self.found_constellation])
            
            # printDebug(self.found_constellation)
            # printDebug(self.rx_bitstream_frame)
            # printDebug(mapped_output)
            
            self.ParallelToserial()
            # printDebug(self.rx_bitstream_frame)
            
        else:
            raise ValueError(f"\n\n***Error --> Not supported mapping_type: <{self.mapping_type}>!\n")
        

    @sync_track
    def ParallelToserial(self):
        """Converts each parllelized constellation into a serial stream of data 'rx_bitstream_frame'."""
        
        self.rx_bitstream_frame = self.rx_bitstream_frame.reshape((-1,))
        
    @sync_track
    def getPilotValue(self):
        """Returns value of self.pilot_value"""
        
        return self.pilot_value

    @sync_track
    def setPilotValue(self, pilot_value):
        """Set new value for self.pilot_value"""
        
        self.pilot_value = pilot_value
        
    @sync_track
    def getBitstreamFrame(self):
        """Returns value of self.bitstream_frame"""
        
        return self.bitstream_frame

    @sync_track
    def setBitstreamFrame(self, bitstream_frame):
        """Set new value for self.bitstream_frame"""
        
        self.bitstream_frame = bitstream_frame

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
    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        
        return self.mapped_info

    @sync_track
    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        
        self.mapped_info = mapped_info

    @sync_track
    def getMappingType(self):
        """Returns value of self.mapping_type"""
        
        return self.mapping_type

    @sync_track
    def setMappingType(self, mapping_type):
        """Set new value for self.mapping_type"""
        
        self.mapping_type = mapping_type

    @sync_track
    def getRxBitstreamFrame(self):
        """Returns value of self.rx_bitstream_frame"""
        
        return self.rx_bitstream_frame

    @sync_track
    def setRxBitstreamFrame(self, rx_bitstream_frame):
        """Set new value for self.rx_bitstream_frame"""
        
        self.rx_bitstream_frame = rx_bitstream_frame
    
    @sync_track
    def getConstellation(self):
        """Returns value of self.constellation"""
        
        return self.constellation
    
    @sync_track
    def setConstellation(self, constellation):
        """Set new value for self.constellation"""
        
        self.constellation = constellation
    
    @sync_track
    def getFoundConstellation(self):
        """Returns value of self.found_constellation"""
        
        return self.found_constellation

    @sync_track
    def setFoundConstellation(self, found_constellation):
        """Set new value for self.found_constellation"""
        
        self.found_constellation = found_constellation
    
    @sync_track
    def getNumberOfDataCarriers(self):
        """Returns value of self.number_of_data_carriers"""
        
        return self.number_of_data_carriers

    @sync_track
    def setNumberOfDataCarriers(self, number_of_data_carriers):
        """Set new value for self.number_of_data_carriers"""
        
        self.number_of_data_carriers = number_of_data_carriers

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj