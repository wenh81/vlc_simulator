#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#sampling.py

import math
import numpy

import main
import qc_analysis as q
import ZERNIKE as Z

def slope_QC():
	print("sampling::slope_QC")

	global x_edge
	global yb
	global Ac
	global Bc
	global Cc
	global Dc
	global outx
	global slope
	global xx

	R = 0.0
	resolucao = 10.00005
	sd = 0.0
	sd1 = 0.0
	media = 0.0
	soma1 = 0.0
	soma2 = 0.0
	intens = 0.0
	b0 = 0.0
	b1 = 0.0
	xs = 0.0
	NN = 50.0
	ccc = 0.0
	main.x_edge = 0.0
	R = 0.0
	main.yb = 0.0
	main.Ac = 0.0
	main.Bc = 0.0
	main.Cc = 0.0
	main.Dc = 0.0
	#while R <= resolucao :
	ccc = 0.0
	main.x_edge = 0.23
	sd = 0.0
	sd1 = 0.0
	media = 0.0
	soma1 = 0.0
	soma2 = 0.0
	intens = 0.0
	b0 = 0.0
	b1 = 0.0
	xs = 0.0
	main.outx = 0.0
	##Cálculo da média
	for main.xx in numpy.arange(-main.x_edge,main.x_edge + (main.x_edge / NN),main.x_edge / NN):
		if main.x_edge == 0 or NN == 0:
			print("Calc media", 0.0)
		else :
			print("Calc media",round((main.xx) / (main.x_edge / NN)))
		q.qcell(main.xx,0)
		if (main.Ac + main.Bc + main.Cc + main.Dc) == 0 :
			main.outx += 0
		else :
			main.outx += ((main.Bc + main.Cc) - (main.Ac + main.Dc)) / (main.Ac + main.Bc + main.Cc + main.Dc)
		main.Ac = 0.0
		main.Bc = 0.0
		main.Cc = 0.0
		main.Dc = 0.0
		xs += main.xx
		ccc += 1.0
	if ccc == 0 :
		media = 0
	else :
		media = main.outx / ccc
	if ccc == 0 :
		xs = 0
	else :
		xs /= ccc
	print(ccc, media, xs)
	main.outx = 0.0
	##Cálculo do slope
	for main.xx in numpy.arange(-main.x_edge,main.x_edge + main.x_edge / NN,main.x_edge / NN):
		if main.x_edge == 0 or NN == 0:
			print("Calc slope", 0.0)
		else :
			print("Calc slope",round((main.xx) / (main.x_edge / NN)))
		q.qcell(main.xx,0)
		if (main.Ac + main.Bc + main.Cc + main.Dc) == 0 :
			main.outx = 0
		else :
			main.outx = ((main.Bc + main.Cc) - (main.Ac + main.Dc)) / (main.Ac + main.Bc + main.Cc + main.Dc)
		intens = main.outx
		main.Ac = 0.0
		main.Bc = 0.0
		main.Cc = 0.0
		main.Dc = 0.0
		soma1 += ((main.xx - xs) * (intens - media))
		soma2 += math.pow((main.xx - xs),2)
		if soma2 == 0 :
			b1 = 0
		else :
			b1 = soma1 / soma2
		b0 = media - b1 * xs
	print(b0)
	##Cálculo do desvio padrão
	for main.xx in numpy.arange(-main.x_edge,main.x_edge + main.x_edge / NN,main.x_edge / NN):
		if main.x_edge == 0 or NN == 0:
			print("Calc desvio padrão", 0.0)
		else :
			print("Calc desvio padrão",round((main.xx) / (main.x_edge / NN)))
		q.qcell(main.xx,0)
		if (main.Ac + main.Bc + main.Cc + main.Dc) == 0 :
			main.outx = 0
		else :
			main.outx = ((main.Bc + main.Cc) - (main.Ac + main.Dc)) / (main.Ac + main.Bc + main.Cc + main.Dc)	
		main.Ac = 0.0
		main.Bc = 0.0
		main.Cc = 0.0
		main.Dc = 0.0
		sd1 += math.pow((main.outx - (b0 + b1 * main.xx)),2)
	sd1 /= (ccc - 2)
	sd = math.sqrt(sd1)
	sd /= main.cell_qc
	main.outx = 0.0
	if b1 == 0 :
		R = 0
	else :
		R = sd / b1	
	if R <= resolucao :
		main.slope = b1
		main.yb = b0
	#print(R)
	#Fim while

