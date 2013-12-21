# -*- coding: utf-8 -*-
# Filename: SLSConverter.py
""" Main program for convert SLS data into dataExchange.
"""
from preprocessing.preprocess import Preprocess
from dataio.data_exchange import DataExchangeFile, DataExchangeEntry
#from inout import data
from dataio.file_types import Tiff
from tomoRecon import tomoRecon
from visualize import image

import matplotlib.pyplot as plt
import numpy as np

import os
import h5py

import re

#def main():

##dataFolder = '/local/data/databank/SLS_2011/Blakely_SLS'
##baseName = 'Blakely'

filename = '/local/data/databank/SLS_2011/Hornby_SLS/Hornby_b.tif'
SLSlogFile = '/local/data/databank/SLS_2011/Hornby_SLS/Hornby.log'

HDF5 = '/local/data/databank/dataExchange/microCT/Hornby_b_SLS_2011.h5'

print filename
print SLSlogFile

##dataFolder = '/local/data/Hornby_SLS'
##baseName = 'Hornby_b'


#Read input SLS data
file = open(SLSlogFile, 'r')
print '###############################'
for line in file:
    if 'Number of darks' in line:
        NumberOfDarks = re.findall(r'\d+', line)
        print 'Number of Darks', NumberOfDarks[0]
    if 'Number of flats' in line:
        NumberOfFlats = re.findall(r'\d+', line)
        print 'Number of Flats', NumberOfFlats[0]
    if 'Number of projections' in line:
        NumberOfProjections = re.findall(r'\d+', line)
        print 'Number of Projections', NumberOfProjections[0]
    if 'Number of inter-flats' in line:
        NumberOfInterFlats = re.findall(r'\d+', line)
        print 'Number of inter-flats', NumberOfInterFlats[0]
    if 'Inner scan flag' in line:
        InnerScanFlag = re.findall(r'\d+', line)
        print 'Inner scan flag', InnerScanFlag[0]
    if 'Flat frequency' in line:
        FlatFrequency = re.findall(r'\d+', line)
        print 'Flat frequency', FlatFrequency[0]
    if 'Rot Y min' in line:
        RotYmin = re.findall(r'\d+.\d+', line)
        print 'Rot Y min', RotYmin[0]
    if 'Rot Y max' in line:
        RotYmax = re.findall(r'\d+.\d+', line)
        print 'Rot Y max', RotYmax[0]
    if 'Angular step' in line:
        AngularStep = re.findall(r'\d+.\d+', line)
        print 'Angular step', AngularStep[0]
print '###############################'
file.close()

darkStart = 1
darkEnd = int(NumberOfDarks[0]) + 1
whiteStart = darkEnd
whiteEnd = whiteStart + int(NumberOfFlats[0])
projectionStart = whiteEnd
projectionEnd = projectionStart + int(NumberOfProjections[0])

print darkStart, darkEnd
print whiteStart, whiteEnd
print projectionStart, projectionEnd

dark_start = 1
dark_end = 21
white_start = 21
white_end = 221
projections_start = 221
projections_end = 1662

#dark_end = 4
#white_end = 24
#projections_end = 224

mydata = Preprocess()

#mydata.read_tiff(filename, projections_start, projections_end, slices_start = 800, slices_end = 801, white_start = white_start, white_end = white_end, dark_start= dark_start, dark_end = dark_end)
#mydata.read_tiff(filename, projections_start, projections_end, white_start = white_start, white_end = white_end, dark_start= dark_start, dark_end = dark_end)
#mydata.read_tiff(filename, projections_start, projections_end, slices_start = 800, slices_end = 820, dark_start = dark_start, dark_end = dark_end)
mydata.read_tiff(filename, projections_start, projections_end, dark_start = dark_start, dark_end = dark_end, white_start = white_start, white_end = white_end)


#Write HDF5 file.

# Open DataExchange file
f = DataExchangeFile(HDF5, mode='w') 

# Create HDF5 subgroup
# /measurement/instrument
f.add_entry( DataExchangeEntry.instrument(name={'value': 'Tomcat'}) )

# Create HDF5 subgroup
# /measurement/instrument/source
f.add_entry( DataExchangeEntry.source(name={'value': 'Swiss Light Source'},
                                    date_time={'value': "2010-11-08T14:51:56+0100"},
                                    beamline={'value': "Tomcat"},
                                    current={'value': 401.96, 'units': 'mA', 'dataset_opts': {'dtype': 'd'}},
                                    )
)

