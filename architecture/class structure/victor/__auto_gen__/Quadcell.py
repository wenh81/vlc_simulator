import Config
import Parameters


class Quadcell(object):
    def __init__(self, jx, jy, smooth, nn, theta, na, ma, xx, outx_l, outx, outy, cell_qc, slope, slope_exp, x_edge, qc_type, has_microlens, A_intensity, B_intensity, C_intensity, D_intensity):
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

        # QC's dimension (edge for square-QC and diameter for circular QC) (um)
        self.cell_qc = cell_qc

        # Scan-position step
        self.stepp = Config.stepp
        
        # QC's format: 1 for square, 0 for circular
        self.qc_format = Config.qc_format

        # The effective spot radius [um]
        self.spot_radius = Parameters.eff
        
        # QC's inner radius [um]
        self.radius_inner = Parameters.cent

        # Radius or edge of QC [um]
        self.cell_qc = Parameters.cell
        
        # QC's material quantum efficience
        self.QE = Parameters.quant
        
        # QC's material quantum efficience of inner radius
        self.QE_inner = Parameters.quant_inner

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
    
        pass

    def calcAllIntensities(self, xc, yc):
        """Calculates the intensity for each photocell over a given qc spot coordinate (jx, jy)"""
        pass
    

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
    
