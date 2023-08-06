# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
import pandas as pd
from hstphot.container import Container

def rescale_by_distance(flux,in_luminosity_distance,out_luminosity_distance,container,column_names = ['wavelength','flux'],wavelength=None):
    """
    rescale_by_distance is a function to rescale flux given lumionsity distance to a different distance.
    #####
    + Required:
      - pip install hstphot
      - numpy, pandas
    #####
    + Inputs:
      - flux = 1D array of fluxes
      - in_luminosity_distance = a scalar of luminosity distance specified for the flux
      - out_luminosity_distance = a scalar of luminosity distance to be scaled to. Must be the same unit as in_luminosity_distance.
      - container = hstphot.container.Container class
      - column_names = ['wavelength','flux'] (default). They will define column names of saved output file
      - wavelength = None (default). If supplied as 1D array (parallel to flux), this array will be saved as the first column 'wavelength' in the output file
    #####
    + Outputs:
     - return flux_scale = 1D array of scaled fluxes
     - output file to filepath = ./savefolder/saveprefix_from_luminosity_distance_{int(in_luminosity_distance)}_to_{int(out_luminosity_distance)}.dat
       > Column1: name = column_names[0], values = wavelength
       > Column2: name = column_names[1], values = flux_scale
    """
    scale = in_luminosity_distance / out_luminosity_distance
    flux_scale = flux * np.power(scale,2)
    ##### save #####
    if wavelength is None:
        wavelength = np.full_like(flux_scale,np.nan,dtype=object)
    out = {column_names[0]:wavelength,column_names[1]:flux_scale}
    out = pd.DataFrame(out)
    savefolder, saveprefix = container.data['savefolder'],container.data['saveprefix']
    string = './{0}/{1}_from_luminositdy_distance_{2}_to_{3}.dat'.format(savefolder,saveprefix,int(in_luminosity_distance),int(out_luminosity_distance))
    out.to_csv(string,index=False,sep=' ')
    print('Save {0}'.format(string))
    return flux_scale
    