#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#qc_analysis.py

import math
import random
import numpy

import interface as i
import main as m
import poisson as p

import os

def photogenerated_current(coef, ln, lp, dn, dp, sp, sn, r, area, irradiancia, lam, xp, xn):
	print("qc_analysis::photogenerated_current")

	Jn = 0.0
	Jn1 = 0.0
	Jn2 = 0.0
	Jn3 = 0.0
	Jn4 = 0.0
	Jn5 = 0.0
	Jp = 0.0
	Jp1 = 0.0
	Jp2 = 0.0
	Jp3 = 0.0
	Jp4 = 0.0
	Jp5 = 0.0
	Jtot = 0.0
	teta = 0.0
	tetal = 0.0
	lam = m.lamb * 1e6
	teta = 1e16 * irradiancia * lam / 19.8
	tetal = math.exp(-1 * coef * xn) * teta
	q = 1.6e-19
	Jn1 = -1 * coef * lp * math.exp(-1 * coef * xn)
	Jn2 = sn * (lp / dp) + coef * lp
	Jn3 = math.exp(-1 * coef * xn)
	Jn4 = (sn * (lp / dp) * math.cosh(xn / lp)) + math.sinh(xn / lp)
	Jn5 = math.cosh(xn / lp) + (sn *(lp / dp) * math.sinh(xn / lp))
	Jn = Jn1 + ((Jn2 - (Jn3 * Jn4)) / Jn5)
	Jn *= (q * coef * teta * (1 - r) * lp)
	Jn /= (math.pow(coef * lp, 2) - 1)
	Jp1 = (coef * ln)
	Jp2 = sp * (ln / dn)
	Jp3 = (math.cosh(xp / ln) - math.exp(-1 * coef * xp))
	Jp4 = math.sinh(xp / ln) + (coef * ln * math.exp(-1 * coef * xp))
	Jp5 = math.cosh(xp / ln) + (sp * (ln / dn) * math.sinh(xp / ln))
	Jp = Jp1 - (((Jp2 * Jp3) + Jp4) / Jp5)
	Jp *= (q * coef * tetal * (1 - r) * ln) / (math.pow(coef * ln, 2) - 1)
	Jtot = (Jn + Jp)
	corrente = 0.0
	corrente = Jtot * area

	return corrente

