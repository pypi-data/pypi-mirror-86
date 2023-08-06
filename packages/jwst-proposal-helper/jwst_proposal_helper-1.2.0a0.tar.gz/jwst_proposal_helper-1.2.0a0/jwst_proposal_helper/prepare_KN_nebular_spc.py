# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
import pandas as pd
from flam2millijansky.flam2millijansky import flam2millijansky
from hstphot.container import Container

def prepare_KN_nebular_spc(wavelength_angstrom,luminosity_per_angstrom,luminosity_distance_mpc,container):
    """
    prepare_KN_nebular_spc function prepares a spectrum file to be in a format recognizable by JWST ETC.
    #####
    Required:
      - pip install flam2millijansky, hstphot
      - basic packages in python (e.g., numpy and pandas)
    #####
    + Inputs:
      - wavelength_angstrom = 1D array of wavelengths in Angstrom, sorted ascending.
      - luminosity_per_angstrom = 1D array of luminosity in erg/s/A, parallel to wavelengths.
      - luminosity_distance_mpc = a scalar for luminosity distance in Mpc unit.
      - container = Container class for specifying the output paths. (See hstphot.container.Container; pip install hstphot).
    #####
    + Outputs:
      - return a dict with {'micron':values,'mjy':values}
      - save to a file defined by container:
        > filename: ./{0}/{1}_KN_{2}Mpc.dat where 0 = container.data['savefolder'], 1 = container.data['saveprefix'], and 2 = int(luminosity_distance_mpc).
    """
    wavelength_micron = wavelength_angstrom * 1e-4
    luminosity_distance_cm = luminosity_distance_mpc * 1e6 * 3.086e18
    flam = luminosity_per_angstrom / (4. * np.pi * np.power(luminosity_distance_cm,2))
    mjy = flam2millijansky(wavelength_angstrom,flam)
    out = {'micron':wavelength_micron,'mjy':mjy}
    out = pd.DataFrame(out)
    savefolder,saveprefix = container.data['savefolder'],container.data['saveprefix']
    string = './{0}/{1}_KN_{2}Mpc.dat'.format(savefolder,saveprefix,int(luminosity_distance_mpc))
    out.to_csv(string,index=False)
    print('Save {0}'.format(string))
    return out
