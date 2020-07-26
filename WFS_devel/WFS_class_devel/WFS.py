import math
import time
import random
import numpy as np
import os
# import sys

import Parameters
import Config

from Quadcell import Quadcell

class WFS(object):
    def __init__(self, ml_dimen, total_of_lenses, n_ml, Wf, dWx, dWy, Xr, Yr, spot_radius, sync_type, original_wf, use_defocus, approx_type):
        """Constructor"""

        # Stores the dimension of a QC (radius or half-lenght) [um]
        self.ml_dimen = Parameters.diameter

        # Total number of microlenses
        self.total_of_lenses = Parameters.quantity

        # Square of the number of lenses.
        self.n_ml = math.sqrt(self.total_of_lenses)

        # Matrix with the average WF values for each qc
        self.Wf = Wf

        # Matrix with the average WF Y slope values for each qc
        self.dWx = dWx

        # Matrix with the average WF Y slope values for each qc
        self.dWy = dWy

        # X cartesian coordinates for each QC.
        self.Xr = Xr

        # Y cartesian coordinates for each QC.
        self.Yr = Yr

        # The effective spot radius [um]
        self.spot_radius = Parameters.eff

        # Sets the type of qc (circular or squared)
        self.sync_type = Config.qc_format

        # Stores the object for original WF
        self.original_wf = 0

        # Flag to use defocus or not
        self.use_defocus = Config.flag_defocus

        # Flag to set what is the pproximation type, for method calc_qc_output_approximation
        self.approx_type = Config.flag_approx_type

        # Rotation angle of QC system (radian)
        self.theta = Config.theta * np.pi / 180

        # Scan-position step
        self.stepp = Config.stepp

        # slope (?)
        self.slope = 0
        
        # yb (?)
        self.yb = 0
    

    def main(self):
        """The main code. Describe all the function of the WFS simulator."""

        # no need
        # # i.read_from_interface()


        if Parameters.with_without == "with" :
            self.flag_Vout_QC = 1
        elif Parameters.with_without == "without" :
            self.flag_Vout_QC = 0

        # self.lamb = Parameters.wave * 1e-6
        
        # if Parameters.defocus == True:
        #     self.flag_defocus = 1
        # else :
        #     self.flag_defocus = 0

        # self.outFileInterface = open("interface.txt")

        if self.flag_Vout_QC == 1:
            self.rodaSpice = 1
            self.flag_Vout_QC = 0

        
        print("@@@@@@@@@@@@@@@@@@@@@ Wavefront Sensor - OptMA Lab 2020 @@@@@@@@@@@@@@@@@@@@@@@@")
        print("Starting execution, please wait. If it takes too long, close it and try again with new settings.")
        
        # self.max_order = Parameters.zernike
        
        # self.tc = time.time()
        # random.seed(self.tc)
        # iseed = [0] * 5000
        # iseed = -random.randint(-2147483,2147483) #(-2147483648‬,21474836487) % 1000

        # nz = [0] * max_order * 4
        # mz = [0] * max_order * 4

        self.set_all_qc_center_coordinates()


        self.calculate_sync_weighting_factor()

        print(f'self.TP = {self.TP}')

        #Cálculo do slope da aproximação linear da resposta da QC.
        self.smooth = 1

        if Config.flag_experimental == 1 :
            slope_exp = 1.85
            self.slope = slope_exp
        else :
            self.slope_QC()

        self.smooth = 0




        #Inicializa variáveis que serão usadas na amostragem e reconstrução da frente de onda.

        
        pass

    def open_all_files_to_write(self):
        """Open all files to be written on the main function."""
        
        pass

    def calculate_w_for_all_qc(self):
        """Calculates the average WF value and average derivative for the region defined by a QC. Writtes to the self.Wf1, self.dWx and self.dWy."""
        pass
    

    def set_all_qc_center_coordinates(self):
        """Calculate the cartesian coordinates for each QC. Stores the return in Xr and Yr [um]"""

        self.Xr = np.zeros([Config.N, Config.N])
        self.Yr = np.zeros([Config.N, Config.N])

        # half the length of the matrix
        self.dimens = (self.n_ml * self.ml_dimen) / 2
        # unit length of a microlens
        self.mlq_dimen = self.dimens * 2 / self.n_ml

        if Config.matriz_ortogonal == 1 :
            for a in range(0, int(self.n_ml), 1):
                for b in range(0, int(self.n_ml), 1):
                    self.Xr[int(a)][int(b)] = (-self.dimens + (self.mlq_dimen / 2)) + a * self.mlq_dimen
                    self.Yr[int(a)][int(b)] = (-self.dimens + (self.mlq_dimen / 2)) + b * self.mlq_dimen
        else:
            
            # with open("Otimizacao\\Graficos\\posicoes.txt", "r") as inFile:
            with open("graphs/positions.csv", "r") as inFile:
                
                if inFile == None :
                    print("Unable to open posicoes.txt")
                    exit(1)

                a = 0
                b = 0
                # read the csv file with first column as X values, and second as Y values
                for cont in range(1, int(self.n_ml * self.n_ml) + 1, 1):
                    varlinhas = inFile.readline()
                    varlinhas = varlinhas.replace("\n", "")
                    varlinhas = varlinhas.split(",")
                    xrr = varlinhas[0]
                    yrr = varlinhas[1]
                    self.Xr[a][b] = int(xrr)
                    self.Yr[a][b] = int(yrr)
                    if b == (int(self.n_ml) - 1) :
                        a += 1
                        b = -1
                    b += 1
 

    def use_defocus(self, input_file):
        """Get all cartesian coordinates for each QC from an input file. Stores the return in Xr and Yr (in um)."""
        pass
    

    def calculate_sync_weighting_factor(self):
        """Calculates the sync weghting factor TP (from sync type)."""

        if Config.flag_experimental == 0 :
            #Calculates the sync weghting factor for each microlens
            self.TP = 0
            for xpp in np.arange(-2,2 + 1.0 / self.stepp, 1.0 / self.stepp):
                for ypp in np.arange(-2,2 + 1.0 / self.stepp, 1.0 / self.stepp):
                    sto = (math.sin((1 / self.spot_radius) * math.sqrt(math.pow(xpp, 2) + math.pow(ypp, 2)))) / ((1 / self.spot_radius) * math.sqrt(math.pow(xpp, 2) + math.pow(ypp, 2)))
                    sto = math.pow(sto, 2)
                    self.TP += sto
    

    def get_coeff_from_file(self, coeff_file):
        """Get the Zernike Coefficients from a file."""
        pass
    

    def create_original_wf(self, rho_norm, delta, coeff, n, m):
        """Instantiates the original WF object."""
        pass
    

    def find_spot_coordinates(self, focal_length, dWx, dWy):
        """Calculates the spot coordinates in um given the focal distance"""
        pass
    

    def change_reference(self, theta, dimens):
        """rotates and/or translates reference"""
        pass
    

    # def only_aberration(self):
    #     """?"""
    #     pass
    

    # def aberration_reconstruction(self):
    #     """?"""
    #     pass
    

    # def calculate_out_values(self):
    #     """?"""
    #     pass
    

    def calibration(self, coeff_file):
        """Calculates the spot position for each microlens given an imput WF coefficient vector"""
        pass
    

    def slope_QC(self):
        """Calculates variables for linear approximation"""
        
        x_edge = 0.23
        NN = 50.0
        self.outx = 0
        intens = 0
        resolucao = 10.00005
        xs = 0
        ccc = 0
        soma1 = 0
        soma2 = 0
        sd1 = 0

        # Creates dummy QC, only to use the getIntensitiy method
        dummy_qc = Quadcell(self.smooth, self.TP, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        ##Cálculo da média
        for xx in np.arange(-x_edge, x_edge + (x_edge / NN), x_edge / NN):
            if x_edge == 0 or NN == 0:
                # print("Calc media", 0.0)
                pass
            else :
                # print("Calc media", round((xx) / (x_edge / NN)))
                pass
            
            dummy_qc.calcAllIntensities(xx, 0)
            intensity_A = dummy_qc.getIntensitiy("A")
            intensity_B = dummy_qc.getIntensitiy("B")
            intensity_C = dummy_qc.getIntensitiy("C")
            intensity_D = dummy_qc.getIntensitiy("D")

            if (intensity_A + intensity_B + intensity_C + intensity_D) == 0 :
                self.outx += 0
            else :
                self.outx += ((intensity_B + intensity_C) - (intensity_A + intensity_D)) / (intensity_A + intensity_B + intensity_C + intensity_D)

            xs += xx
            ccc += 1.0
        if ccc == 0 :
            media = 0
        else :
            media = self.outx / ccc
        if ccc == 0 :
            xs = 0
        else :
            xs /= ccc
        # print(ccc, media, xs)
        self.outx = 0.0
        ##Cálculo do slope
        for xx in np.arange(-x_edge,x_edge + x_edge / NN,x_edge / NN):
            if x_edge == 0 or NN == 0:
                # print("Calc slope", 0.0)
                pass
            else :
                # print("Calc slope",round((xx) / (x_edge / NN)))
                pass
            # Creates dummy QC, only to use the getIntensitiy method
            dummy_qc.calcAllIntensities(xx, 0)
            intensity_A = dummy_qc.getIntensitiy("A")
            intensity_B = dummy_qc.getIntensitiy("B")
            intensity_C = dummy_qc.getIntensitiy("C")
            intensity_D = dummy_qc.getIntensitiy("D")

            if (intensity_A + intensity_B + intensity_C + intensity_D) == 0 :
                self.outx = 0
            else :
                self.outx = ((intensity_B + intensity_C) - (intensity_A + intensity_D)) / (intensity_A + intensity_B + intensity_C + intensity_D)
            intens = self.outx


            soma1 += ((xx - xs) * (intens - media))
            soma2 += math.pow((xx - xs),2)
            if soma2 == 0 :
                b1 = 0
            else :
                
                b1 = soma1 / soma2
            b0 = media - b1 * xs
        # print(b0)
        ##Cálculo do desvio padrão
        for xx in np.arange(-x_edge,x_edge + x_edge / NN,x_edge / NN):
            if x_edge == 0 or NN == 0:
                # print("Calc desvio padrão", 0.0)
                pass
            else :
                # print("Calc desvio padrão",round((xx) / (x_edge / NN)))
                pass

            dummy_qc.calcAllIntensities(xx, 0)
            intensity_A = dummy_qc.getIntensitiy("A")
            intensity_B = dummy_qc.getIntensitiy("B")
            intensity_C = dummy_qc.getIntensitiy("C")
            intensity_D = dummy_qc.getIntensitiy("D")

            if (intensity_A + intensity_B + intensity_C + intensity_D) == 0 :
                self.outx = 0
            else :
                self.outx = ((intensity_B + intensity_C) - (intensity_A + intensity_D)) / (intensity_A + intensity_B + intensity_C + intensity_D)

            sd1 += math.pow((self.outx - (b0 + b1 * xx)),2)
        sd1 /= (ccc - 2)
        sd = math.sqrt(sd1)
        sd /= Parameters.cell
        self.outx = 0.0
        if b1 == 0 :
            R = 0
        else :
            R = sd / b1	
        if R <= resolucao :
            self.slope = b1
            self.yb = b0
        print(R)
        #Fim while
        del dummy_qc
        
        # return ?
    

    def calc_qc_output_approximation(self, approx_type):
        """Calculates the real spot coordinate given outx and outy. Returns dXq and dYq"""
        pass
    

main_execution = WFS(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
main_execution.main()