def grava_le_arquivos(numero_de_spots_varridos):
	print("qc_analysis::grava_le_arquivos")
	
	global TimeSpiceclk
	global T_on
	global T_off
	global TimeSpice
	global inFile3
	global As
	global Bs
	global Cs
	global Ds
	global out_irradianciaA
	global out_irradianciaB
	global out_irradianciaC
	global out_irradianciaD
	global outFile_CorrenteA
	global outFile_CorrenteB
	global outFile_CorrenteC
	global outFile_CorrenteD
	global out_clock


	correnteA = 0.0
	correnteB = 0.0
	correnteC = 0.0
	correnteD = 0.0
	T_inc = 0.0
	T_inc = m.TimeSpice_int * 1e-7

	if m.grava_arquivos == 1 :
		
		m.TimeSpiceclk = m.TimeSpice + T_inc
		
		m.T_on = m.TimeSpiceclk + m.TimeSpice_int * m.Int_on
		
		m.T_off = m.T_on + T_inc

		print(float(m.TimeSpice), "e-003\t ", float(m.Ac), file = m.out_irradianciaA)
		correnteA = photogenerated_current(m.coefabs, m.Ln, m.Lp, m.Dn, m.Dp, m.Sb, m.Se, m.reflect, m.area_Ph, m.Ac, m.lamb, m.Wb, m.We)
		print(float(m.TimeSpice), "e-003\t ", float(correnteA), file = m.outFile_CorrenteA)

		print(float(m.TimeSpice), "e-003\t ", float(m.Bc), file = m.out_irradianciaB)
		correnteB = photogenerated_current(m.coefabs, m.Ln, m.Lp, m.Dn, m.Dp, m.Sb, m.Se, m.reflect, m.area_Ph, m.Ac, m.lamb, m.Wb, m.We)
		print(float(m.TimeSpice), "e-003\t ", float(correnteB), file = m.outFile_CorrenteB)

		print(float(m.TimeSpice), "e-003\t ", float(m.Cc), file = m.out_irradianciaC)
		correnteC = photogenerated_current(m.coefabs, m.Ln, m.Lp, m.Dn, m.Dp, m.Sb, m.Se, m.reflect, m.area_Ph, m.Ac, m.lamb, m.Wb, m.We)
		print(float(m.TimeSpice), "e-003\t ", float(correnteC), file = m.outFile_CorrenteC)

		print(float(m.TimeSpice), "e-003\t ", float(m.Dc), file = m.out_irradianciaD)
		correnteD = photogenerated_current(m.coefabs, m.Ln, m.Lp, m.Dn, m.Dp, m.Sb, m.Se, m.reflect, m.area_Ph, m.Ac, m.lamb, m.Wb, m.We)
		print(float(m.TimeSpice), "e-003\t ", float(correnteD), file = m.outFile_CorrenteD)

		print(float(m.TimeSpiceclk), "e-003\t ", 5, file = m.out_clock)
		print(float(m.T_on), "e-003\t ", 5, file = m.out_clock)
		print(float(m.T_off), "e-003\t ", 0, file = m.out_clock)
		
		m.TimeSpice += m.TimeSpice_int

		print(float(m.TimeSpice), "e-003\t ", float(m.Ac), file = m.out_irradianciaA)
		print(float(m.TimeSpice), "e-003\t ", float(m.Bc), file = m.out_irradianciaB)
		print(float(m.TimeSpice), "e-003\t ", float(m.Cc), file = m.out_irradianciaC)
		print(float(m.TimeSpice), "e-003\t ", float(m.Dc), file = m.out_irradianciaD)

		print(float(m.TimeSpice), "e-003\t ", float(correnteA), file = m.outFile_CorrenteA)
		print(float(m.TimeSpice), "e-003\t ", float(correnteB), file = m.outFile_CorrenteB)
		print(float(m.TimeSpice), "e-003\t ", float(correnteC), file = m.outFile_CorrenteC)
		print(float(m.TimeSpice), "e-003\t ", float(correnteD), file = m.outFile_CorrenteD)

		m.TimeSpice += T_inc
		print(float(m.TimeSpice), "e-003\t ", 0, file = m.out_clock)
	##PARAMOS AQUI 06/07
	if m.flag_V_QC == 1 :
		if m.flag_Vout_QC == 1 :
			if m.flag_spice == 0 :
				m.TimeSpiceclk = m.TimeSpice + T_inc
				m.T_on = m.TimeSpiceclk + m.TimeSpice_int * m.Int_on
				m.TimeSpice += m.TimeSpice_int + T_inc
			m.inFile3 = open("SAIDA_QC.txt", "r")
			if m.inFile3 == None :
				print("Unable to open spice file input, SAIDA_QC.txt")
				os.system("PAUSE")
				exit(1)
			cont = 0
			VoutA = 0.0
			VoutB = 0.0
			VoutC = 0.0
			VoutD = 0.0
			time = 0.0
			diff = 10.0
			diff1 = 0.0
			TSpice_amostra = 0.0
			TSpice_amostra = (m.TimeSpice_int * m.Int_on * m.Int_amostra) * 5e-3
			TSpice_amostra += m.T_on * 1e-3
			TSpice_amostra = 9.5e-3
			maxA = 0.0
			maxA2 = 0.0
			maxB = 0.0
			maxB2 = 0.0
			maxC = 0.0
			maxC2 = 0.0
			maxD = 0.0
			maxD2 = 0.0
			temporario = 0.0
			crescente = 1

			#PARA RICOCHETE
			vmin = i.vmin
			vmax = i.vmax
			tempo_inicial_para_amostragem = 9.5e-3
			delay_inicial = 10e-6
			gravou_resultado = 0
			contadorA = 0
			contadorB = 0
			contadorC = 0
			contadorD = 0
			subindoA = 1
			subindoB = 1
			subindoC = 1
			subindoD = 1
			delta_V = (vmax - vmin)

			varcont1 = 0
			while m.inFile3.readline(varcont1) != EOF:
				varlinha1 = m.inFile3.readline(varcont1)
				varcont1 += 1
				time = varlinha1[0]
				VoutA = varlinha1[1]
				VoutB = varlinha1[2]
				VoutC = varlinha1[3]
				VoutD = varlinha1[4]

				if time >= delay_inicial + m.numero_de_spots_varridos * 10 * 1e-3 :
					if VoutA >= vmax and subindoA == 1 :
						subindoA = 0
						contadorA += 1

					if VoutB >= vmax and subindoB == 1 :
						subindoB = 0
						contadorB += 1

					if VoutC >= vmax and subindoC == 1 :
						subindoC = 0
						contadorC += 1

					if VoutD >= vmax and subindoD == 1 :
						subindoD = 0
						contadorD += 1

					#Verifica se chegou ao mínimo do valor de comparação na descida

					if VoutA <= vmin and subindoA == 0 :
						subindoA = 1
						contadorA += 1

					if VoutB <= vmin and subindoB == 0 :
						subindoB = 1
						contadorB += 1

					if VoutC <= vmin and subindoC == 0 :
						subindoC = 1
						contadorC += 1

					if VoutD <= vmin and subindoD == 0 :
						subindoD = 1
						contadorD += 1

				if time >= tempo_inicial_para_amostragem + m.numero_de_spots_varridos * 10 * 1e-3 and gravou_resultado == 0 :
					#FAZ A RECONSTRUÇÃO PELO MÉTODO RICOCHETE
					if contadorA % 2 == 1 :
						m.As = delta_V * contadorA + (vmax - VoutA)
					else :
						m.As = delta_V * contadorA + (VoutA - vmin)

					if contadorB % 2 == 1 :
						m.Bs = delta_V * contadorB + (vmax - VoutB)
					else :
						m.Bs = delta_V * contadorB + (VoutB - vmin)

					if contadorC % 2 == 1 :
						m.Cs = delta_V * contadorC + (vmax - VoutC)
					else :
						m.Cs = delta_V * contadorC + (VoutC - vmin)

					if contadorD % 2 == 1 :
						m.Ds = delta_V * contadorD + (vmax - VoutD)
					else :
						m.Ds = delta_V * contadorD + (VoutD - vmin)

					diff = diff1
					gravou_resultado = 1

					SetLogToStdOut("\ntime\n")
					SetLogToStdOut("VoutA:\t", float(VoutA), "    \tAs:\t", float(m.As), "    \tcontadorA:\t", contadorA)
					SetLogToStdOut("VoutB:\t", float(VoutB), "    \tBs:\t", float(m.Bs), "    \tcontadorB:\t", contadorB)
					SetLogToStdOut("VoutC:\t", float(VoutC), "    \tCs:\t", float(m.Cs), "    \tcontadorC:\t", contadorC)
					SetLogToStdOut("VoutD:\t", float(VoutD), "    \tDs:\t", float(m.Ds), "    \tcontadorD:\t", contadorD)
					SetLogToStdOut("\n \n")

					SetLogToStdOut("numero_de_spots_varridos:  ", (m.numero_de_spots_varridos + 1))
					SetLogToStdOut("CAPTURADO NO TEMPO:  ", (9.5e-3 + m.numero_de_spots_varridos * 10 * 1e-3))

			m.inFile3.close()

