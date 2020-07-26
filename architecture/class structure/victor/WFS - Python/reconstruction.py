#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#reconstruction.py

import math
import numpy

import main as main
import sampling as s
import ZERNIKE as Z

###Início cabeçalho
PI = 3.14159265358979323844
###Fim cabeçalho

def basis(n_spots, max_order):
	print("reconstruction::basis")

	global z_basis

	i = 0
	j = 0
	h = 0
	nn = 0

	for i in numpy.arange(0,main.max_order,1):
		for j in numpy.arange(0,main.n_ml,1):
			for h in numpy.arange(0,main.n_ml,1):
				rhox1 = 0.0
				phix1 = 0.0
				rhox2 = 0.0
				phix2 = 0.0
				rhoy1 = 0.0
				phiy1 = 0.0
				rhoy2 = 0.0
				phiy2 = 0.0
				tiltx = 0.0
				tilty = 0.0
				nn = i * main.n_spots + (j * main.n_ml + h)

				rhox1 = math.sqrt(math.pow(main.Xr[int(j)][int(h)] + main.delta, 2) + math.pow(main.Yr[int(j)][int(h)], 2))
				phix1 = Z.phase(main.Yr[int(j)][int(h)], main.Xr[int(j)][int(h)] + main.delta)
				rhox2 = math.sqrt(math.pow(main.Xr[int(j)][int(h)] - main.delta, 2) + math.pow(main.Yr[int(j)][int(h)], 2))
				phix2 = Z.phase(main.Yr[int(j)][int(h)], main.Xr[int(j)][int(h)] - main.delta)

				rhoy1 = math.sqrt(math.pow(main.Xr[int(j)][int(h)], 2) + math.pow(main.Yr[int(j)][int(h)] + main.delta, 2))
				phiy1 = Z.phase(main.Yr[int(j)][int(h)] + main.delta, main.Xr[int(j)][int(h)])
				rhoy2 = math.sqrt(math.pow(main.Xr[int(j)][int(h)], 2) + math.pow(main.Yr[int(j)][int(h)] - main.delta, 2))
				phiy2 = Z.phase(main.Yr[int(j)][int(h)] - main.delta, main.Xr[int(j)][int(h)])

				tiltx = Z.Zernike(main.nz[i], main.mz[i], rhox1 / main.rad, phix1)
				tiltx -= Z.Zernike (main.nz[i], main.mz[i], rhox2 / main.rad, phix2)
				tiltx /= 2. * main.delta
				tiltx *= main.f

				tiltx = Z.Zernike(main.nz[i], main.mz[i], rhoy1 / main.rad, phiy1)
				tiltx -= Z.Zernike (main.nz[i], main.mz[i], rhoy2 / main.rad, phiy2)
				tiltx /= 2. * main.delta
				tiltx *= main.f

				main.z_basis[int(nn * 2)] = tiltx
				main.z_basis[int(nn * 2 + 1)] = tilty

	return 0

def reconst():
	print("reconstruction::reconst")

	global coeff
	global z_basis
	global coeff
	global c
	global outFile6
	global out_wf_reconstsem
	global out_wf_reconstcom

	Wout = 0.0
	i = 0
	j = 0
	bb = 0
	n = 0
	m = 0
	vector = 0.0
	outFile6 = []
	outFile6 = open("res.txt", "w")
	if outFile6 == None :
		print("Unable to open res.txt")
		exit(1)
	vector = [0.0] * int(main.n_spots) * 8
	
	main.coeff = [0.0] * int(main.max_order) * 4
	
	main.z_basis = [0.0] * int(main.n_spots * 4) * int(main.max_order)
	basis(main.n_spots, main.max_order)
	for i in numpy.arange(1,main.n_ml,1):
		for j in numpy.arange(1,main.n_ml,1):
			bb = i * main.n_ml + j
			vector[int(bb * 2)] = main.dXq[int(i)][int(j)]
			vector[int(bb * 2 + 1)] = main.dYq[int(i)][int(j)]

	decomp(main.z_basis, vector, main.n_spots * 2, main.max_order)
	for i in range(0,main.max_order,1):
		main.coeff[int(i)] *= 1.0

	for i in range(0,main.max_order,1):
		n = main.nz[int(i)]
		m = main.mz[int(i)]
		
		main.c[n][m] = main.coeff[i]
		print(int(n), "\t", int(m), "\t", float(main.c[n][m]), file = outFile6)

	for main.jx in numpy.arange(-main.dimens * 1.5,main.dimens * 1.5 + main.step,main.step):
		for main.jy in numpy.arange(-main.dimens * 1.5,main.dimens * 1.5 + main.step,main.step):
			Wout = 0.0
			Wout = s.calculate(main.jx,main.jy)
			if main.rodaSpice == 0 or main.rodaSpice == 1 :
				print(float(Wout), end = '', file = main.out_wf_reconstsem)
			if main.jy != main.dimens * 1.5 and (main.rodaSpice == 0 or main.rodaSpice == 1) :
				print("\t", end = '', file = main.out_wf_reconstsem)
			elif main.rodaSpice == 0 or main.rodaSpice == 1 :
				print("\n", end = '', file = main.out_wf_reconstsem)
			if main.rodaSpice == 2 :
				print(float(Wout), end = '', file = main.out_wf_reconstcom)
			if main.jy != main.dimens * 1.5 and main.rodaSpice == 2 :
				print("\t", end = '', file = main.out_wf_reconstcom)
			elif main.rodaSpice == 2 :
				print("\n", end = '', file = main.out_wf_reconstcom)

	main.out_wf_reconstsem.close()
	#main.out_wf_reconstcom.close() #Ativado somente quando utilizar o SPICE.

	return(0)

