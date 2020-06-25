class Config(object):
    def __init__(self, rot_flag, nonlin, turb_flag, iseed, print_ctrl, smooth, grava_arquivos, flag_V_QC, matriz_ortogonal, flag_amostragem, flag_experimental, flag_interferencia, flag_linear_resp_QC, flag_sigm_auto_resp_QC, flag_poli_resp_QC, flag_spice, flag_XQC_YQC, flag_Vout_QC, flag_grava_outx_spice, flag_defocus, oxtl_flag, flag_ruido):
        """Constructor"""
        self.rot_flag = 0
        self.nonlin = 0
        self.turb_flag = 0
        self.iseed = []
        self.print_ctrl = 0
        self.smooth = 0
        self.grava_arquivos = 0
        self.flag_V_QC = 0
        self.matriz_ortogonal = 0
        self.flag_amostragem = 0
        self.flag_experimental = 0
        self.flag_interferencia = 0
        self.flag_linear_resp_QC = 0
        self.flag_sigm_auto_resp_QC = 0
        self.flag_poli_resp_QC = 0
        self.flag_spice = 0
        self.flag_XQC_YQC = 0
        self.flag_Vout_QC = 0
        self.flag_grava_outx_spice = 0
        self.flag_defocus = 0
        self.oxtl_flag = 0
        self.flag_ruido = 0
    
        pass
