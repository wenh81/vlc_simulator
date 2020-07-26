#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#ZERNIKE.py

import math
import sys

###Início cabeçalho
Pi = 3.14159265358979323844
Pi2 = 6.28318530717958647688
class FIELD:
	def __init__(self, number, size, Lambda, int1, int2, int3, double1, double2, double3, real, imaginary):
		self.number = number
		self.size = size
		self.Lambda = Lambda
		self.int1 = int1
		self.int2 = int2
		self.int3 = int3
		self.double1 = double1
		self.double2 = double2
		self.double3 = double3
		self.real = real
		self.imaginary = imaginary

field = FIELD(0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0)
pass_string = [0.0]
p_pass = [10]
###Fim cabeçalho

def phase(y, x):

	pp = 0.0

	if x == 0:
		if y > 0:
			pp = 0.5 * Pi
		if y == 0:
			pp = 0
		if y < 0:
			pp = -0.5 * Pi
	else :
		if y != 0:
			pp = math.atan2(y, x)
		else :
			if x > 0:
				pp = 0.0
			else :
				pp = Pi

	return pp

def factor(n):
	
	product = 0.0

	if n < 0:
		print("factorial: argument is negative, exiting", file = sys.stderr)
		exit(1)
	if n == 0:
		return 1
	else :
		product = 1.0
		while n >= 1 :
			product *= n
			n += -1
			
		return product

def Zernike(n, m, rho, phi):
	#print("ZERNIKE::Zernike")

	s = 0
	int_sign = 0
	mm = 0
	ncheck = 0
	ind = 0
	varsum = 0.0 #Substitui a variável sum no código em C
	product = 0.0

	if n < 0:
		print("Zernike: n must be >0; |m| must be less or equal than n\nif n is odd then m must be odd,\nif n is even then m must be even", file = sys.stderr)
		exit(1)
	ind = 0
	for ncheck in range(n,-n-2,-2):
		if ncheck == m:
			ind = 1
	if ind == 0:
		print("Zernike: n must be >0; |m| must be less or equal than n\nif n is odd then m must be odd,\nif n is even then m must be even", file = sys.stderr)
		exit(1)
	mm = int(math.fabs(m))
	varsum = 0
	int_sign = 1
	for s in range(0,int((n - mm) / 2) + 1,1):
		if (n - 2 * s != 0):
			product = math.pow(rho, n - 2 * s)
		else :
			product = 1
		product *= factor(n - s) * int_sign
		product /= factor(s) * factor(((n + mm) / 2) - s) * factor(((n - mm) / 2) - s)
		varsum += product
		int_sign = -int_sign
	if m >= 0:
		return (varsum * math.cos(m * phi))
	else :
		return (varsum * math.sin(m * phi))