def input_coeff():
	#print("sampling::input_coeff")

	global c
	global inFile

	n = 0.0
	m = 0.0
	jv = 0.0
	cc = 0.0

	if main.turb_flag != 1 :
		for n in numpy.arange(0,nz[main.max_order] + 1,1):
			for m in numpy.arange(-n,n + 2,2):
				main.c[n][m] = 0.0
		main.c[na][ma] = 1.0
	else :
		main.inFile = open("coeff.txt", "r")
		if main.inFile == None :
			printf("Unable to open coeff.txt")
			exit(1)
		varmatriz = main.inFile.readlines()	
		for jv in numpy.arange(1,main.max_order + 1,1):
			varchar = varmatriz[jv - 1].split()
			n = int(varchar[0])
			m = int(varchar[1])
			cc = float(varchar[2])
			main.c[n][m] = cc
		main.inFile.close()
		if main.flag_defocus == 1 :
			main.c[1][-1] = 0.0
			main.c[1][1] = 0.0
		else :
			main.c[1][-1] = 0.0
			main.c[1][1] = 0.0
			main.c[2][0] = 0.0

def wfs_comput():
	print("sampling::wfs_comput")

	global a
	global b
	global Wf1
	global dWx
	global dWy
	global out_wf_original
	global nn
	global W
	global a1
	global b1

	x = 0.0
	y = 0.0
	Wxmax = 0.0
	Wxmin = 0.0
	Wymax = 0.0
	Wymin = 0.0
	nn = 0.0
	W = 0.0
	a1 = 0.0
	b1 = 0.0

	for main.jx in numpy.arange(-main.dimens * 1.5,(main.dimens * 1.5) + main.step,main.step):
		for main.jy in numpy.arange(-main.dimens * 1.5,(main.dimens * 1.5) + main.step,main.step):
			#print(main.jx, main.jy)
			main.a = -1.0
			main.b = -1.0
			if main.jx > (-main.dimens - main.step) and main.jy > (-main.dimens - main.step) :
				for a1 in numpy.arange(0,main.n_ml,1) :
					for b1 in numpy.arange(0,main.n_ml,1) :
						if math.pow((main.jx - main.Xr[int(a1)][int(b1)]),2) + math.pow((main.jy - main.Yr[int(a1)][int(b1)]),2) <= math.pow(main.ml_dimen / 2,2) :
							main.a = a1 #RAIO INTERNO DA QC
							main.b = b1
			x = main.jx
			y = main.jy
			calculate(x,y)
			print(float(W), end = '', file = main.out_wf_original)
			if main.jy != main.dimens * 1.5 :
				print("\t", end = '', file = main.out_wf_original)
			else :
				print("\n", end = '', file = main.out_wf_original)
			main.Wf1[int(main.a)][int(main.b)] += main.W #SOMA DE TODOS OS VALORES DE W DENTRO DO RAIO DA QC
			y = main.jy
			x = main.jx + main.delta
			Wxmax = calculate(x,y)
			x = main.jx - main.delta
			Wxmin = calculate(x,y)
			main.dWx[int(main.a)][int(main.b)] += (Wxmax - Wxmin) / (2 * main.delta)#CÁLCULO DA DERIVADA PARA CADA PONTO
			x = main.jx
			y = main.jy + main.delta
			Wymax = calculate(x,y)
			y = main.jy - main.delta
			Wymin = calculate(x,y)
			main.dWy[int(main.a)][int(main.b)] += (Wymax - Wymin) / (2 * main.delta)
			if main.b == (main.n_ml - 1) and main.a == 0 :
				nn += 1.0 #NÚMERO DE W DENTRO DO RAIO DA QC

	return 0


def calculate(x1, y1):
	global W

	n = 0
	m = 0
	rho = 0.0
	phi = 0.0
	main.W = 0.0

	rho = math.sqrt(math.pow(x1,2) + math.pow(y1,2)) / main.rad
	phi = Z.phase(y1,x1)
	if rho >= 1 :
		main.W = 0.0
	else :
		for n in numpy.arange(1,main.nz[main.max_order-1] + 1,1) :
			for m in numpy.arange(-n,n + 2,2) :
				#print(n, m)
				main.W += main.c[int(n)][int(m)] * Z.Zernike(n,m,rho,phi)
				
	return main.W

def zern_ind(max_order):
	print("sampling::zern_ind")
	
	global nz
	global mz

	i = 0
	j = 0
	k = 0

	while i <= main.max_order:
		for j in numpy.arange(k % 2,k + 2,2):
			main.nz[i] = k
			main.mz[i] = j
			i += 1
			if j != 0 :
				main.nz[i] = k
				main.mz[i] = (-j)
				i += 1
		k += 1
	j = i - 1
	for i in numpy.arange(0,j,1):
		main.nz[i] = main.nz[i + 1]
		main.mz[i] = main.mz[i + 1]

	return j