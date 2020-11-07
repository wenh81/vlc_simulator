import math

import Parameters
import Config

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

        # The effective spot radius (in um)
        self.spot_radius = Parameters.eff

        # Sets the type of qc (circular or squared)
        self.sync_type = Config.qc_format

        # Stores the object for original WF
        self.original_wf = 0

        # Flag to use defocus or not
        self.use_defocus = Config.flag_defocus

        # Flag to set what is the pproximation type, for method calc_qc_output_approximation
        self.approx_type = Config.flag_approx_type
    
        pass

    def calculate_w_for_all_qc(self):
        """Calculates the average WF value and average derivative for the region defined by a QC. Writtes to the self.Wf1, self.dWx and self.dWy."""
        pass
    

    def set_all_qc_center_coordinates(self):
        """Calculate the cartesian coordinates for each QC. Stores the return in Xr and Yr (in um)."""
        pass
    

    def use_defocus(self, input_file):
        """Get all cartesian coordinates for each QC from an input file. Stores the return in Xr and Yr (in um)."""
        pass
    

    def calculate_sync_weighting_factor(self):
        """Calculates the sync weghting factor TP (from sync type)."""
        pass
    

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
    

    def only_aberration(self):
        """?"""
        pass
    

    def aberration_reconstruction(self):
        """?"""
        pass
    

    def calculate_out_values(self):
        """?"""
        pass
    

    def calibration(self, coeff_file):
        """Calculates the spot position for each microlens given an imput WF coefficient vector"""
        pass
    

    def slope_QC(self):
        """Calculates variables for linear approximation"""
        pass
    

    def calc_qc_output_approximation(self, approx_type):
        """Calculates the real spot coordinate given outx and outy. Returns dXq and dYq"""
        pass
    
teste = WFS(0,0,0,0,0,0,0,0,0,0,0,0,0)
print(teste.ml_dimen)