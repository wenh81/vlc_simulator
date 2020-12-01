import unittest

from Config import Config


class TestConfigTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Config """
        
        self.ConfigObj = Config(rot_flag, nonlin, turb_flag, iseed, print_ctrl, smooth, grava_arquivos, flag_V_QC, matriz_ortogonal, flag_amostragem, flag_experimental, flag_interferencia, flag_linear_resp_QC, flag_sigm_auto_resp_QC, flag_poli_resp_QC, flag_spice, flag_XQC_YQC, flag_Vout_QC, flag_grava_outx_spice, flag_defocus, oxtl_flag, PI, Kb, hplk, c0, hplk_c0, hplk_c0_e, ele, N)

        self.rot_flag = self.ConfigObj.rot_flag
        self.nonlin = self.ConfigObj.nonlin
        self.turb_flag = self.ConfigObj.turb_flag
        self.iseed = self.ConfigObj.iseed
        self.print_ctrl = self.ConfigObj.print_ctrl
        self.smooth = self.ConfigObj.smooth
        self.grava_arquivos = self.ConfigObj.grava_arquivos
        self.flag_V_QC = self.ConfigObj.flag_V_QC
        self.matriz_ortogonal = self.ConfigObj.matriz_ortogonal
        self.flag_amostragem = self.ConfigObj.flag_amostragem
        self.flag_experimental = self.ConfigObj.flag_experimental
        self.flag_interferencia = self.ConfigObj.flag_interferencia
        self.flag_linear_resp_QC = self.ConfigObj.flag_linear_resp_QC
        self.flag_sigm_auto_resp_QC = self.ConfigObj.flag_sigm_auto_resp_QC
        self.flag_poli_resp_QC = self.ConfigObj.flag_poli_resp_QC
        self.flag_spice = self.ConfigObj.flag_spice
        self.flag_XQC_YQC = self.ConfigObj.flag_XQC_YQC
        self.flag_Vout_QC = self.ConfigObj.flag_Vout_QC
        self.flag_grava_outx_spice = self.ConfigObj.flag_grava_outx_spice
        self.flag_defocus = self.ConfigObj.flag_defocus
        self.oxtl_flag = self.ConfigObj.oxtl_flag
        self.PI = self.ConfigObj.PI
        self.Kb = self.ConfigObj.Kb
        self.hplk = self.ConfigObj.hplk
        self.c0 = self.ConfigObj.c0
        self.hplk_c0 = self.ConfigObj.hplk_c0
        self.hplk_c0_e = self.ConfigObj.hplk_c0_e
        self.ele = self.ConfigObj.ele
        self.N = self.ConfigObj.N
        
        pass


    def test_types(self):
        """ Function to test data types for class Config """
        
        self.assertIsInstance(self.rot_flag, int)
        self.assertIsInstance(self.nonlin, int)
        self.assertIsInstance(self.turb_flag, int)
        self.assertIsInstance(self.iseed, list)
        self.assertIsInstance(self.print_ctrl, int)
        self.assertIsInstance(self.smooth, int)
        self.assertIsInstance(self.grava_arquivos, int)
        self.assertIsInstance(self.flag_V_QC, int)
        self.assertIsInstance(self.matriz_ortogonal, int)
        self.assertIsInstance(self.flag_amostragem, int)
        self.assertIsInstance(self.flag_experimental, int)
        self.assertIsInstance(self.flag_interferencia, int)
        self.assertIsInstance(self.flag_linear_resp_QC, int)
        self.assertIsInstance(self.flag_sigm_auto_resp_QC, int)
        self.assertIsInstance(self.flag_poli_resp_QC, int)
        self.assertIsInstance(self.flag_spice, int)
        self.assertIsInstance(self.flag_XQC_YQC, int)
        self.assertIsInstance(self.flag_Vout_QC, int)
        self.assertIsInstance(self.flag_grava_outx_spice, int)
        self.assertIsInstance(self.flag_defocus, int)
        self.assertIsInstance(self.oxtl_flag, int)
        self.assertIsInstance(self.PI, int)
        self.assertIsInstance(self.Kb, int)
        self.assertIsInstance(self.hplk, int)
        self.assertIsInstance(self.c0, int)
        self.assertIsInstance(self.hplk_c0, int)
        self.assertIsInstance(self.hplk_c0_e, int)
        self.assertIsInstance(self.ele, int)
        self.assertIsInstance(self.N, int)
        
        pass


if __name__ == '__main__':
    unittest.main()