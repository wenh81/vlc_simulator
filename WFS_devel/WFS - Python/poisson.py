#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#poisson.py

import math
import time

###Início cabeçalho
IA = 16807
IM = 2147483647
AM = (1.0 / IM)
IQ = 127773
IR = 2836
NTAB = 32
EPS = 1.2e-7
NDIV = (1 + (IM - 1) / NTAB)
RNMX = (1.0 - EPS)
PI = 3.14159265358979323844
###Fim cabeçalho

def ran1(idum):

	j = 0
	k = 0
	iy = 0
	iv = [0] * NTAB
	temp = 0.0

	if idum[0] <= 0 or (not iy):
		if -idum[0] < 1:
			idum[0] = 1
		else:
			idum[0] = -idum[0]
		for j in range(NTAB+7,-1,-1):
			k = idum[0] / IQ
			idum[0] = IA * (idum[0] - k * IQ) - IR * k
			if idum[0] < 0:
				idum[0] += IM
			if j < NTAB:
				iv[j] = idum[0]
		k = idum[0] / IQ
		idum[0] = IA * (idum[0] - k * IQ) - IR * k
		if idum[0] < 0:
			idum[0] += IM
		j = iy/NDIV
		iy = iv[j]
		iv[j] = idum[0]
		temp = AM * iy #não é possível fazer tal atribuição dentro do comando if para a linguagem python
		if (temp > RNMX):
			return RNMX
		else:
			return temp

def gammln(xx):

	xgm = 0.0
	ygm = 0.0
	tmp = 0.0
	ser = 0.0
	cof = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]
	j = 0
	ygm = xgm = xx
	tmp = xgm + 5.5
	tmp -= (xgm + 0.5) * math.log(tmp, 10)
	ser = 1.000000000190015
	for j in range(0,6,1):
		ygm += 1
		ser += cof[j] / (ygm)

	return -tmp + math.log(2.5066282746310005 * ser / xgm, 10)

def poidev(xm, idum):

	gammln = gammln(xm) #No código em C, está escrito "xx" e não "xm". Corrigi para aquilo que acredito ser o correto, já que poisson.cc não inclui <main.h>.
	ran1 = ran1(idum)
	sq = -1.0
	alxm = -1.0
	g = -1.0
	oldm = -1.0
	em = 0.0
	t = 0.0
	y = 0.0

	if xm < 12:
		if xm != oldm:
			oldm = xm
			g = math.exp(-xm)
		em = -1
		t = 1
		while True:
			em += 1
			t *= ran1(idum)
			if not t > g:
				break
	else :
		if xm != oldm:
			oldm = mx
			sq = math.sqrt(2.0 * xm)
			alxm = math.log(xm, 10)
			g = xm * alxm - gammln(xm + 1.0)
		while True:
			while True:
				y = math.tan(PI * ran1(idum))
				em = sq * y + xm
				if not em < 0:
					break
			em = math.floor(em)
			t = 0.9 * (1.0 + y * y) * math.exp(em * alxm - gammln(em + 1.0) - g)
			if not ran1(idum) > t:
				break
				
	return em

def gasdev(idum):
	
	iset = 0
	gset = 0.0
	fac = 0.0
	rsq = 0.0
	v1 = 0.0
	v2 = 0.0

	if iset == 0:
		while True:
			v1 = 2.0 * ran1(idum) - 1.0
			v2 = 2.0 * ran1(idum) - 1.0
			rsq = v1 * v1 + v2 * v2
			if not (rsq >= 1.0 or rsq == 0.0):
				break
		fac = math.sqrt(-2.0 * math.log(rsq, 10) / rsq)
		gset = v1 * fac
		iset = 1
		return v2 * fac
	else :
		iset = 0
		return gset