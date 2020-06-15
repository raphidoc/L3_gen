import pathlib
import numpy as np
import xarray as xr
import datetime as dt
import pandas as pd
import re

# import variables
from Meta_Gather import inFiles, variables, lat_min, lat_max, lon_min, lon_max, x_res

# define common grid
new_lat = np.arange(lat_min, lat_max, x_res, dtype='float32')
new_lon = np.arange(lon_min, lon_max, x_res, dtype='float32')

gridedFiles = list()
for n in range(len(inFiles)):
    # list of output grided files
    gridedFiles.append('./temp/regrid/L2b_'+re.split('/', inFiles[n])[-1])
    if pathlib.Path(gridedFiles[n]).exists():
        print("{} already exist".format(re.split('/', gridedFiles[n])[-1]))
        continue

    data = xr.open_dataset(inFiles[n])

    # interpolation function from SciPy working on xarray objects fast but 'linear' or 'nearest' only
    data_regrid = data[variables].interp(lat=new_lat, lon=new_lon, method='nearest')

    # outputs of .interp are in float64: heavy and not useful therefore converting back to float32
    # data_regrid = data_regrid.astype('float32')

    # Catch DateTime from attribute, work with : OLI
    DateTime = pd.to_datetime(dt.datetime.strptime(data.attrs['start_date'], '%d-%b-%Y %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S'))

    # add DateTime as new dimension
    data_regrid = data_regrid.assign_coords({'time':DateTime})
    data_regrid = data_regrid.expand_dims('time')


    # saving to netcdf containing only desired variable
    data_regrid.to_netcdf('./temp/regrid/L2b_'+re.split('/', inFiles[n])[-1])
