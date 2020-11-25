from bitstring  import BitArray

import numpy as np

from PIL import Image

import Global

class Message(object):
    def __init__(self, input_info, n_frames, sync_obj):
        """Constructor of Message."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug()
        
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
                self.bitstream_frames.append(local_dict["tx_array"])
        elif self.input_info['type'] == 'image':
            for img_path in self.input_info['data']:
                
                # image = Image.open(img_path)
                # data = np.asarray(image)
                # import pickle
                # serialized = pickle.dumps(data, protocol=0) # protocol 0 is printable ASCII
                # print(serialized)
                # deserialized_a = pickle.loads(serialized)
                
                with open(img_path, "rb") as image:
                    data = image.read()                    
                    exec(f'tx_array = BitArray({data}).bin', globals(), local_dict)
                    self.bitstream_frames.append(local_dict["tx_array"])
        else:
            raise ValueError(f"\n\n***Error --> Not supported input_info type: <{self.input_info['type']}>!\nValid types are <{','.join(Global.supported_input_info)}>\n")
    

    def BitstreamToMessage(self, rx_bitstream_frames):
        """Converts back the received bistream list (rx_bitstream_frames) after receiving, depending on the number of frames."""
        
        self.sync_obj.appendToSimulationPath("BitstreamToMessage @ Message")
        
        output_array = []
        if self.input_info['type'] == 'str':
            for frame in rx_bitstream_frames:
                # Convert the stream of bits (as str) into bytes, to recover info.
                exec(f'rx_array = BitArray(bin="{frame}").bytes', globals())
                output_array.append(rx_array.decode('utf-8'))
            return output_array
            
        elif self.input_info['type'] == 'image':
            for frame, img_path in zip(rx_bitstream_frames, self.input_info['data']):
                exec(f'rx_array = BitArray(bin="{frame}").bytes', globals())
                # output_array.append(rx_array.decode('utf-8'))
                output_array.append(rx_array)
                # image2 = Image.fromarray(data)
                # image2.show()
                with open(img_path.replace('.png', '_____out.png'), "wb") as image:
                    image.write(rx_array)
            return output_array
        else:
            raise ValueError(f"\n\n***Error --> Not supported input_info type: <{self.input_info['type']}>!\nValid types are <{','.join(Global.supported_input_info)}>\n")
        
    

    def compareMessages(self):
        """Compares the input and received output info."""
        pass
    

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
        
        return self.rx_bitstream_frames

    def setRxBitstreamFrames(self, rx_bitstream_frames):
        """Set new value for self.rx_bitstream_frames"""
        
        self.rx_bitstream_frames = rx_bitstream_frames

    def getOutputInfo(self):
        """Returns value of self.output_info"""
        
        return self.output_info

    def setOutputInfo(self, output_info):
        """Set new value for self.output_info"""
        
        self.output_info = output_info
