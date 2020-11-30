from bitstring  import BitArray

import numpy as np

import re

from PIL import Image

import Global

from numba import njit, jit, vectorize

from generalLibrary import timer_dec

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

class Message(object):
    def __init__(self, input_info, n_frames, sync_obj):
        """Constructor of Message."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Message") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Message")
        
        if self.DEBUG:
            print('Running Message...')
        
        # Contains a dict with all the information to be sent, for example, as {"type": "image", "data": [image1, image2]}
        self.input_info = input_info

        # List of bitstream info for transmission. Each position is of type 'bitstream.BitStream'.
        self.bitstream_frames = []

        # Number of frames to be transmitted sequentially.
        self.number_of_frames = n_frames

        # Bitstream list info after receiveing, depending on number of frames.
        self.rx_bitstream_frames = None

        # dict with all recovered received information.
        self.output_info = None
    
        pass
    
    def serialize_boolean_array(self, array):
        """Takes a numpy.array with boolean values and converts it to a space-efficient
        binary representation.
        """
        return np.packbits(array).tobytes()

    def deserialize_boolean_array(self, serialized_array, shape):
        """Inverse of serialize_boolean_array."""
        num_elements = np.prod(shape)
        packed_bits = np.frombuffer(serialized_array, dtype='uint8')
        result = np.unpackbits(packed_bits)[:num_elements]
        result.shape = shape
        return result

    def convertsToBitstream(self):
        """Converts 'input_info' into a list of bistream (bitstream_frames) for transmission, depending on the number of frames to divide the input info."""
        
        self.sync_obj.appendToSimulationPath("convertsToBitstream @ Message")
        
        local_dict = {}
        if self.input_info['type'] == 'str':
            for data in self.input_info['data']:
                exec(f'tx_array = BitArray(b"{data}").bin', globals(), local_dict)
                # print(local_dict["tx_array"])
                self.bitstream_frames.append(local_dict["tx_array"])
                
        elif self.input_info['type'] == 'image_raw':
            for img_path in self.input_info['data']:
                
                with open(img_path, "rb") as image:
                    data = image.read()                    
                    exec(f'tx_array = BitArray({data}).bin', globals(), local_dict)
                    self.bitstream_frames.append(local_dict["tx_array"])
                    
        elif self.input_info['type'] == 'image':
            for img_idx, img_path in enumerate(self.input_info['data']):
                
                # Set number of bytes to transmit, for each integer in nparray
                self.number_of_bytes = self.input_info['n_bytes'][img_idx]
                
                # Codify image into bitstream
                bitstream = self.codifyImageForTransmission(img_path)
                # print(len(bitstream))
                self.bitstream_frames.append(bitstream)
        else:
            raise ValueError(f"\n\n***Error --> Not supported input_info type: <{self.input_info['type']}>!\nValid types are <{','.join(Global.supported_input_info)}>\n")
    

    def BitstreamToMessage(self):
        """Converts back the received bistream list (rx_bitstream_frames) after receiving, depending on the number of frames."""
        
        self.sync_obj.appendToSimulationPath("BitstreamToMessage @ Message")
        
        local_dict = {}
        output_array = []
        if self.input_info['type'] == 'str':
            for frame in self.rx_bitstream_frames:
                # check if not multiple to 8. Complete with zeros.
                if len(frame) % 8 != 0:
                    remainder = len(frame) % 8
                    frame = ['0']*remainder + list(frame)
                    frame = ''.join(frame)
                # Convert the stream of bits (as str) into bytes, to recover info.
                exec(f'rx_array = BitArray(bin="{frame}").bytes', globals(), local_dict)
                # remove padded zeros, if not removed before.
                if Global.remove_padded_zeros_at_message:
                    local_dict["rx_array"] = local_dict["rx_array"].decode('utf-8').replace("\x00", "")
                else:
                    local_dict["rx_array"] = local_dict["rx_array"].decode('utf-8')
                output_array.append(local_dict["rx_array"])
            return output_array
            
        elif self.input_info['type'] == 'image_raw':
            for frame, img_path in zip(self.rx_bitstream_frames, self.input_info['data']):
                # check if not multiple to 8. Complete with zeros.
                if len(frame) % 8 != 0:
                    remainder = len(frame) % 8
                    frame = ['0']*remainder + list(frame)
                    frame = ''.join(frame)
                exec(f'rx_array = BitArray(bin="{frame}").bytes', globals(), local_dict)
                # output_array.append(rx_array.decode('utf-8'))
                output_array.append(local_dict["rx_array"])
                with open(img_path.replace('images','images/out').replace('.png', '_____out.png'), "wb") as image:
                    image.write(local_dict["rx_array"])
            return output_array
        
        elif self.input_info['type'] == 'image':
            for frame, img_path in zip(self.rx_bitstream_frames, self.input_info['data']):
                # check if not multiple to 8. Complete with zeros.
                if len(frame) % 8 != 0:
                    remainder = len(frame) % 8
                    frame = ['0']*remainder + list(frame)
                    frame = ''.join(frame)
                # Codify bitstream back to image
                image = self.decodifyImageForReceiving(frame)
                image.save(img_path.replace('images','images/out').replace('.png', '_____out.png'))
                # image.show()
            return output_array
        else:
            raise ValueError(f"\n\n***Error --> Not supported input_info type: <{self.input_info['type']}>!\nValid types are <{','.join(Global.supported_input_info)}>\n")
        
    
    def convertIntegerToBytes(self, integer):
        """Get an integer an convert it to a given number of bytes."""
        
        # self.sync_obj.appendToSimulationPath("convertIntegerToBytes @ Message")
        
        local_dict = {}
        
        exec(f'bit_integer = BitArray(bytes = b"{integer}").bin', globals(), local_dict)
        
        bit_integer = local_dict["bit_integer"]
        
        missing_bits = 8*self.number_of_bytes - len(bit_integer)
        
        bit_integer = ['0']*missing_bits + list(bit_integer)
        
        return ''.join(bit_integer)
    
    def convertBytesToInteger(self, my_bytes):
        """Get bytes and convert back to integer."""
        
        # self.sync_obj.appendToSimulationPath("convertBytesToInteger @ Message")
        
        local_dict = {}
        
        # exec(run_cmd, globals(), local_dict)
        # exec(f'got_int = BitArray(bin="{my_bytes}").bytes', globals(), local_dict)
        exec('got_int = BitArray(bin="{val}").bytes'.format(val = my_bytes), globals(), local_dict)
        
        try:
            got_int = int(local_dict["got_int"].decode('utf-8').replace("\x00", ""))
        except:
            # got_int = -1
            got_int = None
        
        return got_int
        
        
    def integerToBytesWrapper(self, k):
        """Wrapper funtion to execute bytes conversion from integer"""
        
        # self.sync_obj.appendToSimulationPath("integerToBytesWrapper @ Message")
        
        
        # get indices
        ch0 = (k - self.chunk_idx)//(self.shape_0*self.shape_1)
        y0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1)//(self.shape_0)
        x0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1 - (y0)*self.shape_0)
        
        # return the bytes
        some_bytes = self.convertIntegerToBytes(self.data_in[x0,y0,ch0])
        
        # return converted bytes
        return some_bytes
        
    def bytesToIntegerWrapper(self, k):
        """Wrapper funtion to execute integer conversion from bytes back to integer"""
        
        # self.sync_obj.appendToSimulationPath("bytesToIntegerWrapper @ Message")
        
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
    
    def fixImageNoiseWrapper(self, k):
        """Wrapper to fix noise in image."""
        
        # self.sync_obj.appendToSimulationPath("fixImageNoiseWrapper @ Message")
        
        # get indices
        ch0 = (k - self.chunk_idx)//(self.shape_0*self.shape_1)
        y0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1)//(self.shape_0)
        x0 = (k - self.chunk_idx - (ch0)*self.shape_0*self.shape_1 - (y0)*self.shape_0)
        
        y0 = self.shape_1 - 2 if y0 == self.shape_1 - 1 else y0
        y0 = 1 if y0 == 0 else y0
        
        x0 = self.shape_0 - 2 if x0 == self.shape_0 - 1 else x0
        x0 = 1 if x0 == 0 else x0
        
        # write data to matrix
        self.data[x0,y0,ch0] = int(np.floor(np.mean([self.data[x0,y0+1,ch0], self.data[x0,y0-1,ch0], self.data[x0+1,y0,ch0], self.data[x0-1,y0,ch0]])))
    
    def codifyImageForTransmission(self, img_path):
        """Get an image, code its values into seriallized bits."""
        
        self.sync_obj.appendToSimulationPath("codifyImageForTransmission @ Message")
        
        
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
                
                
        if not Global.multi_theading:
            
            # Loop through all 
            for ch in range(0, shape[2]):
                for y in range(0, shape[1]):
                    for x in range(0, shape[0]):
                        # Convert integer data to bytes, and add to bitstream
                        bitstream += self.convertIntegerToBytes(self.data_in[x,y,ch])
        else:
            
            self.shape_0 = shape[0]
            self.shape_1 = shape[1]
            self.shape_2 = shape[2]
            
            # all indices for decodeification
            index_list = np.arange(self.chunk_idx, self.chunk_idx+self.shape_0*self.shape_1*self.shape_2)
            
            # Runs in multiple threads
            with ThreadPoolExecutor(max_workers = self.shape_2) as executor:
                fs = {executor.submit(self.integerToBytesWrapper, k): k for k in index_list}
                # fs = executor.map(self.integerToBytesWrapper, index_list)
                
            # get inverted dictionary, and add to bitstream in order
            inverted_fs = {v : k for k, v in fs.items()}
            
            for key in inverted_fs:
                bitstream += inverted_fs[key].result()
            
        return bitstream
    
    def decodifyImageForReceiving(self, bitstream):
        """Get seriallized bits and decode back to image."""
        
        self.sync_obj.appendToSimulationPath("decodifyImageForReceiving @ Message")
        
        # slice bitstream into chunks of 8*self.number_of_bytes (ex: 24 bits = 3 bytes)
        self.chunks = re.findall(''.join(['.']*8*self.number_of_bytes), bitstream)
        
        self.shape_0, self.shape_1, self.shape_2 = [], [], []
        self.chunk_idx = 0
        # For each time the shape was stored, for reliability
        for j in range(0, self.store_shape):
            
            self.shape_0.append(self.convertBytesToInteger(self.chunks[self.chunk_idx]))
            self.chunk_idx += 1
            self.shape_1.append(self.convertBytesToInteger(self.chunks[self.chunk_idx]))
            self.chunk_idx += 1
            self.shape_2.append(self.convertBytesToInteger(self.chunks[self.chunk_idx]))
            self.chunk_idx += 1
        
        # Get most frequent value for shape (removing the 'None's)
        self.shape_0 = max(set([sh for sh in self.shape_0 if sh is not None]), key = self.shape_0.count)
        self.shape_1 = max(set([sh for sh in self.shape_1 if sh is not None]), key = self.shape_1.count)
        self.shape_2 = max(set([sh for sh in self.shape_2 if sh is not None]), key = self.shape_2.count)
        
        # List with all bit errors
        self.bit_error_idx = []
        
        # start output nparray data as zeros
        self.data = np.zeros((self.shape_0, self.shape_1, self.shape_2), dtype = np.uint8)
        
        if not Global.multi_theading:
            
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
                
                y0 = self.shape_1 - 2 if y0 == self.shape_1 - 1 else y0
                y0 = 1 if y0 == 0 else y0
                
                x0 = self.shape_0 - 2 if x0 == self.shape_0 - 1 else x0
                x0 = 1 if x0 == 0 else x0
                
                # write data to matrix
                self.data[x0,y0,ch0] = int(np.floor(np.mean([self.data[x0,y0+1,ch0], self.data[x0,y0-1,ch0], self.data[x0+1,y0,ch0], self.data[x0-1,y0,ch0]])))
            
        else:
            # all indices for decodeification
            index_list = np.arange(self.chunk_idx, self.chunk_idx+self.shape_0*self.shape_1*self.shape_2)
            
            # Runs in multiple threads
            with ThreadPoolExecutor(max_workers = self.shape_2) as executor:
                executor.map(self.bytesToIntegerWrapper, index_list)
            
            # print(self.bit_error_idx)
            # print(len(self.bit_error_idx))
            
            with ThreadPoolExecutor(max_workers = self.shape_2) as executor:
                executor.map(self.fixImageNoiseWrapper, self.bit_error_idx)
            
            # with ThreadPoolExecutor(max_workers = self.shape_2) as executor:
            #     fs = [executor.submit(self.bytesToIntegerWrapper, idx) for idx in index_list]
        
        # Convert nparray back to image
        image = Image.fromarray(self.data)
        return image
        
    def compareMessages(self, tx_info, rx_info):
        """Compares the input and received output info."""
        
        self.sync_obj.appendToSimulationPath("compareMessages @ Message")
        
        print(f'\nn_bits = {[len(bitstream) for bitstream in tx_info]}\n')
        
        print(f'tx_info = {tx_info}\n')
        
        print(f'rx_info = {rx_info}\n')
    

    def getInputInfo(self):
        """Returns value of self.input_info"""
        
        return self.input_info

    def setInputInfo(self, input_info):
        """Set new value for self.input_info"""
        
        self.input_info = input_info

    def getBitstreamFrames(self):
        """Returns value of self.bitstream_frames"""
        
        return self.bitstream_frames

    def setBitstreamFrames(self, bitstream_frames):
        """Set new value for self.bitstream_frames"""
        
        self.bitstream_frames = bitstream_frames

    def getNumberOfFrames(self):
        """Returns value of self.number_of_frames"""
        
        return self.number_of_frames

    def setNumberOfFrames(self, number_of_frames):
        """Set new value for self.number_of_frames"""
        
        self.number_of_frames = number_of_frames

    def getRxBitstreamFrames(self):
        """Returns value of self.rx_bitstream_frames"""
        
        self.sync_obj.appendToSimulationPath("getRxBitstreamFrames @ Message")
        
        return self.rx_bitstream_frames

    def setRxBitstreamFrames(self, rx_bitstream_frames):
        """Set new value for self.rx_bitstream_frames"""
        
        self.sync_obj.appendToSimulationPath("setRxBitstreamFrames @ Message")
        
        self.rx_bitstream_frames = rx_bitstream_frames

    def getOutputInfo(self):
        """Returns value of self.output_info"""
        
        return self.output_info

    def setOutputInfo(self, output_info):
        """Set new value for self.output_info"""
        
        self.output_info = output_info
