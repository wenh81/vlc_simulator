import unittest

from Reconstruction import Reconstruction


class TestReconstructionTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Reconstruction """
        
        self.ReconstructionObj = Reconstruction(c, dX, dY, dXg, dYg, dXqg, dYqg, Xr, Yr, dXq, dYq, outx_cal, outy_cal, dXql, dYql, dWx, dWy, Wf1, W, Wrms, delta, yb, x_edge, z_basis, coeff, nz, mz, nn, a, b, a1, b1, theta, jx, jy, ma, xx, outx_l)

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
        self.ma = self.ReconstructionObj.ma
        self.xx = self.ReconstructionObj.xx
        self.outx_l = self.ReconstructionObj.outx_l
        
        pass


    def test_types(self):
        """ Function to test data types for class Reconstruction """
        
        self.assertIsInstance(self.c, int)
        self.assertIsInstance(self.dX, int)
        self.assertIsInstance(self.dY, int)
        self.assertIsInstance(self.dXg, int)
        self.assertIsInstance(self.dYg, int)
        self.assertIsInstance(self.dXqg, int)
        self.assertIsInstance(self.dYqg, int)
        self.assertIsInstance(self.Xr, int)
        self.assertIsInstance(self.Yr, int)
        self.assertIsInstance(self.dXq, int)
        self.assertIsInstance(self.dYq, int)
        self.assertIsInstance(self.outx_cal, int)
        self.assertIsInstance(self.outy_cal, int)
        self.assertIsInstance(self.dXql, int)
        self.assertIsInstance(self.dYql, int)
        self.assertIsInstance(self.dWx, int)
        self.assertIsInstance(self.dWy, int)
        self.assertIsInstance(self.Wf1, int)
        self.assertIsInstance(self.W, int)
        self.assertIsInstance(self.Wrms, int)
        self.assertIsInstance(self.delta, int)
        self.assertIsInstance(self.yb, int)
        self.assertIsInstance(self.x_edge, int)
        self.assertIsInstance(self.z_basis, int)
        self.assertIsInstance(self.coeff, int)
        self.assertIsInstance(self.nz, int)
        self.assertIsInstance(self.mz, int)
        self.assertIsInstance(self.nn, int)
        self.assertIsInstance(self.a, int)
        self.assertIsInstance(self.b, int)
        self.assertIsInstance(self.a1, int)
        self.assertIsInstance(self.b1, int)
        self.assertIsInstance(self.theta, int)
        self.assertIsInstance(self.jx, int)
        self.assertIsInstance(self.jy, int)
        self.assertIsInstance(self.ma, int)
        self.assertIsInstance(self.xx, int)
        self.assertIsInstance(self.outx_l, int)
        
        pass


if __name__ == '__main__':
    unittest.main()