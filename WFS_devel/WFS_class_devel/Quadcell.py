import Config
import Parameters

import numpy as np
import math


class Quadcell(object):
    def __init__(self, smooth, TP, jx, jy, nn, theta, na, ma, xx, outx_l, outx, outy, slope, slope_exp, x_edge, qc_type, has_microlens, A_intensity, B_intensity, C_intensity, D_intensity):
        """Constructor"""

        # Number of integrations points inside the QC
        self.nn = nn

        # Rotation angle of QC system (radian)
        self.theta = theta

        # X position of QC in realation to the microlens coord. system
        self.jx = jx

        # Y position of QC in realation to the microlens coord. system
        self.jy = jy

        # n in realation to the microlens coord. system
        self.na = na

        # m in realation to the microlens coord. system
        self.ma = ma

        # 0.
        self.xx = xx

        # 0.
        self.outx_l = outx_l

        # The calculated X spot coordinate.
        self.outx = outx

        # The calculated Y spot coordinate.
        self.outy = outy

        # Scan-position step
        self.stepp = Config.stepp
        
        # QC's format: 1 for square, 0 for circular
        self.qc_format = Config.qc_format

        # The effective spot radius [um]
        self.spot_radius = Parameters.eff
        
        # QC's inner radius [um]
        self.radius_inner = Parameters.cent

        # QC's dimension (edge for square-QC and diameter for circular QC) [um]
        self.cell_qc = Parameters.cell
        
        # QC's material quantum efficience
        self.QE = Parameters.quant
        
        # QC's material quantum efficience of inner radius
        self.QE_inner = Parameters.quant_inner
        
        # G ??...
        self.G = Config.G

        # QC anwser linear aproximation's slope
        self.slope = 0

        # Experimental QC anwser linear aproximation's slope
        self.slope_exp = slope_exp

        # Can assume values between 0 and 1, 0 means QC-center, 1 means QC edge
        self.x_edge = x_edge

        # Defines the QC format.
        self.qc_type = qc_type

        # Defines if has microlens on the focal plane.
        self.has_microlens = has_microlens

        # Defines the intensity for photocell A
        self.A_intensity = 0

        # Defines the intensity for photocell B
        self.B_intensity = 0

        # Defines the intensity for photocell C
        self.C_intensity = 0

        # Defines the intensity for photocell D
        self.D_intensity = 0
        
        # If 1, calculates the slope for linear approximation
        self.smooth = smooth

        # Sync weghting factor for each microlens
        self.TP = TP

        # Square of the number of lenses.
        self.n_ml = math.sqrt(Parameters.quantity)

        # Wavelenght in [um]
        self.lamb = Parameters.wave * 1e-6
    
        pass

    def calcAllIntensities(self, xc, yc):
        """Calculates the intensity for each photocell over a given qc spot coordinate (jx, jy)"""

        tp = 0.0
        ix = 0
        iy = 0
        h = 0
        ints = np.zeros([5, 5])
        ints_inner = np.zeros([5, 5])
        # ints = [[0.0] * 5] * 5
        # ints_inner = [[0.0] * 5] * 5
        x = 0.0
        y = 0.0
        xc1 = 0.0
        yc1 = 0.0
        xc1 = xc
        yc1 = yc
        
        for h in np.arange(1,5,1):
            for k in np.arange(1,5,1):
                ints[h][k] = 0.0
                ints_inner[h][k] = 0.0

        for k in np.arange(0, 2, 1):
            for h in np.arange(0, 2, 1):
                for ix in np.arange(0, self.stepp + 1, 1):
                    for iy in np.arange(0, self.stepp + 1, 1):
                        #print(k, h, ix, iy)
                        if self.qc_format == 0 :
                            x = -(1 + self.G) + h * (1 + 2 * self.G) + (ix * (1.0 / self.stepp))
                            y = -(1 + self.G) + k * (1 + 2 * self.G) + (iy * (1.0 / self.stepp))
                            if self.spot_radius == 0 or math.sqrt(math.pow((x - xc1),2) + math.pow((y - yc1),2)) == 0 :
                                tp = 0.0
                            else :
                                tp = (math.sin((1 / self.spot_radius) * math.sqrt(math.pow((x - xc1),2) + math.pow((y - yc1),2)))) / ((1 / self.spot_radius) * math.sqrt(math.pow((x - xc1),2) + math.pow((y - yc1),2)))
                            tp = math.pow(tp,2)
                            #print(tp)
                        elif self.qc_format == 1 :
                            x = -1 + h + (ix * (1 / self.stepp))
                            y = -1 + k + (iy * (1 / self.stepp))
                            ints[h + 1][k + 1] +=  math.pow(math.exp((math.pow((x - xc1),2) + math.pow((y - yc1),2) ) / math.pow(self.spot_radius,2)), -1)
                            if (self.spot_radius * self.spot_radius) == 0 or ((x - xc1) * (y - yc1) * np.pi * np.pi) == 0 :
                                tp = 0.0
                            else :
                                tp = (math.sin((x - xc1) * np.pi / self.spot_radius) * math.sin((y - yc1) * np.pi / self.spot_radius)) / (((x - xc1) * (y - yc1) * np.pi * np.pi) / (self.spot_radius * self.spot_radius))

                        if (math.pow(x,2) + math.pow(y,2)) <= math.pow(self.radius_inner,2):
                            ints_inner[h + 1][k + 1] += tp
                        else :
                            if self.qc_format == 1 :
                                if (math.pow(x,2) + math.pow(y,2)) <= math.pow(self.cell_qc, 2):
                                    ints[h + 1][k + 1] += tp
                            if (math.pow(x,2) + math.pow(y,2)) <= 1 :
                                #print(math.pow(x,2) + math.pow(y,2))
                                ints[h + 1][k + 1] += tp
                                # print(ints[h + 1][k + 1])						
                        tp = 0.0

        # print(ints)

        Aq = 0.0
        Bq = 0.0
        Cq = 0.0
        Dq = 0.0
        Ac_inner = 0.0
        Bc_inner = 0.0
        Cc_inner = 0.0
        Dc_inner = 0.0
        Ac = 0.0
        Bc = 0.0
        Cc = 0.0
        Dc = 0.0
        Ac = ints[1][2]
        Bc = ints[2][2]
        Cc = ints[2][1]
        Dc = ints[1][1]

        Ac_inner = ints_inner[1][2]
        Bc_inner = ints_inner[2][2]
        Cc_inner = ints_inner[2][1]
        Dc_inner = ints_inner[1][1]
        Ac *= self.QE
        Bc *= self.QE
        Cc *= self.QE
        Dc *= self.QE

        Ac_inner *= self.QE_inner
        Bc_inner *= self.QE_inner
        Cc_inner *= self.QE_inner
        Dc_inner *= self.QE_inner
        Ac += Ac_inner
        Bc += Bc_inner
        Cc += Cc_inner
        Dc += Dc_inner

        Aq = Ac
        Bq = Bc
        Cq = Cc
        Dq = Dc

        #tp/TP = cotribution percentage of the spot with respect to max (spot center)
        if self.smooth == 0 :
            if (Config.hplk_c0_e * self.TP) == 0 :
                cnst = 0
            else :
                cnst = ((Parameters.TPS / (self.n_ml * self.n_ml)) * self.lamb) / (Config.hplk_c0_e * self.TP) #Número de fótons efeticos
            if Config.flag_spice == 1 :
                Ac *= Parameters.TPS / (self.n_ml * self.n_ml * self.TP) #W
                Bc *= Parameters.TPS / (self.n_ml * self.n_ml * self.TP)
                Cc *= Parameters.TPS / (self.n_ml * self.n_ml * self.TP)
                Dc *= Parameters.TPS / (self.n_ml * self.n_ml * self.TP)
                Ac *= 1 / (math.pow(self.cell_qc * 1e-6,2)) #W/(m^2)
                Bc *= 1 / (math.pow(self.cell_qc * 1e-6,2))
                Cc *= 1 / (math.pow(self.cell_qc * 1e-6,2))
                Dc *= 1 / (math.pow(self.cell_qc * 1e-6,2))
                #Ac *= 1 / (self.lamb * 1e6); #Adequação da irradiância para a unidade W/m2micm conforme necessário no SPICE
                #Bc *= 1 / (self.lamb * 1e6);
                #Cc *= 1 / (self.lamb * 1e6);
                #Dc *= 1 / (self.lamb * 1e6);
                
                ############################## DOUBLE CHECK ##############################
                # self.grava_arquivos = 1
                # self.flag_V_QC = 0
                # grava_le_arquivos(0) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # self.flag_V_QC = 1
                # self.grava_arquivos = 0
                ############################## DOUBLE CHECK ##############################
                Aq *= cnst * 1e9
                Bq *= cnst * 1e9
                Cq *= cnst * 1e9
                Dq *= cnst * 1e9
            else :
                Aq *= cnst * 1e9
                Bq *= cnst * 1e9
                Cq *= cnst * 1e9
                Dq *= cnst * 1e9

        # 'returns' all the intensities
        self.A_intensity = Aq
        self.B_intensity = Bq
        self.C_intensity = Cq
        self.D_intensity = Dq



    def getIntensitiy(self, which_photocell):
        """Return the intensity values for a given photocell (A, B, C or D)"""
        if which_photocell == "A":
            return self.A_intensity
        elif which_photocell == "B":
            return self.B_intensity
        elif which_photocell == "C":
            return self.C_intensity
        elif which_photocell == "D":
            return self.D_intensity
        else:
            exit(f"Wrong photocell ID given: <<{which_photocell}>>. Only (A, B, C or D) allowed")
        
    

    def getPhotoCurrent(self, which_photocell):
        """Return the photocurrent values for a given photocell."""
        pass
    

    def calcAllPhotoCurrents(self):
        """Calculates the photocurrent for each photocell over a given qc spot coordinate."""
        pass
    

    def calcSpotCoordinates(self, A, B, C, D):
        """Calculates the spot coordinates from a list of photocell values. Stores the values on outx and outy."""
        pass
    

    def getOutX(self):
        """Returns the X coordinate outx"""
        pass
    

    def getOutY(self):
        """Returns the Y coordinate outx"""
        pass
    
