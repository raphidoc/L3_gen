import numpy as np
import xarray as xr
from Mask import mask
import re

import matplotlib.pyplot as plt

from Regrid import gridedFiles
from Meta_Gather import clims

# Dask out of core computation for multi file dataset concat ove time dimension
data = xr.open_mfdataset(gridedFiles, combine='by_coords')

# Add option to save stack of regrided file in one place (quick to reuse later for different computation)

# apply land mask
data = mask(data)

# compute bunch of stats !! for season, should add several option
for c in clims:
    Nobs = data.groupby('time.'+clims).count()
    stdev = data.groupby('time.'+clims).std()
    minimum = data.groupby('time.'+clims).min()
    maximum = data.groupby('time.'+clims).max()
    mean = data.groupby('time.'+clims).mean()
    median = data.groupby('time.'+clims).median()

    # One to concat them all (along a new 'stats' dimension)
    L3_data = xr.concat([Nobs, stdev, minimum, maximum, mean, median], 'stats')

    # assign coord to 'stats' dimension
    stats = ['Nobs', 'stdev', 'minimum', 'maximum', 'mean', 'median']
    L3_data = L3_data.assign_coords({'stats':stats})

    # save computed stats to netcdf file on disk
    L3_data.to_netcdf('output/L3_'+clims+'.nc')


# map_data = L3_data['ag_443_bsi'].sel(season='MAM',stats='mean')
# map_data.plot()
# plt.show()
