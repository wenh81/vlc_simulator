#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#main.py

import math
import random
import time
import numpy

import experimental as e
import interface as i
import poisson as p
import qc_analysis as q
import reconstruction as r
import sampling as s
import ZERNIKE as Z

import os
import sys

###Início cabeçalho
PI = 3.14159265358979323844
Kb = 1.38066e-23
hplk = 6.62608e-34
c0 = 2.99792458e8
hplk_c0 = 1.9864488101e-25
hplk_c0_e = 1.2398435442e-6
ele = 1.602177e-19
N = 10

##Flags e controle (fixos)
rot_flag = 0
nonlin = 0
turb_flag = 0
iseed = []
print_ctrl = 0
smooth = 0
grava_arquivos = 0
flag_V_QC = 0

##Flags e controle (variáveis)
matriz_ortogonal = 0
flag_amostragem = 0
flag_experimental = 0
flag_interferencia = 0
flag_linear_resp_QC = 0
flag_sigm_auto_resp_QC = 0
flag_poli_resp_QC = 0
flag_spice = 0
flag_XQC_YQC = 0
flag_Vout_QC = 0
flag_grava_outx_spice = 0
flag_defocus = 0
oxtl_flag = 0
flag_ruido = 0

##Variáveis para tratamento de fentes de onda
c = [[0.0] * 12] * 12
dX = [[0.0] * N] * N
dY = [[0.0] * N] * N
dXg = [[0.0] * N] * N
dYg = [[0.0] * N] * N
dXqg = [[0.0] * N] * N
dYqg = [[0.0] * N] * N
Xr = [[0.0] * N] * N
Yr = [[0.0] * N] * N
dXq = [[0.0] * N] * N
dYq = [[0.0] * N] * N
outx_cal = [[0.0] * N] * N
outy_cal = [[0.0] * N] * N
dXql = [[0.0] * N] * N
dYql = [[0.0] * N] * N
dWx = [[0.0] * N] * N
dWy = [[0.0] * N] * N
Wf1 = [[0.0] * N] * N
W = 0.0
Wrms = 0.0
delta = 0.0
yb = 0.0
x_edge = 0.0
z_basis = [0.0]
coeff = [0.0]
nz = [0]
mz = [0]
nn = 0
a = 0
b = 0
a1 = 0
b1 = 0
theta = 0.0
jx = 0.0
jy = 0.0
ma = 0.0
xx = 0.0
outx_l = 0.0

##Sensor óptico
outx = 0.0
outy = 0.0
Aq = 0.0
Bq = 0.0
Cq = 0.0
Dq = 0.0
Ac_inner = 0.0
Bc_inner = 0.0
Cc_inner = 0.0
Dc_inner = 0.0
Ac = 0.0
Bc = 0.0
Cc = 0.0
Dc = 0.0
cell_qc = 0.0
area_Ph = 0.0
G = 0.0
As = 0.0
Bs = 0.0
Cs = 0.0
Ds = 0.0
QE = 0.0
QE_inner = 0.0
radius_inner = 0.0
stepp = 0
slope = 0.0
coefabs = 0.0
reflect = 0.0
slope_ex = 0.0

##Dados experimentais
slope_exp = 0.0
aux_exp = 0
Asref = 0.0
Bsref = 0.0
Csref = 0.0
Dsref = 0.0

##Setup óptico
TPS = 0.0
lamb = 0.0
f = 0.0
rad = 0.0

##Configurações de microlentes
max_order = 0
ml_dimen = 0
mlq_dimen = 0
n_ml = 0
dimens = 0
n_spots = 0
step = 0
dist = 0.0
coinc = 0.0
radius = 0.0
TP = 0.0

##Variáveis auxiliares
cnst = 0.0
sto = 0.0
xpp = 0.0
ypp = 0.0
aa = 0
bb = 0
rodaSpice  = 0

