import os
from os.path import isfile, join
# import xesmf as xe
import subprocess
import xarray as xr

# set paths for input L2 files !! should accept multiple paths, for multi sensor binning
inPath = '/media/raphael/D/Data/Chone/Landsat/L2/'
inFiles = [inPath + f for f in os.listdir(inPath) if f[-3:] == '.NC']
print(inFiles)

# set desired time integration for binning, refer to http://xarray.pydata.org/en/stable/time-series.html
clims = ['season']

# set list of desired variables
variables = ['ag_443_bsi']

# get maximum extent covered by images (greedy)
lat_max = list()
lat_min = list()
lon_max = list()
lon_min = list()
for n in range(len(inFiles)):
    data = xr.open_dataset(inFiles[n])
    lat_max.append(data['lat'].attrs['valid_max'])
    lat_min.append(data['lat'].attrs['valid_min'])
    lon_max.append(data['lon'].attrs['valid_max'])
    lon_min.append(data['lon'].attrs['valid_min'])

lat_max = max(lat_max)
lat_min = min(lat_min)
lon_max = max(lon_max)
lon_min = min(lon_min)

# get resolution !! should look for different r'esolution to get max_res
y_res = abs(data['lat'].values[0] - data['lat'].values[1])
x_res = abs(data['lon'].values[0] - data['lon'].values[1])
