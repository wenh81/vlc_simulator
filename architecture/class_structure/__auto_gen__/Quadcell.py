class Quadcell(object):
    def __init__(self, nn, theta, jx, jy, na, ma, xx, outx_l, outx, outy, cell_qc, stepp, slope, slope_ex, x_edge, qc_type, has_microlens, A_intensity, B_intensity, C_intensity, D_intensity):
        """Constructor"""

        # Number of integrations points inside the QC
        self.nn = nn

        # Rotation angle of QC system (degree)
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
        self.stepp = 20

        # QC anwser linear aproximation's slope
        self.slope = 0

        # Experimental QC anwser linear aproximation's slope
        self.slope_ex = slope_ex

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
    
        pass

    def calcAllIntensities(self):
        """Calculates the intensity for each photocell over a given qc spot coordinate."""
        pass
    

    def getIntensitiy(self, which_photocell):
        """Return the intensity values for a given photocell."""
        pass
    

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
    