##Variáveis Spice
TimeSpice = 0.0
TimeSpice_int = 0.0
TimeSpice2i = 0.0
TimeSpiceclk = 0.0
Int_amostra = 0.0
Int_on = 0.0
T_on = 0.0
T_off = 0.0
Dn = 0.0
Dp = 0.0
Ln = 0.0
Lp = 0.0
Wb = 0.0
We = 0.0
Sb = 0.0
Se = 0.0
Cj = 0.0
Rs = 0.0
Rp = 0.0

##Variáveis estudo de ruído
Rin = 0.0
Rfed = 0.0
Amplf = 0.0
NLmed = 0.0
NLrms = 0.0
np0 = 0

##Inicialização de arquivos
tc = time.time()
inFile = open
in_saidaXqc = open
in_saidaYqc = open
inFile3 = open
out_wf_original = open
out_wf_reconstsem = open
out_wf_reconstcom = open
out_wrms = open
out_deslocamentos = open
out_irradianciaA = open
out_irradianciaB = open
out_irradianciaC = open
out_irradianciaD = open
out_clock = open
out_area = open
out_comprimentoonda = open
out_coefabs = open
out_reflectancia = open
out_Ln = open
out_Lp = open
out_Wb = open
out_We = open
out_Sb = open
out_Se = open
out_Dn = open
out_Dp = open
out_Cj = open
out_Rs = open
out_Rp = open
outFile_CorrenteA = open
outFile_CorrenteB = open
outFile_CorrenteC = open
outFile_CorrenteD = open
outFilespiceX = open
outFilespiceY = open
inFile50 = open
inFile51 = open
outFileInterface = open

##Flags adicionais - Adcionados na versão do código em python
flag_formato_QC = 0
flag_QEff = 0

###SETUP
numero_de_spots_varridos = 0

##Flags e controle (fixos)
rot_flag = 0
nonlin = 0
turb_flag = 1
print_ctrl = 0
smooth = 0
grava_arquivos = 0
flag_V_QC = 1

##Flags e controle (variáveis)
matriz_ortogonal = 1
flag_amostragem = 0
flag_experimental = 0
flag_interferencia = 0
flag_linear_resp_QC = 1
flag_sigm_auto_resp_QC = 0
flag_poli_resp_QC = 0
flag_spice = 1
flag_XQC_YQC = 0
flag_Vout_QC = 0
flag_grava_outx_spice = 0
flag_defocus = 0 #Não definido no código original nesta sessão.
oxtl_flag = 0 #Não definido no código original nesta sessão.
flag_ruido = 1

##Variáveis para tratamento de fentes de onda
Wrms = 0.0
yb = 0.0
theta = 0.0
xx = 0.0
outx_l = 0.0

##Sensor óptico
Aq = 0.0
Bq = 0.0
Cq = 0.0
Dq = 0.0
Ac_inner = 0.0
Bc_inner = 0.0
Cc_inner = 0.0
Dc_inner = 0.0
Ac = 0.0
Bc = 0.0
Cc = 0.0
Dc = 0.0
stepp = 20.0
slope = 0.0

##Dados experimentais
aux_exp = 1

##Setup óptico
TPS = 1e-4
lamb = 633e-9

##Configurações de microlentes
TP = 0.0

##Variáveis auxiliares
sto = 0.0
rodaSpice  = 0

##Variáveis Spice
TimeSpiceclk = 0.0

##Variáveis estudo de ruído
Rfed = 1e6
Amplf = 1e2
NLmed = 0.0
NLrms = 0.0
np0 = 0

##Flags adicionais - Adcionados na versão do código em python
flag_formato_QC = 0 #Se 0, utiliza QC circular. Se 1, utiliza QC quadrada.
flag_QEff = 0 #Se 0, utiliza QC do tipo homogênea. Se 1, utiliza QC de dupla eficiência quântica.
###Fim do SETUP

###Fim Cabeçalho

