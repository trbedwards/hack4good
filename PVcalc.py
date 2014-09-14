def calcEnergyGenerated(I,A,eta): # in one year
	Eg = I * A * eta # irradiance(one year) * area * efficiency 
	return Eg

def solarIrradiance(): # in one year
	return 1000 # kWh/m2 

def efficiency():
	return 0.15

def moneySaved(Eg,P):
	return feedInTariff(Eg,P) + exportAndSavings(Eg)

def feedInTariff(Eg,P):
	if 0 < P <= 4: # if power rating between 0 and 4kW...
		f = 0.1438
	elif 4 < P <= 10:
		f = 0.1303
	else:
		f = 0.1213
	return f*Eg 

# c = cost of convential usage per kWh, e = export tariff rate
def exportAndSavings(Eg,c=0.09,e=0.0477):
	return Eg/2*e + Eg/2*c # assume 50/50 split between export and used

# p = power rating per m2 of solar panel, A = area of solar panels (m2)
def powerInstalled(A,p=0.15):
	return A*p

# A = area of polygon, roofRatio = ratio of polygon that is roof, coverage = amount of useful space covered in PV 
def calcAreaSolarPanels(areaPoly,coverage=0.10,roofRatio=0.5,southOnly=True): 
	areaPV = areaPoly * roofRatio * coverage
	if southOnly:
		areaPV *= 0.5
	return areaPV

# rate of 1500 pounds per kW
def calcCostSolarPanels(P):
	if 0 < P <= 4:
		c = 1850
	if 4 < P <= 10:
		c = 1570
	else:
		c = 1330
	return P*c
