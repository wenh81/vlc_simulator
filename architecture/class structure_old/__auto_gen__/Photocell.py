class Photocell(object):
    def __init__(self):
        """Constructor"""

        # Photocell's total light intensity
        self.PCq = 0

        # Photocell inner region's light intensity
        self.PC_inner = 0

        # Photocell's light intensity
        self.PCc = 0

        # Photocell's effective area
        self.area_Ph = 0

        # Photocell's half gap
        self.G = 0

        # Store variable
        self.PCs = 0

        # Photodiode's quantum efficiency
        self.QE = 0

        # Photocell inner region's quantum efficiency
        self.QE_inner = 0

        # Photocell inner region's radium (um)
        self.radius_inner = 0

        # Photocell's absorption coefficient (cm-1)
        self.coefabs = 0

        # Reflectance
        self.reflect = 0

        # Store variable
        self.Pcref = 0

        # 
Diffusion coefficient of electrons in the anode (cm^2/s)
        self.Dn = 0

        # 
Diffusion coefficient of holes in the cathode (cm^2/s)
        self.Dp = 0

        # 
Diffusion length of electrons in the anode (cm)
        self.Ln = 0

        # Diffusion length of holes in the cathode (cm)
        self.Lp = 0

        # Recombine speed at the cathode surface (cm/s)
        self.Wb = 0

        # 
Recombine speed at the cathode surface(cm/s)
        self.We = 0

        # 
Recombine speed at the anode surface(cm/s)
        self.Sb = 0
    
        pass

    def calcPhotoCurrent()(self, intensity):
        """Calculates the photocurrent for a given input intensity."""
        pass
    

    def getPhotoCurrent()(self):
        """Returns the photocurrent."""
        pass
    

    def initiAllConfig(self, config):
        """Initial all arguments from config file"""
        pass
    