def qcell(xc, yc):
	#print("qc_analysis::qcell")

	tp = 0.0
	ix = 0
	iy = 0
	h = 0
	ints = [[0.0] * 5] * 5
	ints_inner = [[0.0] * 5] * 5
	x = 0.0
	y = 0.0
	xc1 = 0.0
	yc1 = 0.0

	xc1 = xc
	yc1 = yc
	for h in numpy.arange(1,5,1):
		for k in numpy.arange(1,5,1):
			ints[h][k] = 0.0
			ints_inner[h][k] = 0.0
	for k in numpy.arange(0,2,1):
		for h in numpy.arange(0,2,1):
			for ix in numpy.arange(0,m.stepp + 1,1):
				for iy in numpy.arange(0,m.stepp + 1,1):
					#print(k, h, ix, iy)
					if m.flag_formato_QC == 0 :
						x = -(1 + m.G) + h * (1 + 2 * m.G) + (ix * (1.0 / m.stepp))
						y = -(1 + m.G) + k * (1 + 2 * m.G) + (iy * (1.0 / m.stepp))
						if m.radius == 0 or math.sqrt(math.pow((x - xc1),2) + math.pow((y - yc1),2)) == 0 :
							tp = 0.0
						else :
							tp = (math.sin((1 / m.radius) * math.sqrt(math.pow((x - xc1),2) + math.pow((y - yc1),2)))) / ((1 / m.radius) * math.sqrt(math.pow((x - xc1),2) + math.pow((y - yc1),2)))
						tp = math.pow(tp,2)
						#print(tp)
					elif m.flag_formato_QC == 1 :
						x = -1 + h + (ix * (1 / m.stepp))
						y = -1 + k + (iy * (1 / m.stepp))
						ints[h + 1][k + 1] +=  math.pow(math.exp((math.pow((x - xc1),2) + math.pow((y - yc1),2) ) / math.pow(m.radius,2)), -1)
						if (m.radius * m.radius) == 0 or ((x - xc1) * (y - yc1) * m.PI * m.PI) == 0 :
							tp = 0.0
						else :
							tp = (math.sin((x - xc1) * m.PI / m.radius) * math.sin((y - yc1) * m.PI / m.radius)) / (((x - xc1) * (y - yc1) * m.PI * m.PI) / (m.radius * m.radius))

					if (math.pow(x,2) + math.pow(y,2)) <= math.pow(m.radius_inner,2):
						ints_inner[h + 1][k + 1] += tp
					else :
						if m.flag_formato_QC == 1 :
							if (math.pow(x,2) + math.pow(y,2)) <= math.pow(m.cell_qc,2):
								ints[h + 1][k + 1] += tp
						if (math.pow(x,2) + math.pow(y,2)) <= 1 :
							#print(math.pow(x,2) + math.pow(y,2))
							ints[h + 1][k + 1] += tp
							print(ints[h + 1][k + 1])						
					tp = 0.0

	print(ints)

	global Aq					
	m.Aq = 0.0
	global Bq
	m.Bq = 0.0
	global Cq
	m.Cq = 0.0
	global Dq
	m.Dq = 0.0
	global Ac_inner
	m.Ac_inner = 0.0
	global Bc_inner
	m.Bc_inner = 0.0
	global Cc_inner
	m.Cc_inner = 0.0
	global Dc_inner
	m.Dc_inner = 0.0
	global Ac
	m.Ac = 0.0
	global Bc
	m.Bc = 0.0
	global Cc
	m.Cc = 0.0
	global Dc
	m.Dc = 0.0
	m.Ac = ints[1][2]
	m.Bc = ints[2][2]
	m.Cc = ints[2][1]
	m.Dc = ints[1][1]

	print(m.Ac, m.Bc, m.Cc, m.Dc)

	m.Ac_inner = ints_inner[1][2]
	m.Bc_inner = ints_inner[2][2]
	m.Cc_inner = ints_inner[2][1]
	m.Dc_inner = ints_inner[1][1]
	m.Ac *= m.QE
	m.Bc *= m.QE
	m.Cc *= m.QE
	m.Dc *= m.QE

	print(m.Ac, m.Bc, m.Cc, m.Dc)

	m.Ac_inner *= m.QE_inner
	m.Bc_inner *= m.QE_inner
	m.Cc_inner *= m.QE_inner
	m.Dc_inner *= m.QE_inner
	m.Ac += m.Ac_inner
	m.Bc += m.Bc_inner
	m.Cc += m.Cc_inner
	m.Dc += m.Dc_inner

	print(m.Ac, m.Bc, m.Cc, m.Dc)

	m.Aq = m.Ac
	m.Bq = m.Bc
	m.Cq = m.Cc
	m.Dq = m.Dc

	global cnst
	global grava_arquivos
	global flag_V_QC

	#tp/TP = porcentagem da contribuição do spot em ralação ao máx(centro do spot)
	if m.smooth == 0 :
		
		if (m.hplk_c0_e * m.TP) == 0 :
			m.cnst = 0
		else :
			m.cnst = ((m.TPS / (m.n_ml * m.n_ml)) * m.lamb) / (m.hplk_c0_e * m.TP) #Número de fótons efeticos
		if m.flag_spice == 1 :
			m.Ac *= m.TPS / (m.n_ml * m.n_ml * m.TP) #W
			m.Bc *= m.TPS / (m.n_ml * m.n_ml * m.TP)
			m.Cc *= m.TPS / (m.n_ml * m.n_ml * m.TP)
			m.Dc *= m.TPS / (m.n_ml * m.n_ml * m.TP)
			m.Ac *= 1 / (math.pow(m.cell_qc * 1e-6,2)) #W/(m^2)
			m.Bc *= 1 / (math.pow(m.cell_qc * 1e-6,2))
			m.Cc *= 1 / (math.pow(m.cell_qc * 1e-6,2))
			m.Dc *= 1 / (math.pow(m.cell_qc * 1e-6,2))
			#m.Ac *= 1 / (m.lamb * 1e6); #Adequação da irradiância para a unidade W/m2micm conforme necessário no SPICE
			#m.Bc *= 1 / (m.lamb * 1e6);
			#m.Cc *= 1 / (m.lamb * 1e6);
			#m.Dc *= 1 / (m.lamb * 1e6);
			
			m.grava_arquivos = 1
			
			m.flag_V_QC = 0
			grava_le_arquivos(0)
			m.flag_V_QC = 1
			m.grava_arquivos = 0
			m.Aq *= m.cnst * 1e9
			m.Bq *= m.cnst * 1e9
			m.Cq *= m.cnst * 1e9
			m.Dq *= m.cnst * 1e9
		else :
			m.Aq *= m.cnst * 1e9
			m.Bq *= m.cnst * 1e9
			m.Cq *= m.cnst * 1e9
			m.Dq *= m.cnst * 1e9