def main():

	import auxiliar #Para prevenir import circular.
	print("main")

	##Flags e controle (fixos)
	global rot_flag
	global nonlin
	global turb_flag
	global iseed
	global print_ctrl
	global smooth
	global grava_arquivos
	global flag_V_QC

	##Flags e controle (variáveis)
	global matriz_ortogonal
	global flag_amostragem
	global flag_experimental
	global flag_interferencia
	global flag_linear_resp_QC
	global flag_sigm_auto_resp_QC
	global flag_poli_resp_QC
	global flag_spice
	global flag_XQC_YQC
	global flag_Vout_QC
	global flag_grava_outx_spice
	global flag_defocus
	global oxtl_flag
	global flag_ruido

	##Variáveis para tratamento de fentes de onda
	global c
	global dX
	global dY
	global dXg
	global dYg
	global dXqg
	global dYqg
	global Xr
	global Yr
	global dXq
	global dYq
	global outx_cal
	global outy_cal
	global dXql
	global dYql
	global dWx
	global dWy
	global Wf1
	global W
	global Wrms
	global delta
	global yb
	global x_edge
	global z_basis
	global coeff
	global nz
	global mz
	global nn
	global a
	global b
	global a1
	global b1
	global theta
	global jx
	global jy
	global ma
	global xx
	global outx_l

	##Sensor óptico
	global outx
	global outy
	global Aq
	global Bq
	global Cq
	global Dq
	global Ac_inner
	global Bc_inner
	global Cc_inner
	global Dc_inner
	global Ac
	global Bc
	global Cc
	global Dc
	global cell_qc
	global area_Ph
	global G
	global As
	global Bs
	global Cs
	global Ds
	global QE
	global QE_inner
	global radius_inner
	global stepp
	global slope
	global coefabs
	global reflect
	global slope_ex

	##Dados experimentais
	global slope_exp
	global aux_exp
	global Asref
	global Bsref
	global Csref
	global Dsref

	##Setup óptico
	global TPS
	global lamb
	global f
	global rad

	##Configurações de microlentes
	global max_order
	global ml_dimen
	global mlq_dimen
	global n_ml
	global dimens
	global n_spots
	global step
	global dist
	global coinc
	global radius
	global TP

	##Variáveis auxiliares
	global cnst
	global sto
	global xpp
	global ypp
	global aa
	global bb
	global rodaSpice 

	##Variáveis Spice
	global TimeSpice
	global TimeSpice_int
	global TimeSpice2i
	global TimeSpiceclk
	global Int_amostra
	global Int_on
	global T_on
	global T_off
	global Dn
	global Dp
	global Ln
	global Lp
	global Wb
	global We
	global Sb
	global Se
	global Cj
	global Rs
	global Rp

	##Variáveis estudo de ruído
	global Rin
	global Rfed
	global Amplf
	global NLmed
	global NLrms
	global np0

	##Inicialização de arquivos
	global tc
	global inFile
	global in_saidaXqc
	global in_saidaYqc
	global inFile3
	global out_wf_original
	global out_wf_reconstsem
	global out_wf_reconstcom
	global out_wrms
	global out_deslocamentos
	global out_irradianciaA
	global out_irradianciaB
	global out_irradianciaC
	global out_irradianciaD
	global out_clock
	global out_area
	global out_comprimentoonda
	global out_coefabs
	global out_reflectancia
	global out_Ln
	global out_Lp
	global out_Wb
	global out_We
	global out_Sb
	global out_Se
	global out_Dn
	global out_Dp
	global out_Cj
	global out_Rs
	global out_Rp
	global outFile_CorrenteA
	global outFile_CorrenteB
	global outFile_CorrenteC
	global outFile_CorrenteD
	global outFilespiceX
	global outFilespiceY
	global inFile50
	global inFile51
	global outFileInterface

	##Flags adicionais - Adcionados na versão do código em python
	global flag_formato_QC
	global flag_QEff

	#
	#Código comentado no arquivo C
	#
	

	i.read_from_interface()

	if i.with_without == "with" :
		flag_Vout_QC = 1
	elif i.with_without == "without" :
		flag_Vout_QC = 0

	lamb = i.wave * 1e-6

	if i.defocus == True :
		flag_defocus = 1
	else :
		flag_defocus = 0

	outFileInterface = open("interface.txt")

	if flag_Vout_QC == 1 :
		rodaSpice = 1
		flag_Vout_QC = 0

	print("@@@@@@@@@@@@@@@@@@@@@ Wavefront Sensor - OptMA Lab 2020 @@@@@@@@@@@@@@@@@@@@@@@@")
	print("Programa em execucao, aguarde. Se o programa demorar muito, feche e tente com novas configuracoes.")

	max_order = i.zernike

	random.seed(tc)
	iseed = [0] * 5000
	nz = [0] * max_order * 4
	mz = [0] * max_order * 4
	iseed = -random.randint(-2147483,2147483) #(-2147483648‬,21474836487) % 1000
	
	#Definições de valores microlentes
	ml_dimen = i.diameter
	n_ml = math.sqrt(i.quantity)
	n_spots = n_ml * n_ml
	dimens = (n_ml * ml_dimen) / 2
	mlq_dimen = dimens * 2 / n_ml
	rad = dimens * math.sqrt(2)
	s.zern_ind(max_order)
	Wrms = 0.0
	theta *= PI / 180
	step = 100
	delta = 50.0
	radius = i.eff

	#Definições de valores sensor óptico
	cell_qc = i.cell
	radius_inner = i.cent
	area_Ph = PI * cell_qc * cell_qc / (4 * 100000000)
	G = 0.025
	QE = i.quant
	QE_inner = 1.0
	coefabs = i.coefabs
	reflect = i.reflec
	f = radius * PI * 2 * cell_qc * ml_dimen / (2.44 * lamb * math.pow(10, 6))
	
	#Definições de valores experimentais
	slope_exp = 1.85

	#Definições de valores spice
	TimeSpice = 0
	TimeSpice_int = 10
	TimeSpice2i = 0
	Int_on = 0.1
	Int_amostra = 0.5
	Ln = i.lanode
	Lp = i.lcathode
	Dn = i.canode
	Dp = i.ccathode
	Wb = i.bthick
	We = i.ethick
	Sb = i.rcathode
	Se = i.ranode
	Cj = i.capac
	Rs = i.sres
	Rp = i.pres

	out_wf_original = open("WF_original.txt", "w")
	if out_wf_original == None :
		print("Unable to open WF_original.txt")
		exit(1)

	out_wf_reconstsem = open("WF_reconst_sem_spice.txt", "w")
	if out_wf_reconstsem == None :
		print("Unable to open WF_reconst_sem_spice.txt")
		exit(1)

	out_wrms = open("Wrms.txt","w")
	if out_wrms == None :
		print("Unable to open Wrms.txt")
		exit(1)

	out_deslocamentos = open("Deslocamentos.txt","w")
	if out_deslocamentos == None :
		print("Unable to open Deslocamentos.txt")
		exit(1)

	if flag_spice == 1 :
		out_irradianciaA = open("irradiancia_A.txt", "w")
		if out_irradianciaA == None :
			print("Unable to open irradiancia_A.txt")
			exit(1)

		out_irradianciaB = open("irradiancia_B.txt", "w")
		if out_irradianciaB == None :
			print("Unable to open irradiancia_B.txt")
			exit(1)

		out_irradianciaC = open("irradiancia_C.txt", "w")
		if out_irradianciaC == None :
			print("Unable to open irradiancia_C.txt")
			exit(1)

		out_irradianciaD = open("irradiancia_D.txt", "w")
		if out_irradianciaD == None :
			print("Unable to open irradiancia_D.txt")
			exit(1)

		out_clock = open("clock.txt", "w")
		if out_clock == None :
			print("Unable to open clock.txt")
			exit(1)

		out_area = open("area.txt", "w")
		if out_area == None :
			print("Unable to open area.txt")
			exit(1)

		out_comprimentoonda = open("comprimento_onda.txt", "w")
		if out_comprimentoonda == None :
			print("Unable to open comprimento_onda.txt")
			exit(1)

		out_coefabs = open("coeficiente_absorcao.txt", "w")
		if out_coefabs == None :
			print("Unable to open coeficiente_absorcao.txt")
			exit(1)

		out_reflectancia = open("reflectancia.txt", "w")
		if out_reflectancia == None :
			print("Unable to open reflectancia.txt")
			exit(1)

		out_Ln = open("Ln.txt", "w")
		if out_Ln == None :
			print("Unable to open Ln.txt")
			exit(1)

		out_Lp = open("Lp.txt", "w")
		if out_Lp == None :
			print("Unable to open Lp.txt")
			exit(1)

		out_Wb = open("Wb.txt", "w")
		if out_Wb == None :
			print("Unable to open Wb.txt")
			exit(1)

		out_We = open("We.txt", "w")
		if out_We == None :
			print("Unable to open We.txt")
			exit(1)

		out_Sb = open("Sb.txt", "w")
		if out_Sb == None :
			print("Unable to open Sb.txt")
			exit(1)

		out_Se = open("Se.txt", "w")
		if out_Se == None :
			print("Unable to open Se.txt")
			exit(1)

		out_Dn = open("Dn.txt", "w")
		if out_Dn == None :
			print("Unable to open Dn.txt")
			exit(1)

		out_Dp = open("Dp.txt", "w")
		if out_Dp == None :
			print("Unable to open Dp.txt")
			exit(1)

		out_Cj = open("Cj.txt", "w")
		if out_Cj == None :
			print("Unable to open Cj.txt")
			exit(1)

		out_Rs = open("Rs.txt", "w")
		if out_Rs == None :
			print("Unable to open Rs.txt")
			exit(1)

		out_Rp = open("Rp.txt", "w")
		if out_Rp == None :
			print("Unable to open Rp.txt")
			exit(1)

		outFile_CorrenteA = open("corrente_A.txt", "w")
		if outFile_CorrenteA == None :
			print("Unable to open corrente_A.txt")
			exit(1)

		outFile_CorrenteB = open("corrente_B.txt", "w")
		if outFile_CorrenteB == None :
			print("Unable to open corrente_B.txt")
			exit(1)

		outFile_CorrenteC = open("corrente_C.txt", "w")
		if outFile_CorrenteC == None :
			print("Unable to open corrente_C.txt")
			exit(1)

		outFile_CorrenteD = open("corrente_D.txt", "w")
		if outFile_CorrenteD == None :
			print("Unable to open corrente_D.txt")
			exit(1)

		lamb1 = 0.0
		lamb1 = lamb * 1000000
		print(float(TimeSpice + 1), "e-003\t", float(area_Ph), "\n", file = out_area)
		print(float(TimeSpice + 1), "e-003\t", float(lamb1), "\n", file = out_comprimentoonda)
		print(float(TimeSpice + 1), "e-003\t", float(coefabs), "\n", file = out_coefabs)
		print(float(TimeSpice + 1), "e-003\t", float(reflect), "\n", file = out_reflectancia)
		print(float(TimeSpice + 1), "e-003\t", float(Ln), "\n", file = out_Ln)
		print(float(TimeSpice + 1), "e-003\t", float(Lp), "\n", file = out_Lp)
		print(float(TimeSpice + 1), "e-003\t", float(Wb), "\n", file = out_Wb)
		print(float(TimeSpice + 1), "e-003\t", float(We), "\n", file = out_We)
		print(float(TimeSpice + 1), "e-003\t", float(Sb), "\n", file = out_Sb)
		print(float(TimeSpice + 1), "e-003\t", float(Se), "\n", file = out_Se)
		print(float(TimeSpice + 1), "e-003\t", float(Dn), "\n", file = out_Dn)
		print(float(TimeSpice + 1), "e-003\t", float(Dp), "\n", file = out_Dp)
		print(float(TimeSpice + 1), "e-003\t", float(Cj), "e-12\n", file = out_Cj)
		print(float(TimeSpice + 1), "e-003\t", float(Rs), "\n", file = out_Rs)
		print(float(TimeSpice + 1), "e-003\t", float(Rp), "\n", file = out_Rp)

		if flag_grava_outx_spice == 1 :
			if flag_amostragem == 0 :
				outFilespiceX = open("saidaXqc.txt", "w")
				if outFilespiceX == None :
					print("Unable to open saidaXqc.txt")
					exit(1)

				radius_inner /= cell_qc

				outFilespiceY = open("saidaYqc.txt", "w")
				if outFilespiceY == None :
					print("Unable to open saidaYqc.txt")
					exit(1)

	for a in range(0,int(n_ml), 1):
		for b in range(0,int(n_ml), 1):
			Xr[int(a)][int(b)] = 0.0
			Yr[int(a)][int(b)] = 0.0

	#DETERMINAÇÃO DA COORDENADA DO CENTRO DE CADA MICROLENTE
	#Cojunto de rotinas para distribuição ortogonal de microlentes
	if matriz_ortogonal == 1 :
		for a in range(0,int(n_ml),1):
			for b in range(0,int(n_ml),1):
				Xr[int(a)][int(b)] = (-dimens + (mlq_dimen / 2)) + a * mlq_dimen
				Yr[int(a)][int(b)] = (-dimens + (mlq_dimen / 2)) + b * mlq_dimen

	print(Xr)
	print(Yr)

	STOP_HERE
	
	#Conjunto de rotinas para distribuição aleatória de microlentes
	if matriz_ortogonal == 0 :
		inFile = open("Otimizacao\\Graficos\\posicoes.txt", "r")
		if inFile == None :
			print("Unable to open posicoes.txt")
			exit(1)

		cont = 0
		xrr = 0.0
		yrr = 0.0
		a = 0
		b = 0

		for cont in range(1,int(n_ml * n_ml) + 1,1):
			varlinhas = inFile.readlines(cont - 1)
			xrr = varlinhas[0]
			yrr = varlinhas[1]
			Xr[a][b] = xrr
			Yr[a][b] = yrr
			if b == (int(n_ml) - 1) :
				a += 1
				b = -1
			b += 1

		inFile.close()

	#Inicializa variáveis que serão usadas na amostragem e reconstrução da frente de onda.
	for a in range(0,int(n_ml),1):
		for b in range(0,int(n_ml),1):
			dWx[int(a)][int(b)] = 0.0
			dWy[int(a)][int(b)] = 0.0
			Wf1[int(a)][int(b)] = 0.0
			dX[int(a)][int(b)] = 0.0
			dY[int(a)][int(b)] = 0.0
			dX[int(a)][int(b)] = 0.0
			dXqg[int(a)][int(b)] = 0.0
			dYqg[int(a)][int(b)] = 0.0
			dXg[int(a)][int(b)] = 0.0
			dYg[int(a)][int(b)] = 0.0
			dXql[int(a)][int(b)] = 0.0
			dYql[int(a)][int(b)] = 0.0

	if flag_experimental == 0 :
		#Cálculo do fator de ponderação da potência de luz para cada microlente.
		theta *= PI / 180
		for xpp in numpy.arange(-2,2 + 1.0 / stepp,1.0 / stepp):
			for ypp in numpy.arange(-2,2 + 1.0 / stepp,1.0 / stepp):
				sto = (math.sin((1 / radius) * math.sqrt(math.pow(xpp, 2) + math.pow(ypp, 2)))) / ((1 / radius) * math.sqrt(math.pow(xpp, 2) + math.pow(ypp, 2)))
				sto = math.pow(sto, 2)
				TP += sto

	#Cálculo do slope da aproximação linear da resposta da QC.
	smooth = 1

	if flag_experimental == 1 :
		slope = slope_exp
	else :
		s.slope_QC()

	smooth = 0

	if flag_experimental == 0 :
		s.input_coeff()
		s.wfs_comput()

		a = 0
		b = 0

		for a in range(0,int(n_ml),1):
			for b in range(0,int(n_ml),1):
				if nn == 0 :
					Wf1[int(a)][int(b)] = 0
					dWx[int(a)][int(b)] = 0
					dWy[int(a)][int(b)] = 0
				else :
					Wf1[int(a)][int(b)] /= nn
					dWx[int(a)][int(b)] /= nn
					dWy[int(a)][int(b)] /= nn
				dX[int(a)][int(b)] = (f * dWx[int(a)][int(b)])
				dY[int(a)][int(b)] = (f * dWy[int(a)][int(b)])
				dXg[int(a)][int(b)] = dX[int(a)][int(b)] + Xr[int(a)][int(b)]
				dYg[int(a)][int(b)] = dY[int(a)][int(b)] + Yr[int(a)][int(b)]
				if rot_flag == 0 :
					dXqg[int(a)][int(b)] = dXg[int(a)][int(b)] * math.cos(theta) - dYg[int(a)][int(b)] * math.sin(theta)
					dYqg[int(a)][int(b)] = dXg[int(a)][int(b)] * math.sin(theta) + dYg[int(a)][int(b)] * math.cos(theta)
				else :
					dXqg[int(a)][int(b)] = (dXg[int(a)][int(b)] - 2 * math.sqrt(2) * dimens * math.sin(theta / 2) * math.sin(45 - theta / 2)) * math.cos(theta) - (dYg[int(a)][int(b)] - 2 * math.sqrt(2) * dimens * math.sin(theta / 2) * math.cos(45 - theta / 2)) * math.sin(theta)
					dYqg[int(a)][int(b)] = (dXg[int(a)][int(b)] - 2 * math.sqrt(2) * dimens * math.sin(theta / 2) * math.sin(45 - theta / 2)) * math.sin(theta) + (dYg[int(a)][int(b)] - 2 * math.sqrt(2) * dimens * math.sin(theta / 2) * math.cos(45 - theta / 2)) * math.cos(theta)
				dXql[int(a)][int(b)] = dXqg[int(a)][int(b)] - Xr[int(a)][int(b)]
				dYql[int(a)][int(b)] = dYqg[int(a)][int(b)] - Yr[int(a)][int(b)]

	for a in range(0,int(n_ml),1):
		for b in range(0,int(n_ml),1):
			print("Cell", int(a + 1), int(b + 1))
			if flag_experimental == 0 :
				if flag_amostragem == 1 :
					dXq[int(a)][int(b)] = dXql[int(a)][int(b)]
					dXq[int(a)][int(b)] = dXql[int(a)][int(b)]
				else :
					As = 0.0
					Bs = 0.0
					Cs = 0.0
					Ds = 0.0
					outx = 0.0
					outy = 0.0
					if flag_interferencia == 0 :
						q.qcell((dXql[int(a)][int(b)]) / (cell_qc), (dYql[int(a)][int(b)]) / (cell_qc))
					else :
						for aa in range(a - 1,a + 2,1):
							for bb in range(b - 1,b + 2,1):
								if (aa > -1) and (aa < n_ml) and (bb > -1) and (bb < n_ml) :
									if aa == a and bb == b :
										oxtl_flag = 0
									else :
										oxtl_flag = 1
									q.qcell((dXql[int(aa)][int(bb)] + (aa - a) * ml_dimen) / (cell_qc), (dYql[int(aa)][int(bb)] + (bb - b) * ml_dimen) / (cell_qc))

									if flag_XQC_YQC == 1 :
										q.saida_XQC_YQC()
									else :
										As += Aq
										Bs += Bq
										Cs += Cq
										Ds += Dq

										if (As + Bs + Cs + Ds) == 0 :
											outx = 0
											outy = 0
										else :
											outx = ((Bs + Cs) - (As + Ds)) / (As + Bs + Cs + Ds)
											outy = ((As + Bs) - (Cs + Ds)) / (As + Bs + Cs + Ds)
										outx -= outx_cal[int(a)][int(b)]
										outy -= outy_cal[int(a)][int(b)]

			if flag_experimental == 1 :
				Asref = Bsref = Csref = Dsref = 0.0
				As = Bs = Cs = Ds = outx = outy = 0.0
				e.le_experimental()
				if (As + Bs + Cs + Ds) == 0 :
					outx = 0
					outy = 0
				else :
					outx = ((Bs + Cs) - (As + Ds)) / (As + Bs + Cs + Ds)
					outy = ((As + Bs) - (Cs + Ds)) / (As + Bs + Cs + Ds)
				if (Asref + Bsref + Csref + Dsref) == 0 :
					outx -= 0
					outy -= 0
				else :
					outx -= ((Bsref + Csref) - (Asref + Dsref)) / (Asref + Bsref + Csref + Dsref)
					outy -= ((Asref + Bsref) - (Csref + Dsref)) / (Asref + Bsref + Csref + Dsref)

			Aq = Bq = Cq = Dq = 0.0
			if flag_linear_resp_QC == 1 :
				if slope == 0 :
					dXq[int(a)][int(b)] = 0
					dYq[int(a)][int(b)] = 0
				else :
					dXq[int(a)][int(b)] = ((outx - yb) / slope) * (cell_qc)
					dYq[int(a)][int(b)] = ((outy - yb) / slope) * (cell_qc)
			elif flag_sigm_auto_resp_QC == 1 :
				dXq[int(a)][int(b)] = 0.218 * math.log(-((2 /(outx - 1)) + 1)) * (cell_qc)
				dYq[int(a)][int(b)] = 0.218 * math.log(-((2 /(outy - 1)) + 1)) * (cell_qc)
			else :
				q.aprox_respQC(outx, outy, cell_qc)
			print(a, "\t", b, "\t", dXq[int(a)][int(b)],"\t", dYq[int(a)][int(b)], file = out_deslocamentos)

	print("", file = out_deslocamentos)

	r.reconst()
	print_ctrl = 1

	if flag_experimental == 0 :
		auxiliar.rms_calc()
	else :
		print("Erro RMS não calculado")

	if Wrms != Wrms :
		Wrms = 1000

	print(Wrms, file = out_wrms)

	print("\n Erro RMS sem spice = ", Wrms, "\n")
	outFileInterface = open("Wrms.txt","w")
	print(Wrms, file = outFileInterface)
	outFileInterface.close()

	nn = 0

	out_wf_original.close()
	out_wf_reconstsem.close()

	out_wrms.close()

	if flag_spice == 1 :
		if flag_amostragem == 0 :
			out_irradianciaA.close()
			out_irradianciaB.close()
			out_irradianciaC.close()
			out_irradianciaD.close()
			out_area.close()
			out_comprimentoonda.close()
			out_coefabs.close()
			out_reflectancia.close()
			out_clock.close()
			out_Ln.close()
			out_Lp.close()
			out_Wb.close()
			out_We.close()
			out_Sb.close()
			out_Se.close()
			out_Dn.close()
			out_Dp.close()
			out_Cj.close()
			out_Rs.close()
			out_Rp.close()
	if flag_grava_outx_spice == 1 :
		if flag_amostragem == 0 :
			outFilespiceX.close()
			outFilespiceY.close()

	out_deslocamentos.close()
	print("Sistema pausado!")
	#os.system("PAUSE")

	#EM DESENVOLVIMENTO

	return 0