# Create HDF5 subgroup
# /measurement/instrument/monochromator
f.add_entry( DataExchangeEntry.monochromator(type={'value': 'Multilayer'},
                                            energy={'value': 19.260, 'units': 'keV', 'dataset_opts': {'dtype': 'd'}},
                                            mono_stripe={'value': 'Ru/C'},
                                            )
    )


# Create HDF5 subgroup
# /measurement/experimenter
f.add_entry( DataExchangeEntry.experimenter(name={'value':"Federica Marone"},
                                            role={'value':"Project PI"},
                                            affiliation={'value':"Swiss Light Source"},
                                            phone={'value':"+41 56 310 5318"},
                                            email={'value':"federica.marone@psi.ch"},

                )
    )

# Create HDF5 subgroup
# /measurement/instrument/detector
f.add_entry( DataExchangeEntry.detector(manufacturer={'value':'CooKe Corporation'},
                                        model={'value': 'pco dimax'},
                                        serial_number={'value': '1234XW2'},
                                        bit_depth={'value': 12, 'dataset_opts':  {'dtype': 'd'}},
                                        x_pixel_size={'value': 6.7e-6, 'dataset_opts':  {'dtype': 'f'}},
                                        y_pixel_size={'value': 6.7e-6, 'dataset_opts':  {'dtype': 'f'}},
                                        x_dimensions={'value': 2048, 'dataset_opts':  {'dtype': 'i'}},
                                        y_dimensions={'value': 2048, 'dataset_opts':  {'dtype': 'i'}},
                                        x_binning={'value': 1, 'dataset_opts':  {'dtype': 'i'}},
                                        y_binning={'value': 1, 'dataset_opts':  {'dtype': 'i'}},
                                        operating_temperature={'value': 270, 'units':'K', 'dataset_opts':  {'dtype': 'f'}},
                                        exposure_time={'value': 170, 'units':'ms', 'dataset_opts':  {'dtype': 'd'}},
                                        frame_rate={'value': 3, 'dataset_opts':  {'dtype': 'i'}},
                                        output_data={'value':'/exchange'}
                                        )
    )


f.add_entry(DataExchangeEntry.objective(magnification={'value':10, 'dataset_opts': {'dtype': 'd'}},
                                    )
    )

f.add_entry(DataExchangeEntry.scintillator(name={'value':'LuAg '},
                                            type={'value':'LuAg'},
                                            scintillating_thickness={'value':20e-6, 'dataset_opts': {'dtype': 'd'}},
        )
    )

# Create HDF5 subgroup
# /measurement/experiment
f.add_entry( DataExchangeEntry.experiment( proposal={'value':"e11218"},
            )
    )


# Create HDF5 subgroup
# /measurement/sample
f.add_entry( DataExchangeEntry.sample( name={'value':'Hornby_b'},
                                        description={'value':'rock sample tested at ALS and APS'},
        )
    )



# Create core HDF5 dataset in exchange group for 180 deep stack
# of x,y images /exchange/data
f.add_entry( DataExchangeEntry.data(data={'value': mydata.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
f.add_entry( DataExchangeEntry.data(data_dark={'value': mydata.dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
f.add_entry( DataExchangeEntry.data(data_white={'value': mydata.white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))

f.close()

##mydata.normalize()
##mydata.remove_rings(wname='db10', sigma=2)
##mydata.median_filter()
##mydata.optimize_center()
##mydata.optimize_center(center_init=1010)
##mydata.center = 1404.6484375
##mydata.retrieve_phase(pixel_size=0.65e-4, dist=40, energy=22.4, delta_over_mu=1e-8)
##mydata.data = np.exp(-mydata.data)


# Reconstruct data.
#recon = tomoRecon.tomoRecon(mydata)
#recon.run(mydata)

# Save data.
#f = Tiff()
#f.write(recon.data, file_name='/local/dgursoy/GIT/tomopy/data/test_.tiff')

# Visualize data.
#image.show_slice(recon.data)

#print data.shape
#print data_dark.shape
#print data_white.shape

# Create new folders.
##HDF5File = dataFolder + '/' + baseName + 'ORG.' + 'h5'
##dirPath = os.path.dirname(HDF5File)
##if not os.path.exists(dirPath):
##    os.makedirs(dirPath)
##
##
###if __name__ == "__main__":
###    main()

