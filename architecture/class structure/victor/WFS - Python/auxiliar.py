#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#auxiliar.py

import math
import numpy

import main
import sampling as s
import qc_analysis as q

def calib():

	global c
	global a
	global b
	global Wf1
	global dWx
	global dWy
	global dX
	global dY
	global dXg
	global dYg
	global dXqg
	global dYqg
	global dXql
	global dYql
	global As
	global Bs
	global Cs
	global Ds
	global outx_cal
	global outy_cal
	global oxtl_flag
	global Aq
	global Bq
	global Cq
	global Dq

	n = 0
	m = 0
	for n in range(0,main.nz[main.max_order - 1] + 1,1):
		for m in range(-n,n + 2,2):
			
			main.c[n][m] = 0.0

	s.wfs_comput()
	
	main.a = 0
	main.b = 0
	for a in range(0,main.n_ml,1):
		for b in range(0,main.n_ml,1):
			
			main.Wf1[main.a][main.b] /= main.nn
			main.dWx[main.a][main.b] /= main.nn
			main.dWy[main.a][main.b] /= main.nn
			main.dX[main.a][main.b] = main.f * dWx[main.a][main.b]
			main.dY[main.a][main.b] = main.f * dWy[main.a][main.b]
			main.dXg[main.a][main.b] = dX[main.a][main.b] + main.Xr[main.a][main.b]
			main.dYg[main.a][main.b] = dY[main.a][main.b] + main.Yr[main.a][main.b]

			if main.rot_flag == 0 :
				main.dXqg[main.a][main.b] = main.dXg[main.a][main.b] * math.cos(main.theta) - main.dYg[main.a][main.b] * math.sin(main.theta)
				main.dYqg[main.a][main.b] = main.dXg[main.a][main.b] * math.sin(main.theta) + main.dYg[main.a][main.b] * math.cos(main.theta)
			else :
				main.dXqg[main.a][main.b] = (main.dXg[main.a][main.b] - 2 * math.sqrt(2) * main.dimens * math.sin(main.theta / 2) * math.sin(45 - main.theta / 2)) * math.cos(main.theta) - (main.dYg[main.a][main.b] - 2 * math.sqrt(2) * main.dimens * math.sin(main.theta / 2) * math.cos(45 - main.theta / 2)) * math.sin(main.theta)
				main.dYqg[main.a][main.b] = (main.dXg[main.a][main.b] - 2 * math.sqrt(2) * main.dimens * math.sin(main.theta / 2) * math.sin(45 - main.theta / 2)) * math.sin(main.theta) + (main.dYg[main.a][main.b] - 2 * math.sqrt(2) * main.dimens * math.sin(main.theta / 2) * math.cos(45 - main.theta / 2)) * math.cos(main.theta)
			
			main.dXql[main.a][main.b] = main.dXqg[main.a][main.b] - main.Xr[main.a][main.b]
			main.dYql[main.a][main.b] = main.dYqg[main.a][main.b] - main.Yr[main.a][main.b]

			if math.fabs(main.dXql[main.a][main.b]) > main.cell_qc or math.fabs(main.dYql[main.a][main.b]) > main.cell_qc :
				print("Calibration step\n\nATTENTION!\n\nSpot center outside QC")
				print("\nMicrolens [", main.a, "][", main.b, "]")
				exit(1)
			
	if main.flag_interferencia == 0 :
		for main.a in range(0,main.n_ml,1):
			for main.b in range(0,main.n_ml,1):
				As = 0.0
				Bs = 0.0
				Cs = 0.0
				Ds = 0.0
				outx_cal[main.a][main.b] = 0.0
				outy_cal[main.a][main.b] = 0.0
				q.qcell((main.dXql[main.a][main.b]) / (main.cell_qc), (main.dYql[main.a][main.b]) / (main.cell_qc))
				main.As += main.Aq
				main.Bs += main.Bq
				main.Cs += main.Cq
				main.Ds += main.Dq
	else :
		for aa in range(main.a - 1,main.a + 2,1):
			for bb in range(main.b - 1,main.b + 2,1):
				if (aa > -1) and (aa < main.n_ml) and (bb > -1) and (bb < main.n_ml):
					if aa == main.a and bb == main.b :
						main.oxtl_flag = 0
					else :
						main.oxtl_flag = 1
					q.qcell((main.dXql[aa][bb] + (aa - main.a) * main.ml_dimen) / (main.cell_qc), (main.dYql[aa][bb] + (bb - main.b) * main.ml_dimen) / (main.cell_qc))
					main.As += main.Aq
					main.Bs += main.Bq
					main.Cs += main.Cq
					main.Ds += main.Dq
	main.outx_cal[main.a][main.b] = ((main.Bs + main.Cs) - (main.As + main.Ds)) / (main.As + main.Bs + main.Cs + main.Ds)
	main.outy_cal[main.a][main.b] = ((main.As + main.Bs) - (main.Cs + main.Ds)) / (main.As + main.Bs + main.Cs + main.Ds)
	
	main.Aq = 0.0
	main.Bq = 0.0
	main.Cq = 0.0
	main.Dq = 0.0

	return 0

def rms_calc():
	
	global jx
	global jy
	global Wrms
	global c

	n = 0
	m = 0
	i = 0
	Win = 0.0
	Wout = 0.0
	np = 0

	for main.jx in numpy.arange(-main.dimens * 1.5, main.dimens * 1.5 + main.step, main.step):
		for main.jy in numpy.arange(-main.dimens * 1.5, main.dimens * 1.5 + main.step, main.step):
			Win = 0.0
			Wout = 0.0
			s.input_coeff()
			Win = s.calculate(main.jx, main.jy)
			for i in numpy.arange(0,main.max_order,1):
				n = main.nz[i]
				m = main.mz[i]
					
				main.c[n][m] = main.coeff[i]

			Wout = s.calculate(main.jx, main.jy)
			main.Wrms += math.pow(Wout - Win,2)
			np += 1
	main.Wrms /= (np - 1)
	main.Wrms = math.sqrt(main.Wrms)

	return 0