def simq(A, B, n, flag, IPS):
	print("reconstruction::simq")

	i = 0
	j = 0
	ij = 0
	ip = 0
	ipj = 0
	ipk = 0
	ipn = 0
	idxpiv = 0
	iback = 0
	k = 0
	kp = 0
	kp1 = 0
	kpk = 0
	kpn = 0
	nip = 0
	nkp = 0
	nm1 = 0
	em = 0.0
	q = 0.0
	rownrm = 0.0
	big = 0.0
	size = 0.0
	pivot = 0.0
	SUM = 0.0 #Em caixa alta para difrenciar de sumain.

	if flag >= 0 :
		ij = 0
		for i in range(0,n,1) :
			IPS[i] = i
			rownrm = 0.0
			for j in range(0,n,1) :
				q = math.fabs(A[ij])
				if rownrm < q :
					rownrm = q
				ij += 1

			if rownrm == 0.0 :
				print("SIMQ ROWNRM=0")
				return(1)

			V[i] = 1.0 / rownrm

		nm1 = n - 1
		for k in range(0,nm1,1):
			big = 0.0
			for i in range(k,n,1):
				ip = IPS[i]
				ipk = n * ip + k
				size = math.fabs(A[ipk] * V[ip])
				if size > big :
					big = size
					idxpiv = i

			if big == 0 :
				print("SIMQ BIG=0")
				return(2)

			if idxpiv != k :
				j = IPS[k]
				IPS[k] = IPS[idxpiv]
				IPS[idxpiv] = j

			kp = IPS[k]
			kpk = n * kp + k
			pivot = A[kpk]
			kp1 = k + 1
			for i in range(kp1,n,1):
				ip = IPS[i]
				ipk = n * ip + k
				em = -A[ipk] / pivot
				A[ipk] = -em
				nip = n * ip
				nkp = n * kp
				for j in range(kp1,n,1):
					ipj = nip + j
					A[ipj] = A[ipj] + em * A[nkp + j]


		kpn = n * IPS[n - 1] + n - 1
		if A[kpn] == 0.0 :
			print("SIMQ A[kpn]=0")
			return(3)

	ip = IPS[0]
	V[0] = B[ip]
	for i in range(1,n,1):
		ip = IPS[i]
		ipj = n * ip
		SUM = 0.0
		for j in range(0,i,1) :
			SUM += A[ipj] * V[j]
			ipj += 1

		V[i] = B[ip] - SUM

	ipn = n * IPS[n - 1] + n - 1
	V[n - 1] = V[n - 1] / A[ipn]

	for iback in range(1,n,1):
		i = n - 1 - iback
		ip = IPS[i]
		nip = n * ip
		SUM = 0.0
		for j in range(i + 1,n,1):
			SUM += A[nip + j] * V[j]
		V[i] = (V[i] - SUM) / A[nip + i]

	return(0)		

##(decomposition + Gauss here)
A = [0.0]
B = [0.0]
V = [0.0]

def decomp(z_basis, vector, n, m):
	print("reconstruction::decomp")

	global A
	global B
	global V
	global coeff

	IPS = [0]
	i = 0
	j = 0
	jj = 0
	error = 0
	num1 = 0
	num2 = 0

	A = [0.0] * int(m * m)
	if A == None :
		print("\nMalloc error in decomp A")#Modificado para print de erro na tela.
		exit(1)

	B = [0.0] * int(m * 2)
	if B == None :
		print("\nMalloc error in decomp B")#Modificado para print de erro na tela.
		exit(1)

	V = [0.0] * int(m * 2)
	if V == None :
		print("\nMalloc error in decomp V")#Modificado para print de erro na tela.
		exit(1)
	
	IPS = [0] * int(m * 2)
	if IPS == None :
		print("\nMalloc error in decomp IPS")#Modificado para print de erro na tela.
		exit(1)

	for i in range(0,m,1) :
		for j in range(0,m,1) :
			nn = 0
			nn = i * m + j
			A[int(nn)] = 0.0
			for jj in numpy.arange(1,n,1) :
				num1 = i * n + jj
				num2 = j * n + jj
				A[int(nn)] += z_basis[int(num1)] * z_basis[int(num2)]
			num1 = 0
			num2 = 0

		B[i] = 0.0
		for jj in numpy.arange(0,n,1) :
			numl = 0
			numl = i * n + jj
			B[i] += z_basis[int(numl)] * vector[int(jj)]

	error = simq(A, B, m, 0, IPS)
	if error != 0 :
		print("\nError in Gauss elemination simq")
		return(1)

	for i in range(0,m,1):
		main.coeff[i] = V[i]

	return(0)