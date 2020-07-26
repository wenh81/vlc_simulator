
# Determinate if ML system needs rotation
rot_flag = 0

# Determinates non-linearity in percentage
nonlin = 0

# Determinates coefficients origin (extern or produce it)
turb_flag = 0

# random generator initialization seed
iseed = []

# Record control and derivative calculation on wfs-comput
print_ctrl = 0

# Sinalizes to linear aproximation slope calculation
smooth = 0

# Sinalizes to file  record
grava_arquivos = 0

# Sinalizes to file import
flag_V_QC = 0

# Sinalizes for ortogonal or non-ortogonal (extern) matriz
matriz_ortogonal = 0

# Sinalizes to consider or not QC with sampling
flag_amostragem = 0

# Sinalizes to extern entrance of WF data
flag_experimental = 0

# Sinalizes for interference consideration between QCs
flag_interferencia = 0

# Sinalizes for type of aproximation 
flag_linear_resp_QC = 0

# Sinalizes for type of aproximation response(automatic or calculated)
flag_sigm_auto_resp_QC = 0

# ???Sinalizes for type of aproximation origin
flag_poli_resp_QC = 0

# Sinalizes for file record for Spice simulation
flag_spice = 0

# Sinalizes for use of extern file containing displacements values
flag_XQC_YQC = 0

# Sinalizes for use of extern file containing voltages values
#flag_Vout_QC = 0

# Sinalizes for file record of calculated displacements for Spice
flag_grava_outx_spice = 0

# Sinalizes for desconsideration of defocus term on Zernike coefficients
flag_defocus = 0

# ???optical crosstalk flag; if = 0, adds FPN, else doesn't
oxtl_flag = 0

#QC's format. 1 for square, 0 for circular
qc_format = 0

#QC's type of approximation. 1 for linear, 0 for sigmoidal
flag_approx_type = 0

# Pi value
PI = 314159265358979

# Boltzman constant (J/K)
Kb = 1.38066e-18

# Plancks constant (J.s)
hplk = 6.62608e-29

# Speed of light in vacuum (m/s)
c0 = 29979245800000000

# hplk*c0
hplk_c0 = 1.9864488101e-15

# hplk*c0/ele
hplk_c0_e = 12398.435442

# electron charge  (Coulomb)
ele = 1.602177e-13

# standard (max) size of the matrix for the wavefronts (check if right!)
N = 10

# Rotation angle of QC system (degree)
theta = 0

# Scan-position step
stepp = 20.0

# ....?
G = 0.025