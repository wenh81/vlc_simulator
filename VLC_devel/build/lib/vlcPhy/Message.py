from .common_imports import *

class Message(object):
    
    def __init__(self, n_frames, seq_config, sync_obj):
        """Constructor of Message."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Message") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Message")
        
        if self.DEBUG:
            print('Running Message...')
        
        # Contains a dict with all the information to be sent, for example, as {"type": "image", "data": [image1, image2]}
        self.input_info = None

        # List of bitstream info for transmission. Each position is of type 'bitstream.BitStream'.
        self.bitstream_frames = []

        # Number of frames to be transmitted sequentially.
        self.number_of_frames = n_frames

        # Bitstream list info after receiveing, depending on number of frames.
        self.rx_bitstream_frames = None

        # dict with all recovered received information.
        self.output_info = None
        
        # Add to the message dict in sync object, the number of frames (messages) to be sent
        # self.sync_obj.message_dict["n_frames"] = n_frames
        # self.sync_obj.message_dict["type"] = Global.input_info["type"]
        self.sync_obj.appendToMessageDict("n_frames", n_frames)
        self.sync_obj.appendToMessageDict("Sequence", seq_config)
        self.sync_obj.appendToMessageDict("type", 'DUMMY')
        # self.sync_obj.appendToMessageDict("type", Global.input_info["type"])

        # All configuration for the sequence to be transmitted (like sync header, payloads, mapping, config, etc.)
        self.sequence_config = seq_config
    
    
    # @sync_track
    # def serialize_boolean_array(self, array):
    #     """Takes a numpy.array with boolean values and converts it to a space-efficient
    #     binary representation.
    #     """
    #     return np.packbits(array).tobytes()

    # @sync_track
    # def deserialize_boolean_array(self, serialized_array, shape):
    #     """Inverse of serialize_boolean_array."""
    #     num_elements = np.prod(shape)
    #     packed_bits = np.frombuffer(serialized_array, dtype='uint8')
    #     result = np.unpackbits(packed_bits)[:num_elements]
    #     result.shape = shape
    #     return result

    @sync_track
    def decodeBurstSequence(self):
        """Decode the burst sequence for Tx. Checks the config for all 'subfields' on each 'field'"""

        # Whole burst sequence decoded
        self.decoded_seq = defaultdict(list)

        # index counter for each step on the sequence
        index = 0

        # current time, after sequence
        current_time = 0

        # checks all steps on the current Tx sequence.
        for field in self.sequence_config['fields']:
            
            # checks all subfields for given sequence step
            for subfield in self.sequence_config[field]['subfields']:
                
                # Get the configurations
                all_config = self.sequence_config[field][subfield]

                # add id for current sequence
                self.decoded_seq['seq'].append(f'{field}.{subfield}')
                
                # add index for current sequence
                self.decoded_seq['seq_idx'].append(index)
                index+=1
                
                # add time for current sequence
                current_time += all_config['duration']
                self.decoded_seq['seq_time'].append(current_time)

                # Add if current subfield is a sync sequence or not.
                self.addToSequence('seq_sync', 'sync', all_config)

                # add next duration to sequence
                self.addToSequence('seq_duration', 'duration', all_config)
                # add next mapping for data
                self.addToSequence('seq_map', 'mapping_index', all_config)
                # add next pilot mapping for data
                self.addToSequence('seq_pilot_map', 'pilots_mapping_index', all_config)
                # add next modulation for such data
                self.addToSequence('seq_mod', 'modulation_index', all_config)
                # add optional methdod to be executed during tx encode
                self.addToSequence('seq_func_tx', 'method_tx', all_config)
                # add optional methdod to be executed during rx decode
                self.addToSequence('seq_func_rx', 'method_rx', all_config)

                # Converts the input information to a stream of bits (stored in bitstream_frames)
                data_stream = self.convertsToBitstream(all_config['data'])
                
                # add next data type for tx
                self.decoded_seq['seq_data_type'].append(all_config['data']['type'][0])
                
                # add next data for tx
                self.decoded_seq['seq_data'].append(data_stream)
                # self.addToSequence('seq_data', 'data', all_config)
        
        ### TODO --- REMOVE!
        # self.input_info = Global.input_info

        return self.decoded_seq
        
    # @sync_track
    # def convertBackSequence(self):
    #     """Decode the burst sequence for Tx. Checks the config for all 'subfields' on each 'field'"""

    #     # Whole burst sequence decoded
    #     self.decoded_seq = defaultdict(list)
    
    @sync_track
    def addToSequence(self, key_target, key_source, from_dict):
        """Add next item to sequence. If not existant, use None."""
        try:
            self.decoded_seq[key_target].append(from_dict[key_source])
        except:
            self.decoded_seq[key_target].append(None)

    @sync_track
    def convertsToBitstream(self, data_to_convert):
        """Converts 'input_info' into a list of bistream (bitstream_frames) for transmission, depending on the number of frames to divide the input info."""
        
        local_dict = {}
        # get data to convert
        self.input_info = data_to_convert

        # for each frame to be sent, check data type, and apply conversion to bitstream
        for idx, in_data in enumerate(self.input_info['data']):
            
            if self.input_info['type'][idx] == 'bin':

                self.bitstream_frames.append(in_data)
            
            elif self.input_info['type'][idx] == 'str':
                
                exec(f'tx_array = BitArray(b"{in_data}").bin', globals(), local_dict)
                
                self.bitstream_frames.append(local_dict["tx_array"])
            
            elif self.input_info['type'][idx] == 'image_raw':
                with open(in_data, "rb") as image:
                    data = image.read()
                    exec(f'tx_array = BitArray({data}).bin', globals(), local_dict)
                    self.bitstream_frames.append(local_dict["tx_array"])
            
            elif self.input_info['type'][idx] == 'text':
                
                with open(in_data, "rb") as text_data:
                    
                    get_text_bytes = text_data.read()
                    
                    exec(f'tx_array = BitArray({get_text_bytes}).bin', globals(), local_dict)
                    
                    self.bitstream_frames.append(local_dict["tx_array"])
                    
            elif self.input_info['type'][idx] == 'image':
                # Set number of bytes to transmit, for each integer in nparray
                self.number_of_bytes = self.input_info['n_bytes'][idx]
                
                # Codify image into bitstream
                bitstream = self.codifyImageForTransmission(in_data)
                # print(len(bitstream))
                self.bitstream_frames.append(bitstream)
                
            else:
                raise ValueError(f"\n\n***Error --> Not supported input_info type: <{self.input_info['type'][idx]}>!\nValid types are <{','.join(Global.supported_input_info)}>\n")

            # TODO -- remove rerturn, or remove 'self' from out variable in that function
            return self.bitstream_frames[-1]
    

    @sync_track
    def BitstreamToMessage(self, tx_data, rx_data, bitstream_type):
        """Converts back the received bistream list (rx_bitstream_frames) after receiving, depending on the number of frames."""
        
        
        local_dict = {}
        
        # frame_count = 0

        # rx_data = self.rx_bitstream_frames
        # tx_data = self.tx_data
        # get rx_data type for that bitstream
        # bitstream_type = 
        
        
        # for rx_data, tx_data in zip(self.rx_bitstream_frames, self.input_info['data']):
            
        # # get rx_data type for that bitstream
        # bitstream_type = self.input_info['type'][frame_count]
        
        if bitstream_type == 'bin':
            
            output_array = rx_data

        elif bitstream_type == 'str':
            
            if len(rx_data) % 8 != 0:
                remainder = len(rx_data) % 8
                rx_data = ['0']*remainder + list(rx_data)
                rx_data = ''.join(rx_data)
            # Convert the stream of bits (as str) into bytes, to recover info.
            exec(f'rx_array = BitArray(bin="{rx_data}").bytes', globals(), local_dict)
            # remove padded zeros, if not removed before.
            # if Global.remove_padded_zeros_at_message:
            
            
            _errors_ = True
            while _errors_:
                
                try:
                    if not Global.remove_padded_zeros:
                        local_dict["rx_array"] = local_dict["rx_array"].decode('utf-8').replace("\x00", "")
                        # local_dict["rx_array"] = local_dict["rx_array"].replace(str.encode("\x00"), str.encode("")).decode('utf-8')
                    else:
                        # if byte_error is not None:
                        #     # local_dict["rx_array"] = local_dict["rx_array"].decode('utf-8')
                        #     # print(byte_error)
                        #     local_dict["rx_array"] = local_dict["rx_array"].replace(str.encode(byte_error), new_byte).decode('utf-8')
                        # else:
                        #     local_dict["rx_array"] = local_dict["rx_array"].decode('utf-8')
                        
                        local_dict["rx_array"] = ''.join([chr(local) for local in local_dict["rx_array"]])
                    
                    _errors_ = False
                except Exception as identifier:
                    raise ValueError(f"\n\n***Error --> Could not convert <{local_dict['rx_array']}> to string @ BitstreamToMessage.\n Error message:\n{identifier}\n")
            
            printDebug(tx_data)
            printDebug(local_dict["rx_array"])
            # asd

            output_array = local_dict["rx_array"]
        
        elif bitstream_type == 'text':
            
            if len(rx_data) % 8 != 0:
                remainder = len(rx_data) % 8
                rx_data = ['0']*remainder + list(rx_data)
                rx_data = ''.join(rx_data)
            # Convert the stream of bits (as str) into bytes, to recover info.
            exec(f'rx_array = BitArray(bin="{rx_data}").bytes', globals(), local_dict)
            # remove padded zeros, if not removed before.
            # if Global.remove_padded_zeros_at_message:
            
            if not Global.remove_padded_zeros:
                local_dict["rx_array"] = local_dict["rx_array"].decode('utf-8').replace("\x00", "")
            else:
                local_dict["rx_array"] = ''.join([chr(local) for local in local_dict["rx_array"]])
            
            # Remove the added line breaks
            local_dict["rx_array"] = local_dict["rx_array"].replace("\n", "")
            
            file_name = tx_data.replace('data','data/out').replace('.txt', '_rx.txt')
            output_array = file_name
            
            with open(file_name, "w") as text_data:
                text_data.write(local_dict["rx_array"])
            
        elif bitstream_type == 'image_raw':
            
            # check if not multiple to 8. Complete with zeros.
            if len(rx_data) % 8 != 0:
                remainder = len(rx_data) % 8
                rx_data = ['0']*remainder + list(rx_data)
                rx_data = ''.join(rx_data)
            exec(f'rx_array = BitArray(bin="{rx_data}").bytes', globals(), local_dict)
            # output_array = rx_array.decode('utf-8')
            output_array = local_dict["rx_array"]
            with open(tx_data.replace('data','data/out').replace('.png', '_rx.png'), "wb") as image:
                image.write(local_dict["rx_array"])
                
        elif bitstream_type == 'image':
            
            # check if not multiple to 8. Complete with zeros.
            if len(rx_data) % 8 != 0:
                remainder = len(rx_data) % 8
                rx_data = ['0']*remainder + list(rx_data)
                rx_data = ''.join(rx_data)
            # Codify bitstream back to image
            image = self.decodifyImageForReceiving(rx_data)
            new_img = tx_data.replace('data','data/out').replace('.png', '_rx.png')
            image.save(new_img)
            # image.show()
            output_array = new_img
            
        else:
            raise ValueError(f"\n\n***Error --> Not supported input_info type: <{bitstream_type}>!\nValid types are <{','.join(Global.supported_input_info)}>\n")
        
        # frame_count += 1

        return output_array
        
    
    @sync_track
    def convertIntegerToBytes(self, integer):
        """Get an integer an convert it to a given number of bytes."""
        
        
        local_dict = {}
        
        exec(f'bit_integer = BitArray(bytes = b"{integer}").bin', globals(), local_dict)
        
        bit_integer = local_dict["bit_integer"]
        
        missing_bits = 8*self.number_of_bytes - len(bit_integer)
        
        bit_integer = ['0']*missing_bits + list(bit_integer)
        
        return ''.join(bit_integer)
    
    @sync_track
    def convertBytesToInteger(self, my_bytes):
        """Get bytes and convert back to integer."""
        
        
        local_dict = {}
        
        # exec(run_cmd, globals(), local_dict)
        # exec(f'got_int = BitArray(bin="{my_bytes}").bytes', globals(), local_dict)
        exec('got_int = BitArray(bin="{val}").bytes'.format(val = my_bytes), globals(), local_dict)
        
        try:
            # if not Global.remove_padded_zeros:
            #     got_int = int(local_dict["got_int"].decode('utf-8').replace("\x00", ""))
            # else:
            #     got_int = int(local_dict["got_int"].decode('utf-8'))
            got_int = int(local_dict["got_int"].decode('utf-8').replace("\x00", ""))
            
        except:
            # got_int = -1
            got_int = None
        
        return got_int
        
        
    @sync_track
    def integerToBytesWrapper(self, k):
        """Wrapper funtion to execute bytes conversion from integer"""
        
        
        
        # get indices
        ch0 = (k - self.chunk_idx)//(self.shape_0*self.shape_1)
        y0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1)//(self.shape_0)
        x0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1 - (y0)*self.shape_0)
        
        # return the bytes
        some_bytes = self.convertIntegerToBytes(self.data_in[x0,y0,ch0])
        
        # return converted bytes
        return some_bytes
        
    @sync_track
    def bytesToIntegerWrapper(self, k):
        """Wrapper funtion to execute integer conversion from bytes back to integer"""
        
        
        # Loop through all points
        # for ch in range(0, self.shape_2):
        #     for y in range(0, self.shape_1):
        #         for x in range(0, self.shape_0):
        
        # Convert bytes chunk back to integer, and add to data nparray
        # k = (self.chunk_idx) + (x) + (y)*self.shape_0 + (ch)*self.shape_0*self.shape_1
        got_integer = self.convertBytesToInteger(self.chunks[k])
        
        if got_integer is None:
            self.bit_error_idx.append(k)
        # if got_integer == -1 and k != 0:
        #     got_integer = self.convertBytesToInteger(self.chunks[k-1])
        # elif got_integer == -1 and k == 0:
        #     got_integer = 0
        
        # get indices
        ch0 = (k - self.chunk_idx)//(self.shape_0*self.shape_1)
        y0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1)//(self.shape_0)
        x0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1 - (y0)*self.shape_0)
        
        # write data to matrix
        self.data[x0,y0,ch0] = got_integer
    
    @sync_track
    def fixImageNoiseWrapper(self, k):
        """Wrapper to fix noise in image."""
        
        
        # get indices
        ch0 = (k - self.chunk_idx)//(self.shape_0*self.shape_1)
        y0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1)//(self.shape_0)
        x0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1 - (y0)*self.shape_0)
        
        # snap
        y0 = self.snapToBoundaries(y0, (0, self.shape_1 - 1))
        x0 = self.snapToBoundaries(x0, (0, self.shape_0 - 1))
                
        # y0 = self.shape_1 - 2 if y0 == self.shape_1 - 1 else y0
        # y0 = 1 if y0 == 0 else y0
        
        # x0 = self.shape_0 - 2 if x0 == self.shape_0 - 1 else x0
        # x0 = 1 if x0 == 0 else x0
        
        # write data to matrix
        self.data[x0,y0,ch0] = int(np.floor(np.mean([self.data[x0,y0+1,ch0], self.data[x0,y0-1,ch0], self.data[x0+1,y0,ch0], self.data[x0-1,y0,ch0]])))
    
    @sync_track
    def codifyImageForTransmission(self, img_path):
        """Get an image, code its values into seriallized bits."""
        
        
        
        # Convert image to numpy array
        image = Image.open(img_path)
        self.data_in = np.asarray(image)
        
        # Get image shape
        shape = self.data_in.shape
        
        # Number of times to store shape
        self.store_shape = 3
        bitstream = ''
        
        self.chunk_idx = 0
        
        # Store shape more than once, to make sure it is reliable
        for j in range(0, self.store_shape):
            for sh in shape:
                bitstream += self.convertIntegerToBytes(sh)
                self.chunk_idx += 1
                
                
        if not Global.multi_theading[0]:
            
            # Loop through all 
            for ch in range(0, shape[2]):
                for y in range(0, shape[1]):
                    for x in range(0, shape[0]):
                        # Convert integer data to bytes, and add to bitstream
                        bitstream += self.convertIntegerToBytes(self.data_in[x,y,ch])
                        
            self.shape_0 = shape[0]
            self.shape_1 = shape[1]
            self.shape_2 = shape[2]
        else:
            
            self.shape_0 = shape[0]
            self.shape_1 = shape[1]
            self.shape_2 = shape[2]
            
            # all indices for decodeification
            index_list = np.arange(self.chunk_idx, self.chunk_idx+self.shape_0*self.shape_1*self.shape_2)
            
            # Runs in multiple threads
            with ThreadPoolExecutor(max_workers = Global.multi_theading[1]) as executor:
                fs = {executor.submit(self.integerToBytesWrapper, k): k for k in index_list}
                # fs = executor.map(self.integerToBytesWrapper, index_list)
                
            # get inverted dictionary, and add to bitstream in order
            inverted_fs = {v : k for k, v in fs.items()}
            
            for key in inverted_fs:
                bitstream += inverted_fs[key].result()
            
        return bitstream
    
    @sync_track
    def decodifyImageForReceiving(self, bitstream):
        """Get seriallized bits and decode back to image."""
        
        
        # slice bitstream into chunks of 8*self.number_of_bytes (ex: 24 bits = 3 bytes)
        self.chunks = re.findall(''.join(['.']*8*self.number_of_bytes), bitstream)
        self.chunk_idx = 0
        
        ############ < COMMENT THIS CHUNK, IF WANTS TO DISABLE EQUALIZATION > ############
        
        self.shape_0, self.shape_1, self.shape_2 = [], [], []
        # For each time the shape was stored, for reliability
        for j in range(0, self.store_shape):
            
            self.shape_0.append(self.convertBytesToInteger(self.chunks[self.chunk_idx]))
            self.chunk_idx += 1
            self.shape_1.append(self.convertBytesToInteger(self.chunks[self.chunk_idx]))
            self.chunk_idx += 1
            self.shape_2.append(self.convertBytesToInteger(self.chunks[self.chunk_idx]))
            self.chunk_idx += 1
        
        # Check if shapes were correctly decoded
        if set([sh for sh in self.shape_0 if sh is not None]) == set() or \
            set([sh for sh in self.shape_1 if sh is not None]) == set() or \
                set([sh for sh in self.shape_2 if sh is not None]) == set():
                    raise ValueError(f"\n\n***Error --> Image shapes not decoded, due to large ammount of errors on transmission.\n")
        
        # Get most frequent value for shape (removing the 'None's)
        self.shape_0 = max(set([sh for sh in self.shape_0 if sh is not None]), key = self.shape_0.count)
        self.shape_1 = max(set([sh for sh in self.shape_1 if sh is not None]), key = self.shape_1.count)
        self.shape_2 = max(set([sh for sh in self.shape_2 if sh is not None]), key = self.shape_2.count)
        
        ############ > COMMENT THIS CHUNK, IF WANTS TO DISABLE EQUALIZATION < ############
        
        # List with all bit errors
        self.bit_error_idx = []
        
        # start output nparray data as zeros
        self.data = np.zeros((self.shape_0, self.shape_1, self.shape_2), dtype = np.uint8)
        
        if not Global.multi_theading[0]:
            
            # Loop through all points
            for ch in range(0, self.shape_2):
                for y in range(0, self.shape_1):
                    for x in range(0, self.shape_0):
                        
                        # Convert bytes chunk back to integer, and add to data nparray
                        k = (self.chunk_idx) + (x) + (y)*self.shape_0 + (ch)*self.shape_0*self.shape_1
                        got_integer = self.convertBytesToInteger(self.chunks[k])
                                
                        if got_integer is None:
                            self.bit_error_idx.append(k)
                            got_integer = -1
                            
                        # write data to matrix
                        self.data[x,y,ch] = got_integer
                        
            for k in self.bit_error_idx:
                
                # get indices
                ch0 = (k - self.chunk_idx)//(self.shape_0*self.shape_1)
                y0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1)//(self.shape_0)
                x0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1 - (y0)*self.shape_0)
                
                # snap
                y0 = self.snapToBoundaries(y0, (0, self.shape_1 - 1))
                x0 = self.snapToBoundaries(x0, (0, self.shape_0 - 1))
                
                # y0 = self.shape_1 - 2 if y0 == self.shape_1 - 1 else y0
                # y0 = 1 if y0 == 0 else y0
                
                # x0 = self.shape_0 - 2 if x0 == self.shape_0 - 1 else x0
                # x0 = 1 if x0 == 0 else x0
                
                # write data to matrix
                self.data[x0,y0,ch0] = int(np.floor(np.mean([self.data[x0,y0+1,ch0], self.data[x0,y0-1,ch0], self.data[x0+1,y0,ch0], self.data[x0-1,y0,ch0]])))
            
        else:
            # all indices for decodeification
            index_list = np.arange(self.chunk_idx, self.chunk_idx+self.shape_0*self.shape_1*self.shape_2)
            
            # Runs in multiple threads
            with ThreadPoolExecutor(max_workers = Global.multi_theading[1]) as executor:
                executor.map(self.bytesToIntegerWrapper, index_list)
            
            # print(self.bit_error_idx)
            # print(len(self.bit_error_idx))
            
            with ThreadPoolExecutor(max_workers = Global.multi_theading[1]) as executor:
                executor.map(self.fixImageNoiseWrapper, self.bit_error_idx)
            
            # with ThreadPoolExecutor(max_workers = Global.multi_theading[1]) as executor:
            #     fs = [executor.submit(self.bytesToIntegerWrapper, idx) for idx in index_list]
        
        # Convert nparray back to image
        image = Image.fromarray(self.data)
        return image
    
    @sync_track
    def snapToBoundaries(self, value, boundaries):
        """Snap values to boundaries."""
        
        (lower_boundary, upper_boundary) = boundaries
        
        value = upper_boundary - 1 if value == upper_boundary else value
        value = lower_boundary + 1 if value == lower_boundary else value
        
        return value
    
    @sync_track
    def compareMessages(self, seq_id, tx_data, rx_data, pretty_diff):
        """Compares the input and received output info."""
        
        if len(tx_data) < 60:
            separators = ''.join(30*['##'])
        else:
            separators = ''.join(int(np.ceil(len(tx_data)/2))*['##'])

        pretty_diff = f"""{separators}
ID for current sequence step: < {seq_id} >
{pretty_diff}

"""

        self.DEBUG = True
        if self.DEBUG:

            print(pretty_diff)
        
            print(f'\nn_bits = {[len(bitstream) for bitstream in tx_data]}\n')
            
            print(f'tx_data = {tx_data}\n')
            
            print(f'rx_data = {rx_data}\n')

        # Write to log file
        with open(Global.log_results, "a") as results:
            results.write(pretty_diff)
    

    @sync_track
    def getInputInfo(self):
        """Returns value of self.input_info"""
        
        return self.input_info

    @sync_track
    def setInputInfo(self, input_info):
        """Set new value for self.input_info"""
        
        self.input_info = input_info

    @sync_track
    def getBitstreamFrames(self):
        """Returns value of self.bitstream_frames"""
        
        return self.bitstream_frames

    @sync_track
    def setBitstreamFrames(self, bitstream_frames):
        """Set new value for self.bitstream_frames"""
        
        self.bitstream_frames = bitstream_frames

    @sync_track
    def getNumberOfFrames(self):
        """Returns value of self.number_of_frames"""
        
        return self.number_of_frames

    @sync_track
    def setNumberOfFrames(self, number_of_frames):
        """Set new value for self.number_of_frames"""
        
        self.number_of_frames = number_of_frames
        
    @sync_track
    def getRxBitstreamFrames(self):
        """Returns value of self.rx_bitstream_frames"""
        
        
        return self.rx_bitstream_frames

    @sync_track
    def setRxBitstreamFrames(self, rx_bitstream_frames):
        """Set new value for self.rx_bitstream_frames"""
        
        
        self.rx_bitstream_frames = rx_bitstream_frames

    @sync_track
    def getOutputInfo(self):
        """Returns value of self.output_info"""
        
        return self.output_info

    @sync_track
    def setOutputInfo(self, output_info):
        """Set new value for self.output_info"""
        
        self.output_info = output_info
    
    @sync_track
    def getDecodedSeq(self):
        """Returns value of self.decoded_seq"""
        
        return self.decoded_seq

    @sync_track
    def setDecodedSeq(self, decoded_seq):
        """Set new value for self.decoded_seq"""
        
        self.decoded_seq = decoded_seq

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj