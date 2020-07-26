class Reconstruction(object):
    def __init__(self, c, dX, dY, dXg, dYg, dXqg, dYqg, Xr, Yr, dXq, dYq, outx_cal, outy_cal, dXql, dYql, dWx, dWy, Wf1, W, Wrms, delta, yb, x_edge, z_basis, coeff, nz, mz, nn, a, b, a1, b1, theta, jx, jy, na, ma, xx, outx_l):
        """Constructor"""

        # Zernike coefficient, c[n][m]
        self.c = c

        # "real" x displacement at each spot
        self.dX = dX

        # "real" y displacement at each spot
        self.dY = dY

        # "real" dX in realtion to ML system center
        self.dXg = dXg

        # "real" dY in realtion to ML system center
        self.dYg = dYg

        # "real" dX in relation to QC system center
        self.dXqg = dXqg

        # "real" dY in relation to QC system center
        self.dYqg = dYqg

        # x coordinate of center of microlen
        self.Xr = Xr

        # y coordinate of center of microlen
        self.Yr = Yr

        # "measured" x dispalcement at each spot
        self.dXq = dXq

        # "measured" y dispalcement at each spot
        self.dYq = dYq

        # Calibrated zero at each QC, for a flat input WF (c[n][m]=0, for all n,m)
        self.outx_cal = outx_cal

        # Calibrated zero at each QC, for a flat input WF (c[n][m]=0, for all n,m)
        self.outy_cal = outy_cal

        # "real" dX in realtion to each QC center in QC coord system
        self.dXql = dXql

        # "real" dY in realtion to each QC center in QC coord system
        self.dYql = dYql

        # Acumulates Wxmax and Wxmin difference values
        self.dWx = dWx

        # Acumulates Wymax and Wymin difference values
        self.dWy = dWy

        # Acumulates W values of WF for each spot of the microlen
        self.Wf1 = Wf1

        # WF local value
        self.W = W

        # RMS error between input and output WF
        self.Wrms = Wrms

        # Delta variable for derivative calculations(um)
        self.delta = delta

        # 0.
        self.yb = yb

        # Can assume values between 0 and 1, 0 means QC-center, 1 means QC edge(ALSO ON QUADCELL)
        self.x_edge = x_edge

        # basis formed by zernikes at each spot
        self.z_basis = z_basis

        # calculated coefficients to zernike polynomials
        self.coeff = coeff

        # zernike n indice for each zernike term
        self.nz = nz

        # zernike m indice for each zernike term
        self.mz = mz

        # Number of integrations points inside the QC(ALSO ON QUADCELL)
        self.nn = nn

        # vector indice
        self.a = a

        # vector indice
        self.b = b

        # Variable for determinate microlen
        self.a1 = a1

        # Variable for determinate microlen
        self.b1 = b1

        # Rotation angle of QC system (radian) (ALSO ON QUADCELL)
        self.theta = theta

        # X position of QC in realation to the microlens coord. system(ALSO ON QUADCELL)
        self.jx = jx

        # Y position of QC in realation to the microlens coord. system(ALSO ON QUADCELL)
        self.jy = jy

        # n in realation to the microlens coord. system(ALSO ON QUADCELL)
        self.na = na

        # m in realation to the microlens coord. system(ALSO ON QUADCELL)
        self.ma = ma

        # 0.(ALSO ON QUADCELL)
        self.xx = xx

        # 0.(ALSO ON QUADCELL)
        self.outx_l = outx_l
    
        pass

    def getZernike_term(self, n, m, rho, phi):
        """Calculates a Zernike term"""
        pass
    

    def simq(self, A, B, n, flag, IPS):
        """docstring"""
        pass
    

    def basis(self, n_spots, max_order):
        """sask"""
        pass
    

    def decomp(self, z_basis, vector, n, m):
        """asd"""
        pass
    

    def reconst(self, input_displacement_file):
        """Calculates the coefficients given input displacements file. Returns a coefficient list"""
        pass
    

    def calc_RMS(self, coeff_0, coeff_1):
        """Claculates the RMS difference between two WFs"""
        pass
    
