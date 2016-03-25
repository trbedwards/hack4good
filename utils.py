import csv

def read_csv(fname='data/barnet_data2.csv',header=True):
  with open(fname,"r") as f:
    reader = csv.reader(f)
    if header:
      next(reader,None)
    data = []
    for row in reader:
      data.append(row)
    return data

def writeListToFile(list,file='data/output.txt'):
	with open(file, 'w') as f:
	    for item in list:
	        f.write("%f\n" % item)

def write2csv(data,file):
  # strdata = str(data)
  strdata = ','.join('%s' % str(x) for x in data) 
  with open(file, 'a') as f:
    f.write(strdata+'\n')
