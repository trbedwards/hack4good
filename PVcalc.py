def calcEnergyGenerated(I,A,eta): # in one year
	Eg = I * A * eta # irradiance(one year) * area * efficiency 
	return Eg

def solarIrradiance(): # in one year
	return 1000 # kWh/m2 

def efficiency():
	return 0.1

def moneySaved(Eg,P):
	return feedInTariff(Eg,P) + exportAndSavings(Eg)

def feedInTariff(Eg,P):
	if 0 < P <= 4: # if power rating between 0 and 4kW...
		f = 0.1438
	elif 4 < P < 10:
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

def calcAreaSolarPanels(A,ratio=0.05): # assume 5% coverage on flat roof by default
	return A*ratio