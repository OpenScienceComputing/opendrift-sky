#!/usr/bin/env python
# coding: utf-8

# 28 day OpenDrift run with 10 particles

import numpy as np
from opendrift.readers import reader_ROMS_intake
from opendrift.models.oceandrift import OceanDrift
import intake
import xarray as xr
import datetime as dt
import fsspec


intake_catalog = 'https://renc.osn.xsede.org/rsignellbucket2/rsignell/CNAPS/cnaps_intake.yml'

dataset = 'CNAPS_xinfo_zarr_nochunk-cache'     #   10 particles: 1min 8s for 28 days, 8.9 main loop to run 2 days

fs = fsspec.filesystem('s3', anon=False, client_kwargs=dict(endpoint_url='https://renc.osn.xsede.org'))

ncfile = 'sky_output.nc'
s3_ncfile = f's3://rsignellbucket2/rsignell/CNAPS/output/{ncfile}'

cat = intake.open_catalog(intake_catalog)

o = OceanDrift(loglevel=50)  # Set loglevel to 0 for debug information

cnaps = reader_ROMS_intake.Reader(intake_catalog=cat, dataset=dataset)
o.add_reader(cnaps)

# Seed elements at defined positions, depth and time
lat,lon = (42.807016,-70.46207)
o.seed_elements(lon=lon, lat=lat, radius=1000, number=10, 
                z=np.linspace(0, -150, 10), time=dt.datetime(2012,10,29,0,0,0))
# Running model

o.run(time_step=3600, duration=dt.timedelta(days=28), outfile=ncfile)

# Upload the file to S3
fs.upload(ncfile, s3_ncfile)

fs = fsspec.filesystem('file')
fs.rm(ncfile)

# Print and plot results, with lines colored by particle depth
print(o)
#o.plot(linecolor='z', fast=True)
