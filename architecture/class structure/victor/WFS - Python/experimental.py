#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#experimental.py

import math

import main as m

def le_experimental():
	print("experimental::le_experimental")
	
	global inFile50
	global inFile51
	global As
	global Bs
	global Cs
	global Ds
	global aux_exp

	m.inFile50 = open("ExpF200_Or1_1_QCdupla_WFref_ABCD.txt", "r")
	if m.inFile50 == None :
		print("Unable to open ExpF200_Or1_1_QCdupla_WFref_ABCD.txt")
		exit(1)
	m.inFile51 = open("ExpF200_Or1_1_QCdupla_WFaberra_ABCD.txt", "r")
	if m.inFile51 == None :
		print("Unable to open ExpF200_Or1_1_QCdupla_WFaberra_ABCD.txt")
		exit(1)

	VAref = 0.0
	VBref = 0.0
	VCref = 0.0
	VDref = 0.0
	VA = 0.0
	VB = 0.0
	VC = 0.0
	VD = 0.0
	ulens = 0
	
	varcont1 = 0
	while m.inFile50.readline(varcont1) != EOF:
		varlinha1 = m.inFile50.readline(varcont1)
		varcont1 += 1
		m.ulens = varlinha1[0]
		m.VAref = varlinha1[1]
		m.VBref = varlinha1[2]
		m.VCref = varlinha1[3]
		m.VDref = varlinha1[4]
		if m.aux_exp == m.ulens:
			m.As = m.VA
			m.Bs = m.VB
			m.Cs = m.VC
			m.Ds = m.VD
	m.aux_exp += 1
	m.inFile50.close()
	m.inFile51.close()