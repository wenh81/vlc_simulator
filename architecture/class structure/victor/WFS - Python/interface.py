#WFS_simulator(Versão Python) - OptmaLAB - 2020
#Victor Lopes Dias Ferreira
#interface.py

###Início cabeçalho
with_without = ""
wave = 0.0
zernike = 0
defocus = False
quantity = 0
diameter = 0.0
focal = 0.0
reflec = 0.0
cell = 0.0
space = 0.0
eff = 0.0
lin = 0.0
coefabs = 0.0
cent = 0.0
quant = 0.0
lanode = 0.0
lcathode = 0.0
canode = 0.0
ccathode = 0.0
rcathode = 0.0
ranode = 0.0
reset = 0.0
integ = 0.0
capac = 0.0
bthick = 0.0
ethick = 0.0
sres = 0.0
pres = 0.0
lreset = 0.0
wreset = 0.0
lbuffer = 0.0
wbuffer = 0.0
lsel = 0.0
wsel = 0.0
charge = 0.0
vmin = 0.0
vmax = 0.0
stepTran = 0.0
noise_noiseless = ""
###Fim cabeçalho

def read_from_interface():
	print("interface::read_from_interface")
	#Abertura do arquivo "c_parameters.txt" pela variável arquivo. Cada linha do arquivo é separada em um item pela variável linhas que é do tipo lista.
	arquivo = open("c_parameters.txt")
	linhas = arquivo.readlines()
	global with_without
	with_without = linhas[0]
	global wave
	wave = float(linhas[1])
	global zernike
	zernike = int(linhas[2])
	global defocus
	defocus = int(linhas[3])
	global quantity
	quantity = int(linhas[4])
	global diameter
	diameter = float(linhas[5])
	global focal
	focal = float(linhas[6])
	global reflec
	reflec = float(linhas[7])
	global cell
	cell = float(linhas[8])
	global space
	space = float(linhas[9])
	global eff
	eff = float(linhas[10])
	global lin
	lin = float(linhas[11])
	global coefabs
	coefabs = float(linhas[12])
	global cent
	cent = float(linhas[13])
	global quant
	quant = float(linhas[14])
	global lanode
	lanode = float(linhas[15])
	global lcathode
	lcathode = float(linhas[16])
	global canode
	canode = float(linhas[17])
	global ccathode
	ccathode = float(linhas[18])
	global rcathode
	rcathode = float(linhas[19])
	global ranode
	ranode = float(linhas[20])
	global reset
	reset = float(linhas[21])
	global integ
	integ = float(linhas[22])
	global capac
	capac = float(linhas[23])
	global bthick
	bthick = float(linhas[24])
	global ethick
	ethick = float(linhas[25])
	global sres
	sres = float(linhas[26])
	global pres
	pres = float(linhas[27])
	global lreset
	lreset = float(linhas[28])
	global wreset
	wreset = float(linhas[29])
	global lbuffer
	lbuffer = float(linhas[30])
	global wbuffer
	wbuffer = float(linhas[31])
	global lsel
	lsel = float(linhas[32])
	global wsel
	wsel = float(linhas[33])
	global charge
	charge = float(linhas[34])
	global vmin
	vmin = float(linhas[35])
	global vmax
	vmax = float(linhas[36])
	global stepTran
	stepTran = float(linhas[37])
	global noise_noiseless
	noise_noiseless = linhas[38]
	arquivo.close()