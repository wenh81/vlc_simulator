import unittest

from WFS import WFS


class TestWFSTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class WFS """
        
        self.WFSObj = WFS(ml_dimen, total_of_lenses, n_ml, Wf, dWx, dWy, Xr, Yr, spot_radius, sync_type, original_wf, use_defocus, approx_type)

        self.ml_dimen = self.WFSObj.ml_dimen
        self.total_of_lenses = self.WFSObj.total_of_lenses
        self.n_ml = self.WFSObj.n_ml
        self.Wf = self.WFSObj.Wf
        self.dWx = self.WFSObj.dWx
        self.dWy = self.WFSObj.dWy
        self.Xr = self.WFSObj.Xr
        self.Yr = self.WFSObj.Yr
        self.spot_radius = self.WFSObj.spot_radius
        self.sync_type = self.WFSObj.sync_type
        self.original_wf = self.WFSObj.original_wf
        self.use_defocus = self.WFSObj.use_defocus
        self.approx_type = self.WFSObj.approx_type
        
        pass


    def test_types(self):
        """ Function to test data types for class WFS """
        
        self.assertIsInstance(self.ml_dimen, float)
        self.assertIsInstance(self.total_of_lenses, int)
        self.assertIsInstance(self.n_ml, float)
        self.assertIsInstance(self.Wf, list)
        self.assertIsInstance(self.dWx, list)
        self.assertIsInstance(self.dWy, list)
        self.assertIsInstance(self.Xr, list)
        self.assertIsInstance(self.Yr, list)
        self.assertIsInstance(self.spot_radius, float)
        self.assertIsInstance(self.sync_type, string)
        self.assertIsInstance(self.original_wf, Wavefront)
        self.assertIsInstance(self.use_defocus, bool)
        self.assertIsInstance(self.approx_type, string)
        
        pass

class TestCalculate_w_for_all_qc(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.calculate_w_for_all_qc() """
        
        
        pass

class TestSet_all_qc_center_coordinates(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.set_all_qc_center_coordinates() """
        
        
        pass

class TestUse_defocus(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.use_defocus() """
        
        
        pass

class TestCalculate_sync_weighting_factor(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.calculate_sync_weighting_factor() """
        
        
        pass

class TestGet_coeff_from_file(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.get_coeff_from_file() """
        
        
        pass

class TestCreate_original_wf(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.create_original_wf() """
        
        
        pass

class TestFind_spot_coordinates(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.find_spot_coordinates() """
        
        
        pass

class TestChange_reference(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.change_reference() """
        
        
        pass

class TestOnly_aberration(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.only_aberration() """
        
        
        pass

class TestAberration_reconstruction(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.aberration_reconstruction() """
        
        
        pass

class TestCalculate_out_values(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.calculate_out_values() """
        
        
        pass

class TestCalibration(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.calibration() """
        
        
        pass

class TestSlope_QC(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.slope_QC() """
        
        
        pass

class TestCalc_qc_output_approximation(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method WFS.calc_qc_output_approximation() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()