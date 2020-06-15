import os
from os.path import isfile, join
import netCDF4
import re
import subprocess
import rioxarray
import array

trans = xr.open_dataset('output/L3_'+clim+'.nc')

for c in clim:
    time_group = list(L3_data.coords[time[0]].values)
    for t in time_group:
        for j in variables:
            for s in stats:
                L3_tif = trans.sel(**{c: t}, **{'stats': s})
                L3_tif = L3_tif[j].rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=False)
                L3_tif = L3_tif.rio.write_crs(4326)
                # create output path
                outPath = 'output/'+t+'/'+j
                cstr = 'mkdir -p '+outPath
                subprocess.call(cstr, shell=True)
                L3_tif.rio.to_raster('output/'+t+'/'+j+'/L3_'+t+'_'+j+'_'+s+'.tif')


# inPath = '/media/raphael/D/Data/Chone/Landsat/L2/NC/'
# inFiles = [inPath + f for f in os.listdir(inPath) if isfile(join(inPath, f))]
# print(inFiles)
#
# for n in range(len(inFiles)):
#     date = re.findall(r"(?<=/)\d\d\d\d", inFiles[n])[0]
#     Cmkdir = 'mkdir -p '+inPath+date
#     subprocess.call(Cmkdir, shell=True)
#     data = netCDF4.Dataset(inFiles[n])
#     r = re.compile(".*\d\d\d\d$")
#     variable = list(filter(r.match, list(data.variables.keys())))
#     for j in range(len(variable)):
#         Ctranslate = 'gdal_translate -of Gtiff NETCDF:"'+inFiles[n]+'":'+variable[j]+' '+inPath+date+'/'+variable[j]+'.tif'
#         subprocess.call(Ctranslate, shell=True)