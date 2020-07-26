import unittest

from Reconstruction import Reconstruction


class TestReconstructionTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Reconstruction """
        
        self.ReconstructionObj = Reconstruction(c, dX, dY, dXg, dYg, dXqg, dYqg, Xr, Yr, dXq, dYq, outx_cal, outy_cal, dXql, dYql, dWx, dWy, Wf1, W, Wrms, delta, yb, x_edge, z_basis, coeff, nz, mz, nn, a, b, a1, b1, theta, jx, jy, na, ma, xx, outx_l)

        self.c = self.ReconstructionObj.c
        self.dX = self.ReconstructionObj.dX
        self.dY = self.ReconstructionObj.dY
        self.dXg = self.ReconstructionObj.dXg
        self.dYg = self.ReconstructionObj.dYg
        self.dXqg = self.ReconstructionObj.dXqg
        self.dYqg = self.ReconstructionObj.dYqg
        self.Xr = self.ReconstructionObj.Xr
        self.Yr = self.ReconstructionObj.Yr
        self.dXq = self.ReconstructionObj.dXq
        self.dYq = self.ReconstructionObj.dYq
        self.outx_cal = self.ReconstructionObj.outx_cal
        self.outy_cal = self.ReconstructionObj.outy_cal
        self.dXql = self.ReconstructionObj.dXql
        self.dYql = self.ReconstructionObj.dYql
        self.dWx = self.ReconstructionObj.dWx
        self.dWy = self.ReconstructionObj.dWy
        self.Wf1 = self.ReconstructionObj.Wf1
        self.W = self.ReconstructionObj.W
        self.Wrms = self.ReconstructionObj.Wrms
        self.delta = self.ReconstructionObj.delta
        self.yb = self.ReconstructionObj.yb
        self.x_edge = self.ReconstructionObj.x_edge
        self.z_basis = self.ReconstructionObj.z_basis
        self.coeff = self.ReconstructionObj.coeff
        self.nz = self.ReconstructionObj.nz
        self.mz = self.ReconstructionObj.mz
        self.nn = self.ReconstructionObj.nn
        self.a = self.ReconstructionObj.a
        self.b = self.ReconstructionObj.b
        self.a1 = self.ReconstructionObj.a1
        self.b1 = self.ReconstructionObj.b1
        self.theta = self.ReconstructionObj.theta
        self.jx = self.ReconstructionObj.jx
        self.jy = self.ReconstructionObj.jy
        self.na = self.ReconstructionObj.na
        self.ma = self.ReconstructionObj.ma
        self.xx = self.ReconstructionObj.xx
        self.outx_l = self.ReconstructionObj.outx_l
        
        pass


    def test_types(self):
        """ Function to test data types for class Reconstruction """
        
        self.assertIsInstance(self.c, list)
        self.assertIsInstance(self.dX, list)
        self.assertIsInstance(self.dY, list)
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
        self.assertIsInstance(self.Wf1, list)
        self.assertIsInstance(self.W, float)
        self.assertIsInstance(self.Wrms, float)
        self.assertIsInstance(self.delta, float)
        self.assertIsInstance(self.yb, float)
        self.assertIsInstance(self.x_edge, float)
        self.assertIsInstance(self.z_basis, float)
        self.assertIsInstance(self.coeff, float)
        self.assertIsInstance(self.nz, int)
        self.assertIsInstance(self.mz, int)
        self.assertIsInstance(self.nn, int)
        self.assertIsInstance(self.a, int)
        self.assertIsInstance(self.b, int)
        self.assertIsInstance(self.a1, int)
        self.assertIsInstance(self.b1, int)
        self.assertIsInstance(self.theta, float)
        self.assertIsInstance(self.jx, float)
        self.assertIsInstance(self.jy, float)
        self.assertIsInstance(self.na, int)
        self.assertIsInstance(self.ma, int)
        self.assertIsInstance(self.xx, float)
        self.assertIsInstance(self.outx_l, float)
        
        pass

class TestGetZernike_term(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Reconstruction.getZernike_term() """
        
        
        pass

class TestSimq(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Reconstruction.simq() """
        
        
        pass

class TestBasis(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Reconstruction.basis() """
        
        
        pass

class TestDecomp(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Reconstruction.decomp() """
        
        
        pass

class TestReconst(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Reconstruction.reconst() """
        
        
        pass

class TestCalc_RMS(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Reconstruction.calc_RMS() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()