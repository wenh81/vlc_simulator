class Photocell(object):
    def __init__(self, PCq, PC_inner, PCc, area_Ph, G, PCs, QE, QE_inner, radius_inner, coefabs, reflect, Pcref, Dn, Dp, Ln, Lp, Wb, We, Sb):
        """Constructor"""

        # Photocell's total light intensity
        self.PCq = 0

        # Photocell inner region's light intensity
        self.PC_inner = 0

        # Photocell's light intensity
        self.PCc = 0

        # Photocell's effective area
        self.area_Ph = area_Ph

        # Photocell's half gap
        self.G = G

        # Store variable
        self.PCs = PCs

        # Photodiode's quantum efficiency
        self.QE = QE

        # Photocell inner region's quantum efficiency
        self.QE_inner = QE_inner

        # Photocell inner region's radium (um)
        self.radius_inner = radius_inner

        # Photocell's absorption coefficient (cm-1)
        self.coefabs = coefabs

        # Reflectance
        self.reflect = reflect

        # Store variable
        self.Pcref = Pcref

        # 
Diffusion coefficient of electrons in the anode (cm^2/s)
        self.Dn = Dn

        # 
Diffusion coefficient of holes in the cathode (cm^2/s)
        self.Dp = Dp

        # 
Diffusion length of electrons in the anode (cm)
        self.Ln = Ln

        # Diffusion length of holes in the cathode (cm)
        self.Lp = Lp

        # Recombine speed at the cathode surface (cm/s)
        self.Wb = Wb

        # 
Recombine speed at the cathode surface(cm/s)
        self.We = We

        # 
Recombine speed at the anode surface(cm/s)
        self.Sb = Sb
    
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
    
