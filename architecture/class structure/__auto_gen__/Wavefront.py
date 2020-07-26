class Wavefront(object):
    def __init__(self, rho_norm, delta, coeff, n, m):
        """Constructor"""

        # Acumulates the values of W(um) for each point of the WF
        self.WF = 0

        # Zernike coefficients
        self.c = coeff

        # REPETIDO DE RECONSTRUCTION
        self.W = 0

        # REPETIDO DE RECONSTRUCTION
        self.Wrms = 0

        # Delta increment for slope calculation.
        self.delta = delta

        # REPETIDO DE RECONSTRUCTION
        self.yb = 0

        # REPETIDO EM QUADCELL
        self.z_basis = 0

        # REPETIDO EM QUADCELL
        self.coeff = 0

        # REPETIDO EM QUADCELL
        self.nz = 0

        # REPETIDO EM QUADCELL
        self.mz = 0

        # Input optical power to the system(watt)
        self.TPS = 0

        # Light wavelength in meters(m)
        self.lamb = 0

        # Focal distance
        self.f = 0

        # REPETIDO DE RECONSTRUCTION
        self.dXg = 0

        # REPETIDO DE RECONSTRUCTION
        self.dYg = 0

        # REPETIDO DE RECONSTRUCTION
        self.dXqg = 0

        # REPETIDO DE RECONSTRUCTION
        self.dYqg = 0

        # REPETIDO DE RECONSTRUCTION
        self.Xr = 0

        # REPETIDO DE RECONSTRUCTION
        self.Yr = 0

        # REPETIDO DE RECONSTRUCTION
        self.dXq = 0

        # REPETIDO DE RECONSTRUCTION
        self.dYq = 0

        # REPETIDO DE RECONSTRUCTION
        self.outx_cal = 0

        # REPETIDO DE RECONSTRUCTION
        self.outy_cal = 0

        # REPETIDO DE RECONSTRUCTION
        self.dXql = 0

        # REPETIDO DE RECONSTRUCTION
        self.dYql = 0

        # REPETIDO DE RECONSTRUCTION
        self.dWx = 0

        # REPETIDO DE RECONSTRUCTION
        self.dWy = 0

        # Zernike normalization radius
        self.norm_radius = rho_norm

        # Number of points that defines the WF
        self.N = 10
    
        pass

    def calculate_w(self, x, y):
        """Returns the Zernike surface W (in um) for a given cartesian coordinate x and y (in um)."""
        pass
    

    def calculate_slopes(self, x, y):
        """Calculates the dX and dY for a given x and y cartesian coordinates (in um)"""
        pass
    

    def calculate_zernike(self, rho, phi, y, n, m):
        """Calculates the Zernike for a given n,m and polar coordinates rho and phi."""
        pass
    

    def calculate_wf(self):
        """Calculates WF for all points (3.1*N)x(3.1*N) matrix."""
        pass
    

    def export_wf_file(self, file_name):
        """Export the WF matrix to a given file name."""
        pass
    
