import csv

# function for reading csv file and returning data
def read_csv(fname='data/barnet_data2.csv',header=True):
  with open(fname,"r") as f:
    reader = csv.reader(f)
    if header:
      next(reader,None)
    data = []
    for row in reader:
      data.append(row)
    return data
