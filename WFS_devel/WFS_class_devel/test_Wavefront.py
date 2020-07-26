import unittest

from Wavefront import Wavefront


class TestWavefrontTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Wavefront """
        
        self.WavefrontObj = Wavefront(WF, c, W, Wrms, delta, yb, z_basis, coeff, nz, mz, TPS, lamb, f, dXg, dYg, dXqg, dYqg, Xr, Yr, dXq, dYq, outx_cal, outy_cal, dXql, dYql, dWx, dWy, norm_radius, N)

        self.WF = self.WavefrontObj.WF
        self.c = self.WavefrontObj.c
        self.W = self.WavefrontObj.W
        self.Wrms = self.WavefrontObj.Wrms
        self.delta = self.WavefrontObj.delta
        self.yb = self.WavefrontObj.yb
        self.z_basis = self.WavefrontObj.z_basis
        self.coeff = self.WavefrontObj.coeff
        self.nz = self.WavefrontObj.nz
        self.mz = self.WavefrontObj.mz
        self.TPS = self.WavefrontObj.TPS
        self.lamb = self.WavefrontObj.lamb
        self.f = self.WavefrontObj.f
        self.dXg = self.WavefrontObj.dXg
        self.dYg = self.WavefrontObj.dYg
        self.dXqg = self.WavefrontObj.dXqg
        self.dYqg = self.WavefrontObj.dYqg
        self.Xr = self.WavefrontObj.Xr
        self.Yr = self.WavefrontObj.Yr
        self.dXq = self.WavefrontObj.dXq
        self.dYq = self.WavefrontObj.dYq
        self.outx_cal = self.WavefrontObj.outx_cal
        self.outy_cal = self.WavefrontObj.outy_cal
        self.dXql = self.WavefrontObj.dXql
        self.dYql = self.WavefrontObj.dYql
        self.dWx = self.WavefrontObj.dWx
        self.dWy = self.WavefrontObj.dWy
        self.norm_radius = self.WavefrontObj.norm_radius
        self.N = self.WavefrontObj.N
        
        pass


    def test_types(self):
        """ Function to test data types for class Wavefront """
        
        self.assertIsInstance(self.WF, float)
        self.assertIsInstance(self.c, list)
        self.assertIsInstance(self.W, double)
        self.assertIsInstance(self.Wrms, double)
        self.assertIsInstance(self.delta, double)
        self.assertIsInstance(self.yb, double)
        self.assertIsInstance(self.z_basis, double)
        self.assertIsInstance(self.coeff, double)
        self.assertIsInstance(self.nz, int)
        self.assertIsInstance(self.mz, int)
        self.assertIsInstance(self.TPS, float)
        self.assertIsInstance(self.lamb, float)
        self.assertIsInstance(self.f, float)
        self.assertIsInstance(self.dXg, list)
        self.assertIsInstance(self.dYg, list)
        self.assertIsInstance(self.dXqg, list)
        self.assertIsInstance(self.dYqg, list)
        self.assertIsInstance(self.Xr, list)
        self.assertIsInstance(self.Yr, list)
        self.assertIsInstance(self.dXq, list)
        self.assertIsInstance(self.dYq, list)
        self.assertIsInstance(self.outx_cal, list)
        self.assertIsInstance(self.outy_cal, list)
        self.assertIsInstance(self.dXql, list)
        self.assertIsInstance(self.dYql, list)
        self.assertIsInstance(self.dWx, list)
        self.assertIsInstance(self.dWy, list)
        self.assertIsInstance(self.norm_radius, float)
        self.assertIsInstance(self.N, int)
        
        pass

class TestCalculate_w(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Wavefront.calculate_w() """
        
        
        pass

class TestCalculate_slopes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Wavefront.calculate_slopes() """
        
        
        pass

class TestCalculate_zernike(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Wavefront.calculate_zernike() """
        
        
        pass

class TestCalculate_wf(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Wavefront.calculate_wf() """
        
        
        pass

class TestExport_wf_file(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Wavefront.export_wf_file() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()