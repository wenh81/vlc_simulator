import unittest

from OFDM import OFDM


class TestOFDMTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class OFDM """
        
        self.OFDMObj = OFDM(ofdm_type, mapped_info, pilot_value, n_carriers, n_pilots, n_cp)

        self.ofdm_type = self.OFDMObj.ofdm_type
        self.mapped_info = self.OFDMObj.mapped_info
        self.pilot_value = self.OFDMObj.pilot_value
        self.number_of_carriers = self.OFDMObj.number_of_carriers
        self.number_of_pilots = self.OFDMObj.number_of_pilots
        self.number_of_cyclic_prefix = self.OFDMObj.number_of_cyclic_prefix
        
        pass


    def test_types(self):
        """ Function to test data types for class OFDM """
        
        self.assertIsInstance(self.ofdm_type, str)
        self.assertIsInstance(self.mapped_info, numpy.ndarray)
        self.assertIsInstance(self.pilot_value, complex)
        self.assertIsInstance(self.number_of_carriers, int)
        self.assertIsInstance(self.number_of_pilots, int)
        self.assertIsInstance(self.number_of_cyclic_prefix, int)
        
        pass

class TestApplyModulation(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.applyModulation() """
        
        
        pass

class TestGenerateOFDMSymbol(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.generateOFDMSymbol() """
        
        
        pass

class TestApplyIFFT(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.applyIFFT() """
        
        
        pass

class TestApplyCp(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.applyCp() """
        
        
        pass

class TestRemoveCp(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.removeCp() """
        
        
        pass

class TestApplyIFFT(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.applyIFFT() """
        
        
        pass

class TestEstimateChannel(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.estimateChannel() """
        
        
        pass

class TestEqualize(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.equalize() """
        
        
        pass

class TestGetConstellation(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method OFDM.getConstellation() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()