def aprox_respQC(outx, outy, cell_qc):
	print("qc_analysis::aprox_respQC")
	global dXq
	global dYq

	if m.flag_poli_resp_QC == 0 :
		if m.flag_formato_QC == 0 and m.flag_QEff == 0 :
			m.dXq[m.a][m.b] = 0.18313 * math.log(((-0.89 - 0.89) / (outx - 0.89)) - 1) * (cell_qc)
			m.dYq[m.a][m.b] = 0.18313 * math.log(((-0.89 - 0.89) / (outy - 0.89)) - 1) * (cell_qc)

		if m.flag_formato_QC == 0 and m.flag_QEff == 1 :
			m.dXq[m.a][m.b] = 0.22239 * math.log(((-0.92 - 0.92) / (outx - 0.92)) - 1) * (cell_qc)
			m.dYq[m.a][m.b] = 0.22239 * math.log(((-0.92 - 0.92) / (outy - 0.92)) - 1) * (cell_qc)

		if m.flag_formato_QC == 1 and m.flag_QEff == 0 :
			m.dXq[m.a][m.b] = 0.21201 * math.log(((-0.9 - 0.9) / (outx - 0.9)) - 1) * (cell_qc)
			m.dYq[m.a][m.b] = 0.21201 * math.log(((-0.9 - 0.9) / (outy - 0.9)) - 1) * (cell_qc)

		if m.flag_formato_QC == 1 and m.flag_QEff == 1 :
			m.dXq[m.a][m.b] = 0.21602 * math.log(((-0.88 - 0.88) / (outx - 0.88)) - 1) * (cell_qc)
			m.dYq[m.a][m.b] = 0.21602 * math.log(((-0.88 - 0.88) / (outy - 0.88)) - 1) * (cell_qc)

	else :
		if m.flag_formato_QC == 0 and m.flag_QEff == 0 :
			m.dXq[m.a][m.b] = (0.48991 * outx - 1.64947 * math.pow(outx,3) + 10.80716 * math.pow(outx,5) - 23.43905 * math.pow(outx,7) + 17.27537 * math.pow(outx,9)) * (cell_qc)
			m.dYq[m.a][m.b] = (0.48991 * outy - 1.64947 * math.pow(outy,3) + 10.80716 * math.pow(outy,5) - 23.43905 * math.pow(outy,7) + 17.27537 * math.pow(outy,9)) * (cell_qc)

		if m.flag_formato_QC == 0 and m.flag_QEff == 1 :
			m.dXq[m.a][m.b] = (0.53904 * outx - 1.78851 * math.pow(outx,3) + 11.78661 * math.pow(outx,5) - 25.82779 * math.pow(outx,7) + 19.14151 * math.pow(outx,9)) * (cell_qc)
			m.dYq[m.a][m.b] = (0.53904 * outy - 1.78851 * math.pow(outy,3) + 11.78661 * math.pow(outy,5) - 25.82779 * math.pow(outy,7) + 19.14151 * math.pow(outy,9)) * (cell_qc)

		if m.flag_formato_QC == 1 and m.flag_QEff == 0 :
			m.dXq[m.a][m.b] = (0.51819 * outx - 1.55151 * math.pow(outx,3) + 10.64861 * math.pow(outx,5) - 23.71723 * math.pow(outx,7) + 18.07311 * math.pow(outx,9)) * (cell_qc)
			m.dYq[m.a][m.b] = (0.51819 * outy - 1.55151 * math.pow(outy,3) + 10.64861 * math.pow(outy,5) - 23.71723 * math.pow(outy,7) + 18.07311 * math.pow(outy,9)) * (cell_qc)

		if m.flag_formato_QC == 1 and m.flag_QEff == 1 :
			m.dXq[m.a][m.b] = (0.54332 * outx - 1.14376 * math.pow(outx,3) + 8.18487 * math.pow(outx,5) - 18.3305 * math.pow(outx,7) + 14.12322 * math.pow(outx,9)) * (cell_qc)
			m.dYq[m.a][m.b] = (0.54332 * outy - 1.14376 * math.pow(outy,3) + 8.18487 * math.pow(outy,5) - 18.3305 * math.pow(outy,7) + 14.12322 * math.pow(outy,9)) * (cell_qc)

