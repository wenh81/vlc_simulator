class Wavefront(object):
    def __init__(self, WF, c, W, Wrms, delta, yb, z_basis, coeff, nz, mz, TPS, lamb, f, dXg, dYg, dXqg, dYqg, Xr, Yr, dXq, dYq, outx_cal, outy_cal, dXql, dYql, dWx, dWy, norm_radius, N):
        """Constructor"""

        # Acumulates the values of W(um) for each point of the WF
        self.WF = WF

        # Zernike coefficients
        self.c = coeff

        # WF local value(ALSO ON RECONSTRUCTION)
        self.W = W

        # RMS error between input and output WF(ALSO ON RECONSTRUCTION)
        self.Wrms = Wrms

        # Delta increment for slope calculation.
        self.delta = delta

        # 0.(ALSO ON RECONSTRUCTION)
        self.yb = 0

        # basis formed by zernikes at each spot(ALSO ON QUADCELL)
        self.z_basis = z_basis

        # calculated coefficients to zernike polynomials(ALSO ON QUADCELL)
        self.coeff = coeff

        # zernike n indice for each zernike term(ALSO ON QUADCELL)
        self.nz = nz

        # zernike m indice for each zernike term(ALSO ON QUADCELL)
        self.mz = mz

        # Input optical power to the system(watt)
        self.TPS = 0

        # Light wavelength in meters(m)
        self.lamb = 0

        # Focal distance
        self.f = 0

        # "real" dX in realtion to ML system center(ALSO ON RECONSTRUCTION)
        self.dXg = dXg

        # "real" dY in realtion to ML system center(ALSO ON RECONSTRUCTION)
        self.dYg = dYg

        # "real" dX in relation to QC system center(ALSO ON RECONSTRUCTION)
        self.dXqg = dXqg

        # "real" dY in relation to QC system center(ALSO ON RECONSTRUCTION)
        self.dYqg = dYqg

        # x coordinate of center of microlen(ALSO ON RECONSTRUCTION)
        self.Xr = Xr

        # y coordinate of center of microlen(ALSO ON RECONSTRUCTION)
        self.Yr = Yr

        # "measured" x dispalcement at each spot(ALSO ON RECONSTRUCTION)
        self.dXq = dXq

        # "measured" y dispalcement at each spot(ALSO ON RECONSTRUCTION)
        self.dYq = dYq

        # Calibrated zero at each QC, for a flat input WF (c[n][m]=0, for all n,m)(ALSO ON RECONSTRUCTION)
        self.outx_cal = outx_cal

        # Calibrated zero at each QC, for a flat input WF (c[n][m]=0, for all n,m)(ALSO ON RECONSTRUCTION)
        self.outy_cal = outy_cal

        # "real" dX in realtion to each QC center in QC coord system(ALSO ON RECONSTRUCTION)
        self.dXql = dXql

        # "real" dY in realtion to each QC center in QC coord system(ALSO ON RECONSTRUCTION)
        self.dYql = dYql

        # Acumulates Wxmax and Wxmin difference values(ALSO ON RECONSTRUCTION)
        self.dWx = dWx

        # Acumulates Wymax and Wymin difference values(ALSO ON RECONSTRUCTION)
        self.dWy = dWy

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
    
