from .common_imports import *


class OFDM(object):
    
    def __init__(self, bitstream_frame, modulation_config, mapping_config, mapping_pilot_config, ofdm_duration, sync_obj):
        """Constructor of OFDM."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        # Get debug and plot flags
        self.DEBUG, self.PLOT = lib.getDebugPlot("OFDM", self.sync_obj)
        
        self.sync_obj.appendToSimulationPath("OFDM")
        
        if self.DEBUG:
            print('Running OFDM...')
            
        # Flag to use pyfft (wrapper for FFTW, that is faster), istead of numpy fft
        self.use_pyfft = Global.use_pyfft
        
        # Bitstream info for transmission, depending on number of frames.
        self.bitstream_frame = bitstream_frame
        
        # flag to remove padded zeros before analysis
        self.remove_padded_zeros = Global.remove_padded_zeros
        
        # Mapping config to be applied on data.
        self.mapping_config = mapping_config

        # Mapping config to be applied on pilots.
        self.mapping_pilot_config = mapping_pilot_config
        
        # Type of OFDM modulation, such as DCO or ACO-OFDM.
        self.ofdm_type = modulation_config["ofdm_type"]

        # Array with all symbols converted from the input bitstream.
        self.mapped_info = None

        # Value for the pilot in the OFDM symbol.
        self.pilot_value = None

        # Number of OFDM subcarriers per OFDM symbol.
        self.number_of_carriers = modulation_config["n_fft"]

        # Set indexes for pilot subcarriers per OFDM symbol.
        self.pilot_subcarriers = modulation_config["pilots"]
        
        # Number of pilot carriers per OFDM symbol.
        self.number_of_pilots = len(self.pilot_subcarriers)

        # Length of the cyclic prefix per OFDM symbol.
        self.number_of_cyclic_prefix = modulation_config["n_cp"]
        
        # # Time duration of OFDM symbol (without cyclic prefix)
        # self.ofdm_symbol_time = modulation_config["ofdm_symbol_time"]

        # get actual OFDM time symbol duration (in secodns)
        # self.ofdm_duration = self.ofdm_symbol_time*(self.number_of_cyclic_prefix/self.number_of_carriers + 1)
        # self.ofdm_duration = Global.time_frame
        self.ofdm_duration = ofdm_duration

        # Total number of subcarriers including cyclic prefix
        self.total_subcarriers = (self.number_of_cyclic_prefix + self.number_of_carriers)

        # Set what will be the sample frequency. For OFDM this is the inverse of symbol duration by total number of subcarriers
        # b/c fundamental frequency of OFDM is 1 / (OFDM symbol duration), and largest frequency is max number of carriers * fundamental
        self.sample_frequency = (self.total_subcarriers) / self.ofdm_duration
        
        # Start the time vector list (each position for a position in data list)
        self.time_vector_list = None
        self.time_vector = None

        # Delay in steps for given rx wave
        self.phase_delay_steps = 0
        # Delay in time for given rx wave
        self.phase_delay_time = 0

        # Modulation config info
        self.modulation_config = modulation_config
        
        # List of all input info to be transmitted. Will be converted into ofdm_symbol_list.
        # It depends on the frame_size, bits_per_symbol and number_of_carriers
        self.bitstream_list = []
        
        # OFDM symbol list
        self.ofdm_symbol_list = []
        
        # List with all mapped info for each OFDM symbol of each sequence step
        self.all_mapped_info = []
        
    @sync_track
    # @timer_dec
    def applyModulation(self, decoded_sequence = None, seq_idx = None):
        """Wrapper for all functions to apply the OFDM modulation on the mapped info."""
        
        # Before mapping, we need to setup the data for each OFDM symbol.
        self.setupBitstreamList()
        
        # for each chunk of information to become an OFDM symbol, to the Mapping
        for bitstream_ofdm_frame in self.bitstream_list:
            
            #### Mapping object for data
            # Starts by creating the mapping object.
            self.mapping_obj = Mapping(
                bitstream_frame = bitstream_ofdm_frame,
                mapping_config = self.mapping_config,
                sync_obj = self.sync_obj
            )
            
            ## TODO -- PASS HERE THE DATA CARRIERS INDICES AND PILOTS... or NO NEED?
            # This is only the data, that should be converted into the mapping. Do the same for pilots?
            # pilots are known symbols introduced in '@ generateOFDMSymbol'
            
            # Set number of data carriers, before applying the mapping
            self.mapping_obj.setNumberOfDataCarriers(self.number_of_data_carriers)
            
            # Apply the mapping for such information frame (bitstream_ofdm_frame)
            self.mapping_obj.applyMapping()
            
            # Get the mapped info
            self.mapped_info = self.mapping_obj.getMappedInfo()
            
            #### Mapping object for pilots
            # Starts by creating the mapping object for pilots (to get the pilot value)
            self.mapping_pilot_obj = Mapping(
                bitstream_frame = None,
                mapping_config = self.mapping_pilot_config,
                sync_obj = self.sync_obj
            )
            
            # Create the mapping table for given pilot config, and return the pilot value
            self.pilot_value = self.mapping_pilot_obj.createPilotTable()
            
            # Create the OFDM symbol data adding pilots and mapped data
            self.generateOFDMSymbol()

            # Only for IM/DD
            if self.modulation_config['IM_DD']:
                # Apply hermitian simetry
                self.applyHermitianSymetry()
            
            # Do the IDFT on the OFDM symbol data
            self.applyIFFT()
            
            # Add the cyclic prefix in the OFDM symbol
            self.applyCp()
            
            
            # Only for IM/DD
            if self.modulation_config['IM_DD']:
                
                # Check if imaginary part is non-zero
                if np.abs(np.sum(self.ofdm_tx_data.imag)) > Global.zero_slack :
                    raise ValueError(f"\n\n***Error --> Hermitian symmetry generated a signal with non-zero imaginary part :\n{self.ofdm_tx_data}\n")
                
                # Convert to real, by removing imaginary part
                self.ofdm_tx_data = self.ofdm_tx_data.real

                # Clip signal to zero if ACO-OFDM
                OFDM_type = next(iter(self.ofdm_type.keys()))
                if OFDM_type == "ACO-OFDM":
                    self.ofdm_tx_data = lib.zeroClip(self.ofdm_tx_data)


            self.all_mapped_info.append(self.mapped_info)
            self.ofdm_symbol_list.append(self.ofdm_tx_data)

        # Add info that could be re-calculated at RX end, but we want to speed up things
        decoded_sequence['seq_pilot_value'].append(self.pilot_value)
        decoded_sequence['seq_all_mapped_info'].append(self.all_mapped_info)
        decoded_sequence['seq_zeros_to_pad'].append(self.zeros_to_pad)
        
    
    @sync_track
    def checkInputPilots(self, max_carriers = None, min_carriers = None, ignore_even = False):
        """Calculates and do check error if input pilots are inside allowed range."""
        
        # Calculates error check
        self.larger = None
        self.smaller = None
        self.even = None

        self.max_carriers = max_carriers - 1 ## -1 b/c any range goes from 0 to N-1
        self.min_carriers = min_carriers
        self.larger = np.array(self.pilot_subcarriers) > self.max_carriers
        self.smaller = np.array(self.pilot_subcarriers) < self.min_carriers
        if not ignore_even:
            self.even = np.array([True if num % 2 == 0 else False for num in np.array(self.pilot_subcarriers)])
        else:
            self.even = np.array([False for num in np.array(self.pilot_subcarriers)])

        # printDebug(self.larger)
        # printDebug(self.smaller)
        # printDebug(self.even, stop=False)
    
        # Do error check
        # if np.max(self.pilot_subcarriers) > self.number_of_carriers or np.min(self.pilot_subcarriers) < 0:
        if True in self.smaller or True in self.larger or True in self.even:
            raise ValueError(f"\n\n***Error -->\nFollowing input indexes for pilots <{np.array(self.pilot_subcarriers)[self.larger]}> may be larger than max number of carrier index < {self.max_carriers} >;\nand/or pilots <{np.array(self.pilot_subcarriers)[self.smaller]}> may be smaller than min number of carrier index < {self.min_carriers} >;\nand/or selected even pilot index <{np.array(self.pilot_subcarriers)[self.even]}> may be 'even' for ACO-OFDM.\n")

    @sync_track
    def setupOFDMCarriersIndexes(self):
        """Setup carriers indexes for ofdm calculation."""
        
        if self.modulation_config['IM_DD']: # N/2 - 1 actual carriers
            # Get OFDM type
            OFDM_type = next(iter(self.ofdm_type.keys()))

            if OFDM_type == "DCO-OFDM":
                
                # Indexes for all carriers (data carriers + pilot carriers)
                self.all_subcarriers = np.arange(self.number_of_carriers//2 - 1)
                
                # check the pilots vector boundaries for further error detetion
                # self.checkInputPilots(max_carriers = self.number_of_carriers//2 - 1, min_carriers = 0)
                self.checkInputPilots(max_carriers = self.number_of_carriers//2 - 1, min_carriers = 0, ignore_even = True)

                ## TODO -- Check if must substract 1 position here as well (as done for ACO)

                # # old calculation
                # self.pilot_subcarriers = self.all_subcarriers[::(self.number_of_carriers//2 - 1)//(self.number_of_pilots//2 -1)]

            elif OFDM_type == "ACO-OFDM":
                
                # all carriers
                self.all_subcarriers = np.arange(self.number_of_carriers//2 - 1)
                
                # set as negative all components to become 0 on ACO-OFDM
                # (in the even position, since will move to odd after 
                # hermitian application <applyHermitianSymetry>)
                for index in np.arange(1, self.number_of_carriers//2 - 1, 2):
                    self.all_subcarriers[index] = -1
                
                # check the pilots vector boundaries for further error detetion
                self.checkInputPilots(max_carriers = self.number_of_carriers//2 - 1, min_carriers = 0)

                # Substract 1 position to go to even pilots. Will apped one position at beginning on hermitian, so will move back to odd.
                self.pilot_subcarriers = list(np.array(self.pilot_subcarriers) - 1)

                # # old calculation
                # self.pilot_subcarriers = self.all_subcarriers[0::(self.number_of_carriers//2 - 1)//(self.number_of_pilots//2 - 1)]
                
            else:
                raise ValueError(f"\n\n***Error --> Not supported OFDM type: < {OFDM_type} >\n")
        else:
            # For RF OFDM: Use all subcarriers
            self.all_subcarriers = np.arange(self.number_of_carriers)
            
            # check the pilots vector boundaries for error detetion
            self.checkInputPilots(max_carriers = self.number_of_carriers, min_carriers = 0, ignore_even = True)
            
            # # old calculation: For RF OFDM: pilot subcarriers
            # self.pilot_subcarriers = self.all_subcarriers[::self.number_of_carriers//self.number_of_pilots]
        

        ## # old: calculation:
        # make last subcarrier also as a pilot (and increment number of pilots)
        # self.pilot_subcarriers = np.hstack([self.pilot_subcarriers, np.array([self.all_subcarriers[-1]])])
        # self.number_of_pilots += 1
        
        # # # old: calculation: remove duplicate carriers, if any (and -1). Sort list.
        # self.pilot_subcarriers = sorted(list(set([item for item in self.pilot_subcarriers if item != -1])))
        
        # set the indexes for the data subcarriers (just subtract the pilots)
        self.data_subcarriers = np.delete(self.all_subcarriers, self.pilot_subcarriers)
        
        # set number of actual data carriers (through FFT)
        # self.number_of_data_carriers = len(self.data_subcarriers)
        self.number_of_data_carriers = len([item for item in self.data_subcarriers if item != -1])
        
        
        # printDebug(self.pilot_subcarriers)
        # printDebug(self.all_subcarriers)
        # printDebug(self.data_subcarriers)
        # printDebug(self.number_of_data_carriers, stop=True)

    @sync_track
    def setupBitstreamList(self):
        """Generate list of data to be converted into OFDM symbols."""
        
        # Converts bitstream to numpy array
        self.bitstream_frame = np.array([bit for bit in self.bitstream_frame], dtype=int)
        
        # get frame_size and bits_per_symbol
        frame_size = len(self.bitstream_frame)
        bits_per_symbol = int(np.log2(self.mapping_config[1]))
        
        # total number of symbols for transmition for each frame
        number_of_symbols_to_transmit_per_frame = frame_size//bits_per_symbol

        
        # number of symbols per OFDM symbol is the number of data carriers that can be transmitted at once
        # number_of_symbols_per_ofdm_symbol = self.number_of_data_carriers//bits_per_symbol
        
        # number of OFDM symbols for transmission
        # n_ofdm_symbols = number_of_symbols_per_ofdm_symbol//self.number_of_data_carriers
        n_ofdm_symbols = number_of_symbols_to_transmit_per_frame//self.number_of_data_carriers
        
        # number of bits for each ofdm symbol
        self.bits_per_ofdm_symbol = bits_per_symbol*self.number_of_data_carriers
        
        # Pad whole info frame with zeros if necessary
        # if frame_size > n_ofdm_symbols*self.bits_per_ofdm_symbol:
        if number_of_symbols_to_transmit_per_frame > n_ofdm_symbols*self.number_of_data_carriers:
            # Need one more OFDM symbol, then
            n_ofdm_symbols = n_ofdm_symbols + 1
            # number of zeros to pad
            # self.zeros_to_pad = (n_ofdm_symbols + 1)*self.bits_per_ofdm_symbol - frame_size
            self.zeros_to_pad = (n_ofdm_symbols)*self.number_of_data_carriers - number_of_symbols_to_transmit_per_frame
            # number of bits to be zero padded (multiply number of zero subcarriers by number of bits per subcarrier)
            self.zeros_to_pad = self.zeros_to_pad*bits_per_symbol
            # actual zero padded bitstream
            self.bitstream_frame = np.array([0]*self.zeros_to_pad + list(self.bitstream_frame), dtype=int)
        else:
            self.zeros_to_pad = 0
            
        
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
        
        # printDebug(frame_size)
        # printDebug(bits_per_symbol)
        # printDebug(number_of_symbols_to_transmit_per_frame)
        # printDebug(n_ofdm_symbols)
        # printDebug(self.bits_per_ofdm_symbol)
        # printDebug(self.number_of_data_carriers)
        # printDebug(self.bitstream_frame)
        # printDebug(self.bitstream_list)
        # printDebug(temp_bitstream)
        # printDebug(self.zeros_to_pad)
        # printDebug()
    
    @sync_track
    def applyHermitianSymetry(self):
        """Applies the Hermitian Symetry, to make sure IFFT of signal is Real. Input (N/2 - 1); Output (N)."""

        if self.DEBUG:
            printDebug(self.ofdm_tx_data)
            if self.PLOT:
                plotDebug(self.ofdm_tx_data, symbols="ro-", hold = True)

        # Get only the data
        actual_data = self.ofdm_tx_data[0:self.number_of_carriers//2 - 1]
        
        
        # Build hermitian vector
        hermitian = [0] + list(actual_data) + [0] + list(np.conj(np.flipud(actual_data)))
        hermitian = np.array(hermitian)

        # printDebug(actual_data)
        # plotDebug(actual_data, symbols="b*-", hold = False)

        # Use hermitian
        self.ofdm_tx_data = hermitian
        
        if self.DEBUG:
            printDebug(self.ofdm_tx_data)
            if self.PLOT:
                plotDebug(self.ofdm_tx_data, symbols="b*-", hold = False)
        
        # HERMITIAN
        del hermitian
    
    @sync_track
    def applyHermitianDemodulation(self):
        """Applies the Hermitian Demodulation, to retrieve FFT signal."""

        # Get OFDM type
        OFDM_type = next(iter(self.ofdm_type.keys()))
        
        # Get actual data from the correct positions
        if OFDM_type == "DCO-OFDM":
            self.ofdm_symbol_rx = self.ofdm_symbol_rx[1:self.number_of_carriers//2]
            # print(self.number_of_carriers)
            # print(type(self.ofdm_symbol_rx))
            # print(len(self.ofdm_symbol_rx))
        elif OFDM_type == "ACO-OFDM":
            
            self.ofdm_symbol_rx = self.ofdm_symbol_rx[1:self.number_of_carriers//2]
            # self.ofdm_symbol_rx = self.ofdm_symbol_rx[1:self.number_of_carriers][::2]


            # # print(type(self.ofdm_symbol_rx))
            # # print(self.ofdm_symbol_rx)
            # # Get upper and lower data parts (excluding the zeros)
            # # upper_data = self.ofdm_symbol_rx[1:self.number_of_carriers//2]
            # # lower_data = self.ofdm_symbol_rx[self.number_of_carriers//2+1:]
            # upper_data = self.ofdm_symbol_rx[1:self.number_of_carriers//2][::2]
            # lower_data = self.ofdm_symbol_rx[self.number_of_carriers//2+1:][::2]
            # self.ofdm_symbol_rx = np.array(list(upper_data) + list(lower_data))
            # print('upper_data')
            # print(upper_data)
            # print(len(upper_data))
            # print('lower_data')
            # print(lower_data)
            # print(len(lower_data))
            # print('self.ofdm_symbol_rx')
            # print(self.ofdm_symbol_rx)
            # print(len(self.ofdm_symbol_rx))
            # print(type(self.ofdm_symbol_rx))

            # self.ofdm_symbol_rx = self.ofdm_symbol_rx[1::2]
        else:
            raise ValueError(f"\n\n***Error --> Not supported OFDM type: < {OFDM_type} >\n")

        
    @sync_track
    def generateOFDMSymbol(self):
        """Generate OFDM symbols, adding pilots and data carriers."""
        
        
        # Initialize the the ofdm data as zeros
        self.ofdm_tx_data = np.zeros(self.number_of_carriers, dtype=complex)
        
        
        # Introduce the pilots in the subcarrier ofdm symbol
        self.ofdm_tx_data[self.pilot_subcarriers] = self.pilot_value
        
        # Introduce the actual mapped data in the ofdm symbol
        # self.ofdm_tx_data[self.data_subcarriers] = self.mapped_info
        self.only_data_carriers = [item for item in self.data_subcarriers if item != -1]
        self.ofdm_tx_data[self.only_data_carriers] = self.mapped_info
        
        # printDebug(self.number_of_carriers)
        # printDebug(self.ofdm_tx_data)
        # printDebug(self.pilot_subcarriers)
        # printDebug(self.mapped_info)
        # printDebug(self.pilot_value)
        # printDebug()
        
    @sync_track
    def applyIFFT(self):
        """Applies the IDFT on the OFDM symbols."""
        
        if self.DEBUG:
            printDebug(self.ofdm_tx_data)
            if self.PLOT:
                plotDebug(self.ofdm_tx_data, symbols="ro-", hold = True)
        
        if self.use_pyfft:
            # self.ofdm_tx_data = np.fft.ihfft(self.ofdm_tx_data)
            self.ofdm_tx_data = pyfftw.interfaces.numpy_fft.ifft(self.ofdm_tx_data)
        else:
            self.ofdm_tx_data = np.fft.ifft(self.ofdm_tx_data)


        if self.DEBUG:
            printDebug(self.ofdm_tx_data)
            if self.PLOT:
                plotDebug(self.ofdm_tx_data, symbols="b*-", hold = False)
    
    @sync_track
    def applyCp(self):
        """Add the cyclic prefix to the OFDM symbol"""
        
        # Get end of cyclic prefix
        temp_tx_data = self.ofdm_tx_data[-self.number_of_cyclic_prefix:]
        
        # And pass to the beginning of te vector
        self.ofdm_tx_data = np.hstack([temp_tx_data, self.ofdm_tx_data])
        
    
    @sync_track
    # @timer_dec
    def applyDeModulation(self, decoded_sequence = None, seq_idx = None):
        """Wrapper for all functions to apply the OFDM de-modulation on the rx_data."""
        
        # when de-mapping, the ouput starts as an empty list (temp_list)
        temp_list = []

        # modulation_config = decoded_sequence['seq_mod'][seq_idx]
        
        # Get number of OFDM symbols for each sequence step
        n_symbols = decoded_sequence['tx_num_symbols'][seq_idx]
        # Get number of padded zeros for that sequence step
        self.zeros_to_pad = decoded_sequence['seq_zeros_to_pad'][seq_idx]
        

        # Checks how many symbols there are from tx side here.
        # This could also easely be calcuated at rx, since we know at which rx sequence we are.
        # This 'n_symbols' is derived from number of "agreed" FFT symbols, cyclic prefix, and time duration of each symbol.
        # We could also use one of the initial OFDM symbols to get this data for next PAYLOAD sequence, as long as that particular sequence is agreed.
        next_min_pos = 0
        next_max_pos = 0
        for symbol_idx in range(0, n_symbols):
            
            # Get the ratio between the initial sample frequency and the actual used one (got from Modulator)
            ratio = int(self.sample_frequency / (self.total_subcarriers / self.ofdm_duration))

            # printDebug(self.sample_frequency)
            # printDebug((self.total_subcarriers / self.ofdm_duration))
            # printDebug(self.modulation_config)

            # Get next OFDM symbol positions, expanding depending on the atual sample ratio, in contrast with original max frequency
            next_min_pos = (self.number_of_cyclic_prefix + self.number_of_carriers)*(symbol_idx) * ratio
            next_max_pos = (self.number_of_cyclic_prefix + self.number_of_carriers)*(symbol_idx+1) * ratio
            # next_min_pos = (carriers_times_sample_ratio)*(symbol_idx)
            # next_max_pos = (carriers_times_sample_ratio)*(symbol_idx+1)
            # next_min_pos = (self.total_subcarriers * ratio)*(symbol_idx)
            # next_max_pos = (self.total_subcarriers * ratio)*(symbol_idx+1)

            # self.sample_frequency = (self.total_subcarriers) / self.ofdm_duration

            # # Apply ratio
            # next_min_pos = int(next_min_pos*ratio)
            # next_max_pos = int(next_max_pos*ratio)

            # Sample the expanded signal (due to larger sample frequency), and recover original equivalent to the subcarriers
            # Set the current RX OFDM symbol for the sampled OFDM
            
            # printDebug(ratio)
            # printDebug(self.ofdm_rx_data)
            self.setOFDMSymbolRx(self.ofdm_rx_data[next_min_pos:next_max_pos][::ratio])

            # printDebug(self.number_of_cyclic_prefix)
            # printDebug(self.number_of_carriers)
            # printDebug(self.ofdm_symbol_rx)
            
            if self.DEBUG:
                printDebug(self.total_subcarriers)
                printDebug(self.sample_frequency)
                # printDebug(self.ofdm_rx_data)
                printDebug(self.number_of_cyclic_prefix)
                printDebug(self.number_of_carriers)
                printDebug(ratio)
                printDebug(n_symbols)
                printDebug(next_min_pos)
                printDebug(next_max_pos)
                printDebug(symbol_idx)
            if self.PLOT:
                plotDebug(self.ofdm_rx_data, symbols='bo-', hold=True)
                # plotDebug(self.ofdm_rx_data[next_min_pos:next_max_pos], symbols='ro-', hold=False)
                plotDebug(self.ofdm_symbol_rx, symbols='ro-', hold=False)
                # expanded_ofdm = self.ofdm_rx_data[next_min_pos:next_max_pos]
                # sampled_ofdm = self.ofdm_rx_data[next_min_pos:next_max_pos][::ratio]
                # plotDebug(sampled_ofdm, symbols='bo-', hold=True)
                # plotDebug(expanded_ofdm, symbols='ro-')
            
            
            # Remove the cyclic prefix in the OFDM symbol
            self.removeCp()
            
            # printDebug(decoded_sequence.keys())
            # printDebug(decoded_sequence['tx_wave_list'][seq_idx])
            # plotDebug(decoded_sequence['tx_wave_list'][seq_idx], symbols="g-", hold = False)
            
            # Applies the FFT
            self.applyFFT()

            # plotDebug(self.ofdm_symbol_rx, symbols="ro-", hold = True)
            
            # # Only for IM/DD
            # if self.modulation_config['IM_DD']:
            #     # Apply hermitian demodulation
            #     self.applyHermitianDemodulation()
            
            # plotDebug(self.ofdm_symbol_rx, symbols="b*-", hold = False)

            # Get info from pre-calculated from tx (that could also be reckoned here at rx)
            self.pilot_value = decoded_sequence['seq_pilot_value'][seq_idx]
            self.all_subcarriers = decoded_sequence['seq_all_carriers'][seq_idx]
            self.pilot_subcarriers = decoded_sequence['seq_pilot_carriers'][seq_idx]
            self.data_subcarriers = decoded_sequence['seq_data_carriers'][seq_idx]

            # Estimates the channel response
            self.estimateChannel()

            if self.PLOT:
                
                ### TODO - Get contribution of multiple CIRs... not sure how to do that yet
                
                # For each CIR in the CIR list (one CIR for each lamp, if appliable)
                for idx_cir, (CIR, CIR_time) in enumerate(self.list_of_channel_response):
                    
                    # show = idx_cir == len(self.list_of_channel_response) - 1
                    show = True
                    self.compareOFDMChannelResponse(
                        current_channel = CIR,
                        channel_time = CIR_time,
                        show = show
                    )
            
            if self.PLOT:
                plotDebug(self.ofdm_symbol_rx, symbols='k-', label="RX wave", hold=True)
                plotDebug(self.ofdm_symbol_rx, symbols='ro', label="Data", hold=True)
                
                plotDebug(self.ofdm_symbol_rx[self.pilot_subcarriers], self.pilot_subcarriers, symbols='bo', label="Pilots", hold=False)
            
            # Applies equalization, given the channel response
            self.applyEqualization()

            # plotDebug(self.ofdm_symbol_rx, symbols="ro-", hold = True)

            # Only for IM/DD
            if self.modulation_config['IM_DD']:
                # Apply hermitian demodulation
                self.applyHermitianDemodulation()
            
            # printDebug(self.ofdm_symbol_rx)
            # plotDebug(self.ofdm_symbol_rx, symbols="b*-", hold = False)
            
            if self.PLOT:
                # printDebug(self.ofdm_symbol_rx)
                plotDebug(self.ofdm_symbol_rx, symbols='mo-', label="Eq. RX wave")
            
            # # Get the mapped info from TX for plotting and compare ## TODO -- Needed?
            # self.mapped_info = decoded_sequence['seq_all_mapped_info'][seq_idx][symbol_idx]
            # printDebug(self.mapped_info)

            # Get the mapped ouput signal, with its associated constellation
            self.getConstellation()
            
            # printDebug(self.mapped_output)
            
            # Creates the de-mapping object.
            self.de_mapping_obj = Mapping(
                bitstream_frame = None,
                mapping_config = self.mapping_config,
                sync_obj = self.sync_obj
            )

            # # Set the mapped output as the info for de-mapping
            # self.de_mapping_obj.setMappedInfo(self.mapped_output)
            
            # Set demapping from mapped_output, just calculated from 'getConstellation'. Returns the decoded data.
            self.de_mapping_obj.applyDemapping(self.mapped_output)


            if self.PLOT:
                # Given de-mapping, plot found constelattions from mapped_output
                # show = idx_data == len(self.ofdm_rx_data_list) - 1
                show = True
                self.showFoundConstellation(
                    self.de_mapping_obj.getFoundConstellation(),
                    self.de_mapping_obj.getConstellation(),
                    show = show
                )
            
            # Get seriallized data of interest
            temp_list.append(self.de_mapping_obj.getRxBitstreamFrame())
                
                
            self.bitstream_frame = []
        
        
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

        # # # # Only for IM/DD
        # # if self.modulation_config['IM_DD']:
        # #     pass
        
        # # printDebug(self.ofdm_rx_data)
        # # plotDebug(self.ofdm_rx_data, self.ofdm_time, symbols='bo-')

        # # cuttof = (0.1)*(1/Global.time_frame)*0
        # # filter_type = 'hp'
        # # filter_order = 20
        # # self.ofdm_rx_data = lib.butterFilter(self.ofdm_rx_data, cuttof = cuttof, \
        # # filter_order = filter_order, filter_type = filter_type)
        # # plotDebug(self.ofdm_rx_data, self.ofdm_time, symbols='bo-')
        
        
        
        # # Applies the FFT
        # self.applyFFT()
        
        
        # # Estimates the channel response
        # self.estimateChannel()
        
        # if self.PLOT:
            
        #     ### TODO - Get contribution of multiple CIRs... not sure how to do that yet
            
        #     # For each CIR in the CIR list (one CIR for each lamp, if appliable)
        #     for idx_cir, CIR in enumerate(self.list_of_channel_response):
                
        #         # show = idx_cir == len(self.list_of_channel_response) - 1
        #         show = True
        #         self.compareOFDMChannelResponse(
        #             CIR,
        #             show = show
        #         )
        
        
        # # Applies equalization, given the channel response
        # self.applyEqualization()
        
        
        # # Get the mapped ouput signal, with its associated constellation
        # self.getConstellation()
        
        
        # # Creates the de-mapping object.
        # self.de_mapping_obj = Mapping(
        #     bitstream_frame = None,
        #     mapping_config = self.mapping_config,
        #     sync_obj = self.sync_obj
        # )
        
        
        # # Set demapping from mapped_output
        # self.de_mapping_obj.applyDemapping()
        
        
        # if self.PLOT:
        #     # Given de-mapping, plot found constelattions from mapped_output
        #     # show = idx_data == len(self.ofdm_rx_data_list) - 1
        #     show = True
        #     self.showFoundConstellation(
        #         self.de_mapping_obj.getFoundConstellation(),
        #         self.de_mapping_obj.getConstellation(),
        #         show = show
        #     )
        
        
        # # Get seriallized data of interest
        # temp_list.append(self.de_mapping_obj.getRxBitstreamFrame())
            
            
        # self.bitstream_frame = []
        
        # for bitstream in temp_list:
        #     self.bitstream_frame = self.bitstream_frame + list(bitstream)
        
        # zero_pad_counter = 0
        # temp_frame = ''
        # for bit in list(self.bitstream_frame):
        #     # print(bit)
        #     if self.remove_padded_zeros:
        #         if zero_pad_counter >= self.zeros_to_pad:
        #             temp_frame += str(bit)
        #     else:
        #         temp_frame += str(bit)
        #     zero_pad_counter += 1
        # self.bitstream_frame = temp_frame
        # del temp_list
        # del temp_frame
    
    # @sync_track
    # # @timer_dec
    # def FLPDecode(self, data, modulation_config = None):
    #     """Remove group delay (that should be previoulsy determined) to synchronize received OFDM data."""

    #     printDebug(modulation_config)
        
    # @sync_track
    # # @timer_dec
    # def syncRxData(self, decoded_sequence = None, seq_idx = None):
    #     """Get tx_data info to do cross-correlation, and find actual phase delay. The tx_data is supposed here to be generated at the rx end, where we know the pattern."""

    #     # Get original tx_data and time for current 'seq_idx'.
    #     # This is the equivalent of the RX side re-creating the expected sync data for synchronization.
    #     tx_data = decoded_sequence['tx_wave_list'][seq_idx]
    #     tx_time = decoded_sequence['tx_time_list'][seq_idx]
    #     # Samples it as it's done at the ADC/DAC levels... b/c we need both tx and rx at the same time frames for cross-correlation
    #     tx_data, tx_time = lib.sampleSignal(tx_data, tx_time, self.sample_frequency)
        
    #     # Get positions for min and max time points for current sequence
    #     min_r = int(decoded_sequence['seq_start_time'][seq_idx] * self.sample_frequency)
    #     max_r = int(decoded_sequence['seq_end_time'][seq_idx] * self.sample_frequency)

    #     # Get range for ofdm rx signal for sync.
    #     rx_data = self.ofdm_rx_data[min_r:max_r]

    #     # # get gradients of signals. # TODO --- Actually need gradients?
    #     # s0 = np.gradient(np.gradient(rx_data))
    #     # s1 = np.gradient(np.gradient(tx_data))
    #     s0 = rx_data
    #     s1 = tx_data
    #     # get max argument for cross-correlatin betwwen rx_data and tx_data
    #     # max_arg = np.argmax(signal.correlate(s1, s0)) + 1 ## +1 for most correct cross-correlation
    #     max_arg = np.argmax(signal.correlate(s1, s0)) + 0

    #     # Get delay in steps for given rx wave
    #     if len(tx_data) > max_arg:
    #         self.phase_delay_steps = len(tx_data) - max_arg
    #     else:
    #         raise ValueError(f"\n\n***Error --> Delay is too large to be synced...\n")
    #         printDebug(max_arg/self.sample_frequency)
    #         printDebug(len(tx_data)/self.sample_frequency)
    #         self.phase_delay_steps = -max_arg-1 + len(tx_data)
    #         # self.phase_delay_steps = max_arg
        
    #     # Get delay in time for given rx wave
    #     self.phase_delay_time = self.phase_delay_steps/self.sample_frequency

    #     if self.PLOT:
    #         sync_data = np.roll(rx_data, -self.phase_delay_steps)
    #         diff_error = sync_data - tx_data
    #         plotDebug(tx_data, self.ofdm_time[min_r:max_r], symbols='bo-', hold=True)
    #         plotDebug(rx_data, self.ofdm_time[min_r:max_r], symbols='ro-', hold=True)
    #         plotDebug(sync_data, self.ofdm_time[min_r:max_r], symbols='mo-', hold=True)
    #         plotDebug(diff_error, self.ofdm_time[min_r:max_r], symbols='ko-', title="Synchronization of Rx data")
        
    #     if self.PLOT:
    #         plotDebug(self.ofdm_rx_data, self.ofdm_time, symbols='ro-', hold=True)
        
    #     # Now, sync whole OFDM data, with given discovered phase delay.
    #     self.ofdm_rx_data = np.roll(self.ofdm_rx_data, -self.phase_delay_steps)
        
    #     if self.PLOT:
    #         plotDebug(self.ofdm_rx_data, self.ofdm_time, symbols='bo-', title="Original (red) and synced (blue) busrt RX signal.")
        
    #     # Returns next sequence index for demodulation. Also, calculate delay.
    #     return seq_idx + 1, self.phase_delay_time, self.phase_delay_steps

    
    
    @sync_track
    def removeCp(self):
        """Removes the cyclic prefix from 'ofdm_rx_data'."""
        
        self.ofdm_symbol_rx = self.ofdm_symbol_rx[self.number_of_cyclic_prefix:(self.number_of_cyclic_prefix + self.number_of_carriers)]
        
    @sync_track
    def applyFFT(self):
        """Applies the DFT on the OFDM symbols."""
        
        if self.use_pyfft:
            # self.ofdm_symbol_rx = np.fft.hfft(self.ofdm_symbol_rx)
            self.ofdm_symbol_rx = pyfftw.interfaces.numpy_fft.fft(self.ofdm_symbol_rx)
        else:
            self.ofdm_symbol_rx = np.fft.fft(self.ofdm_symbol_rx)
            
    @sync_track
    def estimateChannel(self):
        """Analyze pilots to get the channel estimation."""

        outliers = []
        self.ofdm_symbol_rx, outliers = lib.removeOutliers(self.ofdm_symbol_rx, sigma_threshold = 6, default_outlier = 0)

        if not self.modulation_config['IM_DD']:
            OFDM_type = None

            # remove outliers from pilot carriers, if any
            self.pilot_subcarriers = [pilot for pilot in self.pilot_subcarriers if pilot not in outliers]

            # self.estimated_pilots_response = self.ofdm_symbol_rx[self.pilot_subcarriers] / self.pilot_value
            # channel_response_modulus = interpolate.interp1d(self.pilot_subcarriers, abs(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, len(self.all_subcarriers) , 1))
            # channel_response_angle = interpolate.interp1d(self.pilot_subcarriers, np.angle(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, len(self.all_subcarriers) , 1))

            # pilot_subcarriers_freq = (np.array(self.pilot_subcarriers)+1)/Global.time_frame
            pilot_subcarriers_freq = (np.array(self.pilot_subcarriers)+1)/self.ofdm_duration
            # printDebug(self.pilot_subcarriers)
            # printDebug(pilot_subcarriers_freq)

            # printDebug(self.pilot_value)
            # printDebug(self.ofdm_symbol_rx)
            # printDebug(self.estimated_pilots_response)
            # plotDebug(self.ofdm_symbol_rx, symbols='bo-')
            
            self.estimated_pilots_response = self.ofdm_symbol_rx[self.pilot_subcarriers] / self.pilot_value
            # printDebug(self.estimated_pilots_response)
            # printDebug(np.abs(self.estimated_pilots_response))
            # plotDebug(self.estimated_pilots_response, symbols='bo-')
            # plotDebug(np.abs(self.estimated_pilots_response), symbols='bo-')
            
            
            # = (N_FFT + N_FFT/4) = 1.25*N_FFT
            # self.estimated_channel_model = interpolate.interp1d(pilot_subcarriers_freq, self.estimated_pilots_response, kind=Global.interpolation_type, fill_value="extrapolate")
            # self.estimated_channel_response = interpolate.interp1d(pilot_subcarriers_freq, self.estimated_pilots_response, kind=Global.interpolation_type, fill_value="extrapolate")
            
            # Actual valid carriers
            self.valid_carriers = np.arange(0, len(self.all_subcarriers))
            # valid_carriers_freq = (self.valid_carriers + 1)/Global.time_frame
            valid_carriers_freq = (self.valid_carriers + 1)/self.ofdm_duration

            # printDebug(pilot_subcarriers_freq)
            # printDebug(self.estimated_pilots_response)

            channel_response_modulus_model = interpolate.interp1d(pilot_subcarriers_freq, abs(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")
            channel_response_angle_model = interpolate.interp1d(pilot_subcarriers_freq, np.angle(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")
            
            channel_response_modulus = channel_response_modulus_model(valid_carriers_freq)
            channel_response_angle = channel_response_angle_model(valid_carriers_freq)

            ##########self.estimated_channel_response = channel_response_modulus * np.exp(1j*channel_response_angle)
            # self.estimated_channel_response = channel_response_modulus * np.exp(1j*channel_response_angle + 1j*2*np.pi/Global.group_delay)
            # self.estimated_channel_response = self.estimated_channel_response * np.exp(-1j*2*np.pi*Global.group_delay)
            # self.estimated_channel_response = self.estimated_channel_response * np.exp(1j*2*np.pi/Global.group_delay)


            # plotDebug(channel_response_modulus, valid_carriers_freq)
            # plotDebug(self.estimated_channel_response, valid_carriers_freq, symbols= 'bo-')

            
            # printDebug(interp(pilot_subcarriers_freq))
            # printDebug(pilot_subcarriers_freq)
            # plotDebug((interp(pilot_subcarriers_freq)), pilot_subcarriers_freq, symbols='bo-')
            # self.estimated_channel_response = interpolate.interp1d(pilot_subcarriers_freq, self.estimated_pilots_response, kind=Global.interpolation_type, fill_value="extrapolate")
            # frequencies = np.arange(int(len(Global.base_time_vector)))/Global.time_frame
            # self.estimated_channel_response = interp(frequencies)
            # plotDebug(self.estimated_channel_response)



        else:
            # Get OFDM type
            OFDM_type = next(iter(self.ofdm_type.keys()))

            ########### self.pilot_subcarriers = [pilot for pilot in self.pilot_subcarriers if pilot not in outliers]

            self.pilot_subcarriers = [p + 1 for p in self.pilot_subcarriers]

            for idx,pilot in enumerate(self.pilot_subcarriers.copy()):
                # self.ofdm_symbol_rx = self.ofdm_symbol_rx[1:self.number_of_carriers//2]
                # hermitian = [0] + list(actual_data) + [0] + list(np.conj(np.flipud(actual_data)))
                # print(pilot + int(len(self.ofdm_symbol_rx)/2))
                self.pilot_subcarriers.append(int(len(self.ofdm_symbol_rx)) - pilot)
            
            self.pilot_subcarriers.sort()

            # printDebug(self.pilot_subcarriers)
            # printDebug(self.ofdm_symbol_rx[self.pilot_subcarriers])
            # printDebug(self.ofdm_symbol_rx)
            # printDebug(self.pilot_value)

            # plotDebug(self.ofdm_symbol_rx[self.pilot_subcarriers], symbols="k*-", hold = True)
            # plotDebug(self.ofdm_symbol_rx, symbols="b-", hold = False)
            
            
            # Get the channel response by dividing the pilot subcarriers by the known pilot value.
            if OFDM_type == "DCO-OFDM":
                self.estimated_pilots_response = self.ofdm_symbol_rx[self.pilot_subcarriers] / self.pilot_value
                # interpolates the estimated response, to get the actual modulus and angle for estimated channel response
                channel_response_modulus = interpolate.interp1d(self.pilot_subcarriers, abs(self.estimated_pilots_response),kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, (len(self.all_subcarriers)+1)*2 , 1))
                channel_response_angle = interpolate.interp1d(self.pilot_subcarriers, np.angle(self.estimated_pilots_response),kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, (len(self.all_subcarriers)+1)*2 , 1))
                ####### channel_response_modulus = interpolate.interp1d(self.pilot_subcarriers, abs(self.estimated_pilots_response),kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, len(self.all_subcarriers) , 1))
                ####### channel_response_angle = interpolate.interp1d(self.pilot_subcarriers, np.angle(self.estimated_pilots_response),kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, len(self.all_subcarriers) , 1))
                # printDebug('self.all_subcarriers')
                # printDebug(self.all_subcarriers)
            elif OFDM_type == "ACO-OFDM":
                # multiply by 2 at RX, because the ACO simmetry makes the IFFT output 2x smaller at TX
                self.ofdm_symbol_rx = self.ofdm_symbol_rx*2
                # printDebug(self.ofdm_symbol_rx*2)
                # Correct positions for ACO pilot carriers
                self.estimated_pilots_response = self.ofdm_symbol_rx[self.pilot_subcarriers] / self.pilot_value
                # self.estimated_pilots_response = self.ofdm_symbol_rx[[int(item//2) for item in self.pilot_subcarriers]] / self.pilot_value

                # plotDebug(self.estimated_pilots_response, symbols="k*-", hold = False)

                # printDebug('CHANNEL')
                # printDebug(self.ofdm_symbol_rx[self.pilot_subcarriers])
                # printDebug(self.ofdm_symbol_rx)
                # printDebug(self.pilot_subcarriers)
                # printDebug(self.pilot_value)
                # printDebug(self.estimated_pilots_response)
                # printDebug('self.all_subcarriers')
                # printDebug(self.all_subcarriers)
                
                self.valid_carriers = [item if item != -1 else self.all_subcarriers[idx-1]+1 for idx,item in enumerate(self.all_subcarriers) ]
                
                # self.valid_carriers = [int(item//2) for item in self.all_subcarriers if item != -1]
                # self.all_subcarriers = self.valid_carriers
                # self.valid_carriers = self.all_subcarriers

                # printDebug(self.valid_carriers)
                # printDebug(self.pilot_subcarriers)
                # printDebug(self.all_subcarriers)

                # assad

                channel_response_modulus = interpolate.interp1d(self.pilot_subcarriers, abs(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, (len(self.all_subcarriers)+1)*2 , 1))
                channel_response_angle = interpolate.interp1d(self.pilot_subcarriers, np.angle(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, (len(self.all_subcarriers)+1)*2 , 1))
                ####### channel_response_modulus = interpolate.interp1d(self.pilot_subcarriers, abs(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, len(self.all_subcarriers) , 1))
                ####### channel_response_angle = interpolate.interp1d(self.pilot_subcarriers, np.angle(self.estimated_pilots_response), kind=Global.interpolation_type, fill_value="extrapolate")(np.arange(0, len(self.all_subcarriers) , 1))
                
                # join modulus and phase to create the estimated channel response
            
            elif OFDM_type is not None:
                raise ValueError(f"\n\n***Error --> Not supported OFDM type: < {OFDM_type} >\n")

        # if self.modulation_config['IM_DD']:
        #     printDebug(self.estimated_channel_response)
        
        # self.valid_carriers = self.all_subcarriers
        self.valid_carriers = np.arange(0, len(self.all_subcarriers))
        self.estimated_channel_response = channel_response_modulus * np.exp(1j*channel_response_angle)
        # print(self.estimated_channel_response)
        # print(len(self.estimated_channel_response))
        
    @sync_track
    def applyEqualization(self):
        """Equalize, given OFDM symbols from DFT operation, and the channel estimate."""
        
        # printDebug('applyEqualization')
        # plotDebug(self.estimated_channel_response)
        # printDebug(self.ofdm_symbol_rx)

        # self.mapped_output_pilots = self.ofdm_symbol_rx[self.pilot_subcarriers]
        self.ofdm_symbol_rx = self.ofdm_symbol_rx / self.estimated_channel_response
        

    @sync_track
    def getConstellation(self):
        """Given equalized data, return the 'mapped_output', with carriers related to data only."""
        
        # printDebug(self.ofdm_symbol_rx)
        # printDebug(self.data_subcarriers)
        # printDebug([item for item in self.data_subcarriers if item != -1])
        # printDebug(self.ofdm_symbol_rx[self.data_subcarriers])
        # printDebug(self.ofdm_symbol_rx[[item for item in self.data_subcarriers if item != -1]])
        
        # printDebug('self.ofdm_symbol_rx =\n', self.ofdm_symbol_rx[[item for item in self.data_subcarriers if item != -1]])
        # printDebug('self.ofdm_symbol_rx = ', len(self.ofdm_symbol_rx[[item for item in self.data_subcarriers if item != -1]]))
        # printDebug('self.mapped_info =\n', self.mapped_info)
        # printDebug('self.mapped_info = ', len(self.mapped_info))
        # self.mapped_output = self.ofdm_symbol_rx[self.data_subcarriers]
        self.mapped_output = self.ofdm_symbol_rx[[item for item in self.data_subcarriers if item != -1]]
        # self.mapped_output_pilots = self.ofdm_symbol_rx[self.pilot_subcarriers]
    
    @sync_track
    def compareOFDMChannelResponse(self, current_channel, channel_time, show = False):
        """Compares the OFDM channel response with estimated. Must first set all channel responses."""
        
        temp_sub_carriers = [item for item in self.all_subcarriers if item != -1]
        # Calculates the actual CIR
        # CIR = np.fft.fft(current_channel, self.number_of_carriers)
        # CIR = np.fft.fft(current_channel, len(self.all_subcarriers))
        # CIR = np.fft.fft(current_channel, len(temp_sub_carriers))
        # CIR = np.fft.fft(current_channel, len(self.valid_carriers))
        # x = [int(item*2) for item in self.valid_carriers]
        # x = np.arange(0, 64)
        # freq = np.arange(self.number_of_carriers, 0, -3)
        # freq = np.arange(0, self.number_of_carriers, 1) - 4
        
        # freq = np.arange(0, self.number_of_carriers, 1)
        freq = np.arange(0, self.total_subcarriers, 1)
        # freq = np.arange(0, self.valid_carriers, 1)
        # get actual frequencies for each subcarrier
        # freq = (freq+1)/Global.time_frame
        freq = (freq+1)/self.ofdm_duration
        
        # Actual frequency for the pitlos
        # pilot_subcarriers_freq = np.arange(0, self.pilot_subcarriers, 1)
        # pilot_subcarriers_freq = (pilot_subcarriers_freq+1)/Global.time_frame

        # pilot_subcarriers_freq = (np.array(self.pilot_subcarriers)+1)/Global.time_frame
        pilot_subcarriers_freq = (np.array(self.pilot_subcarriers)+1)/self.ofdm_duration

        # printDebug(self.pilot_subcarriers)
        # printDebug(self.valid_carriers)
        # self.all_subcarriers = np.arange(self.number_of_carriers)
        # printDebug(self.all_subcarriers)
        ##### TODO ---> re-analysed, and should be full carriers....
        self.valid_carriers = np.arange(self.number_of_carriers)


        # Actual valid carriers
        # valid_carriers_freq = (self.valid_carriers + 1)/Global.time_frame
        valid_carriers_freq = (self.valid_carriers + 1)/self.ofdm_duration
        
        
        ## TODO --- DEBUG WHY THE 'ACTUAL' CHANNEL RESPONSE IS NOT MATCHING THE PILOTS ESTIMATES??
        ## TODO --- LOOKS LIKE THE 'ABS' HELPS, SINCE THE OFDM FOR LIFI USES ONLY 'REAL' DATA.
        ## TODO --- IS THERE AN ISSUE WITH THE CONVOLUTION FOR THIS OFDM?

        # if self.modulation_config['IM_DD']:
        #     current_channel = abs(current_channel)

        # fourierTransform = np.fft.fft(current_channel)/len(current_channel)
        # fourierTransform = fourierTransform[range(int(len(current_channel)/2))] # Exclude sampling frequency

        # Get FFT of channel response
        CIR = np.fft.fft(current_channel)
        
        # Get equivalent frequencies
        frequencies = np.arange(int(len(channel_time)))/self.ofdm_duration
        
        # Interpolates the channel frequency response, but for the frequencies on the OFDM channel
        # which are 1/f, 2/f ... N/f; where N is the total number of subcarriers (N_FFT + N_pilots) =
        # Ex: (N_FFT + N_FFT/4) = 1.25*N_FFT
        interp = interpolate.interp1d(frequencies, CIR, kind=Global.interpolation_type, fill_value="extrapolate")
        
        ###### plotDebug((interp(freq)), freq, symbols='bo-')
        ###### plotDebug(abs(interp(freq)), freq, symbols='bo-')
        ###### plotDebug(np.angle(interp(freq))/np.pi*180, freq, symbols='bo-')

        plot_type = 'angle'
        plot_type = 'abs'
        # plot_type = 'complex'

        # printDebug(self.estimated_channel_model(valid_carriers_freq))
        # plotDebug(self.estimated_channel_model(valid_carriers_freq), valid_carriers_freq)
        
        if plot_type == 'complex':
            plt.plot(valid_carriers_freq, (interp(valid_carriers_freq)/np.max(interp(valid_carriers_freq))), 'go-', label='Actual channel response')
            plt.plot(valid_carriers_freq, (self.estimated_channel_response)/np.max(self.estimated_channel_response), 'ko-', label='Interpolated estimated channel')
            plt.stem(pilot_subcarriers_freq, (self.estimated_pilots_response)/np.max(self.estimated_pilots_response), label='Estimated pilots')
        elif plot_type == 'abs':
            plt.plot(valid_carriers_freq, abs(interp(valid_carriers_freq))/np.max(abs(interp(valid_carriers_freq))), 'go-', label='Actual channel response')
            # plt.plot(valid_carriers_freq, abs(self.estimated_channel_response)/np.max(self.estimated_channel_response), 'ko-', label='Interpolated estimated channel')
            plt.stem(pilot_subcarriers_freq, abs(self.estimated_pilots_response)/np.max(self.estimated_pilots_response), label='Estimated pilots')
        elif plot_type == 'angle':
            plt.plot(valid_carriers_freq, np.angle(interp(valid_carriers_freq))/np.pi*180, 'go-', label='Actual channel response')
            plt.plot(valid_carriers_freq, np.angle(self.estimated_channel_response)/np.pi*180, 'ko-', label='Interpolated estimated channel')
            plt.stem(pilot_subcarriers_freq, np.angle(self.estimated_pilots_response)/np.pi*180, label='Estimated pilots')
        

        # SOME ISSUE HERE..........
        # plt.plot(valid_carriers_freq, abs(interp(freq)), 'go-', label='Actual channel response')
        # plt.plot(freq, interp(freq), 'go-', label='Actual channel response')
        # plt.plot(frequencies, abs(CIR)/np.max(abs(CIR)), 'go-', label='current_channel')
        # plt.plot(np.arange(0, self.number_of_carriers), abs(self.estimated_channel_response), 'bo', label='Interpolated estimated channel')
        # plt.plot(self.all_subcarriers, abs(self.estimated_channel_response), 'bo', label='Interpolated estimated channel')
        # plt.stem(pilot_subcarriers_freq[1:], abs(self.estimated_pilots_response[1:])/np.max(self.estimated_pilots_response[1:]), label='Estimated pilots')
        plt.grid(True)
        plt.title('Channel response estimations')
        plt.xlabel('Subcarrier indexes')
        plt.ylabel('$|H(f)|$')
        plt.legend(fontsize=10)
        # plt.ylim(0, np.max([np.max(abs(self.estimated_channel_response)), np.max(abs(CIR))])*1.1)
        # plt.ylim(0, 1.1)
        plt.show(block=show)

        
    @sync_track
    def showFoundConstellation(self, found_constellation, constellation, show = False):
        """Plots the found constellation."""
        
        # printDebug(found_constellation)
        # plotDebug(found_constellation)
        # printDebug(self.mapped_output)
        # plot all the estimated constellations
        for qam, estimated in zip(self.mapped_output, found_constellation):
            # plotDebug(constellation.real, constellation.imag, symbols='ko')
            # plotDebug([qam.real, estimated.real], [qam.imag, estimated.imag], symbols='b-o')
            # sad
            plt.plot(constellation.real, constellation.imag, 'ko')
            plt.plot([qam.real, estimated.real], [qam.imag, estimated.imag], 'b-o')
            plt.plot(found_constellation.real, found_constellation.imag, 'ro')
            # plt.plot(found_constellation.real, found_constellation.imag, 'ro')
        
        # for qam in self.mapped_output_pilots:
        #     plt.plot([qam.real, self.pilot_value.real], [qam.imag, self.pilot_value.imag], 'g-*')
        #     # plt.plot(qam.real, qam.imag, 'g-o')
        
        plt.grid(True)
        plt.title('Estimated constellation')
        plt.xlabel('Real')
        plt.ylabel('Imagingary')
        plt.legend(fontsize=10)
        plt.show(block=show)
        # plt.show(show)
        
    
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
    def getNumberOfDataCarriers(self):
        """Returns value of self.number_of_data_carriers"""
        
        
        return self.number_of_data_carriers
    
    @sync_track
    def setNumberOfDataCarriers(self, number_of_data_carriers):
        """Set new value for self.number_of_data_carriers"""
        
        
        self.number_of_data_carriers = number_of_data_carriers
    
    @sync_track
    def getDataCarriers(self):
        """Returns value of self.data_subcarriers"""
        
        return self.data_subcarriers
    
    @sync_track
    def setDataCarriers(self, data_subcarriers):
        """Set new value for self.data_subcarriers"""
        
        self.data_subcarriers = data_subcarriers

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
    def getOFDMRxData(self):
        """Returns value of self.ofdm_rx_data"""
        
        return self.ofdm_rx_data
    
    @sync_track
    def setOFDMRxData(self, ofdm_rx_data):
        """Set new value for self.ofdm_rx_data"""
        
        self.ofdm_rx_data = ofdm_rx_data
    
    @sync_track
    def getOFDMTime(self):
        """Returns value of self.ofdm_time"""
        
        return self.ofdm_time
    
    @sync_track
    def setOFDMTime(self, ofdm_time):
        """Set new value for self.ofdm_time"""
        
        self.ofdm_time = ofdm_time
    
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
    def getSampleFrequency(self):
        """Returns value of self.sample_frequency"""
        
        return self.sample_frequency

    @sync_track
    def setSampleFrequency(self, sample_frequency):
        """Set new value for self.sample_frequency"""
        
        self.sample_frequency = sample_frequency
    
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