def saida_XQC_YQC():
	print("qc_analysis::saida_XQC_YQC")

	global TimeSpiceclk
	global T_on
	global TimeSpice
	global outx
	global outy

	cont = 0
	outxsp = 0.0
	outysp = 0.0
	time = 0.0
	diff = 10.0
	diff1 = 0.0
	TSpice_amostra = 0.0
	T_inc = 0.0

	if m.flag_spice == 0 :
		
		m.TimeSpiceclk = m.TimeSpice + T_inc
		
		m.T_on = m.TimeSpiceclk + m.TimeSpice_int * m.Int_on
		
		m.TimeSpice += m.TimeSpice_int + m.T_inc

	T_inc = m.TimeSpice_int * 1e-7
	TSpice_amostra = (m.TimeSpice_int * m.Int_on * Int_amostra) * 1e-3
	TSpice_amostra += m.T_on * 1e-3

	in_saidaXqc = open("saidaXqc.txt", "r")
	in_saidaYqc = open("saidaYqc.txt", "r")

	if in_saidaXqc == None :
		print("Unable to open spice input, saidaXqc.txt")
		os.system("PAUSE")
		exit(1)
	if in_saidaYqc == None :
		print("Unable to open spice input, saidaYqc.txt")
		os.system("PAUSE")
		exit(1)
	varcont1 = 0
	cont = in_saidaYqc.read(varcont1)
	while cont != EOF:
		varlinha1 = m.in_saidaXqc.readline(varcont1)
		time = varlinha1[0]
		outxsp = varlinha1[1]
		varlinha2 = m.in_saidaYqc.readline(varcont1)
		time = varlinha1[0]
		outysp = varlinha1[1]
		varcont1 += 1
		cont = in_saidaYqc.read(varcont1)#Lógica implementada por Victor Lopes Dias Ferreira

		diff1 = math.fabs(time - TSpice_amostra)
		if diff1 < diff :	
			m.outx = m.outxsp
			m.outx -= m.outx_cal[m.a][m.b]
			m.outy = m.outysp
			m.outy -= m.outy_cal[m.a][m.b]
			diff = diff1
			
	print("TSpice_amostra=", float(TSpice_amostra), " [outx][outy]=[", float(m.outx), "][", float(m.outy), "]")
	in_saidaXqc.close()
	in_saidaYqc.close()

