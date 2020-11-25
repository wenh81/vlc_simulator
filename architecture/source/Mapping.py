import numpy as np

class Mapping(object):
    def __init__(self, bitstream_frame, mapping_config, mapped_info, sync_obj):
        """Constructor of Mapping, that parallelizes and maps the input stream."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug()
        
        self.sync_obj.appendToSimulationPath("Mapping")
        
        if self.DEBUG:
            print('Running Mapping...')

        
        # Mapping config to be applied.
        self.mapping_config = mapping_config
        
        # Bitstream info for transmission, depending on number of frames.
        self.bitstream_frame = bitstream_frame

        # Number of bits per symbol, before mapping.
        self.bits_per_symbol = mapping_config[1]

        # Size of current frame to be transmitted.
        self.frame_size = len(bitstream_frame)

        # Type of mapping to be applied in parallelized data.
        self.mapping_type = mapping_config[0]

        # Array with all parallelized symbols from the input bitstream.
        self.parallelized_info = np.zeros([self.frame_size//self.bits_per_symbol, self.bits_per_symbol], dtype=np.uint8)
        # self.parallelized_info = np.zeros([self.frame_size//self.bits_per_symbol, self.bits_per_symbol], dtype=np.bool_)
        
        # Bitstream info after receiveing, depending on number of frames.
        self.rx_bitstream_frame = None
        
        # Array with all symbols converted from the input bitstream.
        self.mapped_info = mapped_info
        
        # Has the shape of the input mapped info.
        self.mapped_shape = None
        
        # Stores the number of data carriers, i.e., the number of quadrature symbols for each transmission
        self.number_of_data_carriers = None
    
        pass

    def setupMappingTable(self):
        """Setup mapping table, depending on the choosen mapping scheme."""
        
        self.sync_obj.appendToSimulationPath("setupMappingTable @ Mapping")
        
        self.sync_obj.setPrevious("Mapping")
        
        if self.mapping_type == "QAM":
            if self.bits_per_symbol == 4:
        
                self.mapping_table = {
                    (0,0,0,0) : -3-3j,
                    (0,0,0,1) : -3-1j,
                    (0,0,1,0) : -3+3j,
                    (0,0,1,1) : -3+1j,
                    (0,1,0,0) : -1-3j,
                    (0,1,0,1) : -1-1j,
                    (0,1,1,0) : -1+3j,
                    (0,1,1,1) : -1+1j,
                    (1,0,0,0) :  3-3j,
                    (1,0,0,1) :  3-1j,
                    (1,0,1,0) :  3+3j,
                    (1,0,1,1) :  3+1j,
                    (1,1,0,0) :  1-3j,
                    (1,1,0,1) :  1-1j,
                    (1,1,1,0) :  1+3j,
                    (1,1,1,1) :  1+1j
                }
            else:
                raise ValueError(f"\n\n***Error --> {self.bits_per_symbol}-QAM not supported yet.\n")
        
    def serialToParallel(self):
        """Converts each 'bitstream_frame' into 2D numpy array, as [bits_per_symbol, len(bitstream_info)/bits_per_symbol]"""
        
        self.sync_obj.appendToSimulationPath("serialToParallel @ Mapping")
        
        self.sync_obj.setPrevious("Mapping")
        
        if self.number_of_data_carriers is not None:
            self.parallelized_info = self.bitstream_frame.reshape((self.number_of_data_carriers, self.bits_per_symbol))
        else:
            raise ValueError(f"\n\n***Error --> Please first setup the number of data carriers 'number_of_data_carriers'.\nUse setNumberOfDataCarriers(value)\n")
        
        pass
    

    def applyMapping(self):
        """Given 'bits_per_symbol' and 'mapping_type', generates the 'mapped_info'."""
        
        self.sync_obj.appendToSimulationPath("applyMapping @ Mapping")
        
        self.sync_obj.setPrevious("Mapping")
        
        if self.mapping_type == "QAM":
            
            self.setupMappingTable()
            
            self.sync_obj.setPrevious("Mapping")
            
            self.serialToParallel()
            
            self.sync_obj.setPrevious("Mapping")
            
            # calculate the mapped info, depending on the modulations scheme
            self.mapped_info = np.array([self.mapping_table[tuple(symbol)] for symbol in self.parallelized_info])
                
        else:
            raise ValueError(f"\n\n***Error --> Not supported mapping_type: <{self.mapping_type}>!\n")
    

    def applyDemapping(self):
        """Given 'mapped_output', returns the closest values for the demapping."""
        pass
    

    def ParallelToserial(self):
        """Converts each 'bitstream_frame' into a serial stream of data 'rx_bitstream_frame'."""
        pass
    

    def getBitstreamFrame(self):
        """Returns value of self.bitstream_frame"""
        
        return self.bitstream_frame

    def setBitstreamFrame(self, bitstream_frame):
        """Set new value for self.bitstream_frame"""
        
        self.bitstream_frame = bitstream_frame

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

    def getMappedInfo(self):
        """Returns value of self.mapped_info"""
        
        self.sync_obj.appendToSimulationPath("getMappedInfo @ Mapping")
        
        return self.mapped_info

    def setMappedInfo(self, mapped_info):
        """Set new value for self.mapped_info"""
        
        self.sync_obj.appendToSimulationPath("setMappedInfo @ Mapping")
        
        self.mapped_info = mapped_info

    def getMappingType(self):
        """Returns value of self.mapping_type"""
        
        return self.mapping_type

    def setMappingType(self, mapping_type):
        """Set new value for self.mapping_type"""
        
        self.mapping_type = mapping_type

    def getRxBitstreamFrame(self):
        """Returns value of self.rx_bitstream_frame"""
        
        return self.rx_bitstream_frame

    def setRxBitstreamFrame(self, rx_bitstream_frame):
        """Set new value for self.rx_bitstream_frame"""
        
        self.rx_bitstream_frame = rx_bitstream_frame
    
    def getNumberOfDataCarriers(self):
        """Returns value of self.number_of_data_carriers"""
        
        return self.number_of_data_carriers

    def setNumberOfDataCarriers(self, number_of_data_carriers):
        """Set new value for self.number_of_data_carriers"""
        
        self.sync_obj.appendToSimulationPath("setNumberOfDataCarriers @ Mapping")
        
        self.sync_obj.setPrevious("Mapping")
        
        self.number_of_data_carriers = number_of_data_carriers
