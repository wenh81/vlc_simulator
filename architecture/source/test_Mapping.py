import unittest

from Mapping import Mapping


class TestMappingTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Mapping """
        
        self.MappingObj = Mapping(bitstream_frames, mapping_type, bits_per_symbol)

        self.bitstream_frames = self.MappingObj.bitstream_frames
        self.bits_per_symbol = self.MappingObj.bits_per_symbol
        self.frame_size = self.MappingObj.frame_size
        self.mapped_info = self.MappingObj.mapped_info
        self.mapping_type = self.MappingObj.mapping_type
        self.rx_bitstream_frames = self.MappingObj.rx_bitstream_frames
        
        pass


    def test_types(self):
        """ Function to test data types for class Mapping """
        
        self.assertIsInstance(self.bitstream_frames, list)
        self.assertIsInstance(self.bits_per_symbol, int)
        self.assertIsInstance(self.frame_size, numpy.ndarray)
        self.assertIsInstance(self.mapped_info, str)
        self.assertIsInstance(self.mapping_type, str)
        self.assertIsInstance(self.rx_bitstream_frames, list)
        
        pass

class TestSerialToParallel(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Mapping.serialToParallel() """
        
        
        pass

class TestApplyMapping(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Mapping.applyMapping() """
        
        
        pass

class TestApplyDemapping(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Mapping.applyDemapping() """
        
        
        pass

class TestParallelToserial(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Mapping.ParallelToserial() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()