def mask(data):
    import subprocess
    import geopandas as gpd
    import rioxarray
    from shapely.geometry import mapping
    from Meta_Gather import lat_min, lat_max, lon_min, lon_max
    # import matplotlib.pyplot as plt

    inMask = './common/masks/gshhg-shp-2.3.7/GSHHS_shp/f/GSHHS_f_L1.shp'
    TempMask = './temp/mask/GSHHS_f_L1_TEMP.shp'

    # clip shapefile to raster extent
    Cclip = 'ogr2ogr -progress -clipsrc '+str(lon_min)+' '+str(lat_min)+' '+str(lon_max)+' '+str(lat_max)+' '+TempMask+' '+inMask
    subprocess.call(Cclip, shell=True)

    # read Mask (shapefile) in geopandas
    Mask = gpd.read_file(TempMask)
    # Mask.plot()
    # plt.show()

    # Spatial dims (names) and crs need to be set
    data.rio.set_spatial_dims('lon', 'lat', inplace=True)
    data = data.rio.write_crs(4326)
    data = data.rio.clip(Mask.geometry.apply(mapping), Mask.crs, drop=False, invert=True)
    return data


# load on memory too heavy
#data.to_netcdf(outPath+'masked.nc')

# Shapefile mask is use instead of raster
# should get raster size here to be use in Crasterize (-ts ...)
# size = subprocess.run('gdalinfo '+outFiles[1], shell=True, stdout=subprocess.PIPE)
# size.stdout

#Crasterize = 'gdal_rasterize -burn 999 -ts 512 512 -of GTiff '+TempMask+' '+TempMaskRaster
#subprocess.call(Crasterize, shell=True)

# Mask = rast.open(TempMaskRaster)
# show(Mask)
#
# Mask = xr.open_rasterio(TempMaskRaster)
# Mask.rio.crs
# Mask.plot()
# plt.show()



# create output files
# outPath = '/media/raphael/D/Data/Chone/Landsat/L2/NC/masked/'
# cstr = 'mkdir -p '+outPath
# subprocess.call(cstr, shell=True)

# outFiles = [outPath + f for f in os.listdir(inPath) if isfile(join(inPath, f))]
# print(outFiles)
# for n in range(len(outFiles)):
#     inFile = inFiles[n]
#     outFile = outFiles[n]
#     cstr = 'cp -u '+inFile+' '+outFile
#     subprocess.call(cstr, shell=True)

# for n in range(len(outFiles)):
#     data = xr.open_dataset(outFiles[n])
#     print(data['Longitude'])