def fix_saida_qc():#EM DESENVOLVIMENTO
	pass

def CleanString(IN, nummer):#EM DESENVOLVIMENTO
	pass

def random_tanner_noise(vo):
	print("qc_analysis::random_tanner_noise")

	random.seed()#Inicializa o gerador de números aleatórios
	x = 0
	resolution = 0
	noise_rms = 0.0
	vfinal = 0.0
	noise_component = 0.0

	#VALOR RMS DO RUÍDO
	if i.noise_noiseless == "noise" :
		noise_rms = 901.90721e-6
	elif i.noise_noiseless == "noiseless" :
		noise_rms = 0.0
	resolution = 1024

	x = random.getstate() % resolution
	noise_component = double(x)
	noise_component = noise_component / resolution * noise_rms
	vfinal = vo[0] - noise_rms / 2 + noise_component
	vo[0] = vfinal

def gaussian_noise(vo):
	ruido_rms = 0.0
	vfinal = 0.0
	componente_de_ruido = 0.0
	variavel_aleatoria = 0.0
	sigma = 0.0

	#VALOR RMS DO RUÍDO
	if i.noise_noiseless == "noise" :
		ruido_rms = 901.90721e-6
	elif i.noise_noiseless == "noiseless" :
		ruido_rms = 0.0
	sigma = 1.0
	variavel_aleatoria = p.gasdev(iseed)
	componente_de_ruido = variavel_aleatoria * (ruido_rms / 2) / (2 * sigma)
	vfinal = vo[0] + componente_de_ruido
	vo[0] = vfinal