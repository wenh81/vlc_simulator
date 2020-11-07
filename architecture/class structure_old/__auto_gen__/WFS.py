import Parameters

class WFS(object):
    def __init__(self, n_ml):
        """Constructor"""

        # Stores the dimension of a QC (radius or half-lenght)
        self.ml_dimen = Parameters.diameter

        # Total number of microlenses
        self.total_of_lenses = Parameters.quantity

        # Square of the number of lenses.
        self.n_ml = math.sqrt(self.total_of_lenses)

        # Matrix with the average WF values for each qc
        self.Wf1[ = np.zeros(n_ml, n_ml)

        # Matrix with the average WF Y slope values for each qc
        self.dWx[n_ml][n_ml] = 0

        # Matrix with the average WF Y slope values for each qc
        self.dWy[n_ml][n_ml] = 0

        # X cartesian coordinates for each QC.
        self.Xr[n_ml][n_ml] = 0

        # Y cartesian coordinates for each QC.
        self.Yr[n_ml][n_ml] = 0

        # The effective spot radius (in um)
        self.spot_radius = Parameters.eff

        # Sets the type of qc (circular or squared)
        self.sync_type = Flags.qc_format

        # Stores the object for original WF
        self.original_wf = None

        # Flag to use defocus or not
        self.use_defocus = Flags.flag_defocus

        # Flag to set what is the pproximation type, for method calc_qc_output_approximation
        self.approx_type = Flags.flag_approx_type
    
        pass

    def main(self):
        """Describe all the function of the WFS simulator"""

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

        outFileInterface = open("interface.txt")

        

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
    


main_execution = WFS()

main_execution.main()