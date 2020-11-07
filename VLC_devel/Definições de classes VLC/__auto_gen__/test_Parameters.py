import unittest

from Parameters import Parameters


class TestParametersTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Parameters """
        
        self.ParametersObj = Parameters(with_without, wave, zernike, defocus, quantity, diameter, reflect, cell, space, eff, lin, coefabs, cent, quant, lanode, lcathode, canode, ccathode, ranode, rcathode, reset, integ, capac, bthick, ethick, sres, pres, lreset, wreset, lbuffer, wbuffer, lsel, wsel, charge, vmin, vmax, tran_time_step, noise_noiseless)

        self.with_without = self.ParametersObj.with_without
        self.wave = self.ParametersObj.wave
        self.zernike = self.ParametersObj.zernike
        self.defocus = self.ParametersObj.defocus
        self.quantity = self.ParametersObj.quantity
        self.diameter = self.ParametersObj.diameter
        self.reflect = self.ParametersObj.reflect
        self.cell = self.ParametersObj.cell
        self.space = self.ParametersObj.space
        self.eff = self.ParametersObj.eff
        self.lin = self.ParametersObj.lin
        self.coefabs = self.ParametersObj.coefabs
        self.cent = self.ParametersObj.cent
        self.quant = self.ParametersObj.quant
        self.lanode = self.ParametersObj.lanode
        self.lcathode = self.ParametersObj.lcathode
        self.canode = self.ParametersObj.canode
        self.ccathode = self.ParametersObj.ccathode
        self.ranode = self.ParametersObj.ranode
        self.rcathode = self.ParametersObj.rcathode
        self.reset = self.ParametersObj.reset
        self.integ = self.ParametersObj.integ
        self.capac = self.ParametersObj.capac
        self.bthick = self.ParametersObj.bthick
        self.ethick = self.ParametersObj.ethick
        self.sres = self.ParametersObj.sres
        self.pres = self.ParametersObj.pres
        self.lreset = self.ParametersObj.lreset
        self.wreset = self.ParametersObj.wreset
        self.lbuffer = self.ParametersObj.lbuffer
        self.wbuffer = self.ParametersObj.wbuffer
        self.lsel = self.ParametersObj.lsel
        self.wsel = self.ParametersObj.wsel
        self.charge = self.ParametersObj.charge
        self.vmin = self.ParametersObj.vmin
        self.vmax = self.ParametersObj.vmax
        self.tran_time_step = self.ParametersObj.tran_time_step
        self.noise_noiseless = self.ParametersObj.noise_noiseless
        
        pass


    def test_types(self):
        """ Function to test data types for class Parameters """
        
        self.assertIsInstance(self.with_without, string)
        self.assertIsInstance(self.wave, float)
        self.assertIsInstance(self.zernike, int)
        self.assertIsInstance(self.defocus, int)
        self.assertIsInstance(self.quantity, int)
        self.assertIsInstance(self.diameter, float)
        self.assertIsInstance(self.reflect, float)
        self.assertIsInstance(self.cell, float)
        self.assertIsInstance(self.space, float)
        self.assertIsInstance(self.eff, float)
        self.assertIsInstance(self.lin, float)
        self.assertIsInstance(self.coefabs, float)
        self.assertIsInstance(self.cent, float)
        self.assertIsInstance(self.quant, float)
        self.assertIsInstance(self.lanode, float)
        self.assertIsInstance(self.lcathode, float)
        self.assertIsInstance(self.canode, float)
        self.assertIsInstance(self.ccathode, float)
        self.assertIsInstance(self.ranode, float)
        self.assertIsInstance(self.rcathode, float)
        self.assertIsInstance(self.reset, float)
        self.assertIsInstance(self.integ, float)
        self.assertIsInstance(self.capac, float)
        self.assertIsInstance(self.bthick, float)
        self.assertIsInstance(self.ethick, float)
        self.assertIsInstance(self.sres, float)
        self.assertIsInstance(self.pres, float)
        self.assertIsInstance(self.lreset, float)
        self.assertIsInstance(self.wreset, float)
        self.assertIsInstance(self.lbuffer, float)
        self.assertIsInstance(self.wbuffer, float)
        self.assertIsInstance(self.lsel, float)
        self.assertIsInstance(self.wsel, float)
        self.assertIsInstance(self.charge, float)
        self.assertIsInstance(self.vmin, float)
        self.assertIsInstance(self.vmax, float)
        self.assertIsInstance(self.tran_time_step, float)
        self.assertIsInstance(self.noise_noiseless, string)
        
        pass


if __name__ == '__main__':
    unittest.main()